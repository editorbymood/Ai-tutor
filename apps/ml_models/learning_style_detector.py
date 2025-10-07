"""
Machine Learning model for detecting learning styles using K-means clustering.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class LearningStyleDetector:
    """
    Detect student learning styles using K-means clustering.
    
    Features used:
    - Time spent on different content types (video, text, interactive)
    - Quiz performance patterns
    - Interaction frequency
    - Content preference patterns
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=4)
        self.n_clusters = 4  # Visual, Auditory, Reading/Writing, Kinesthetic
        self.model_path = os.path.join(
            settings.ML_MODELS_DIR,
            'learning_style_detector.pkl'
        )
    
    def extract_features(self, user_data):
        """
        Extract features from user interaction data.
        
        Args:
            user_data: Dict containing user interaction metrics
        
        Returns:
            numpy array of features
        """
        features = [
            user_data.get('video_time', 0),
            user_data.get('text_time', 0),
            user_data.get('interactive_time', 0),
            user_data.get('quiz_attempts', 0),
            user_data.get('chat_interactions', 0),
            user_data.get('visual_content_views', 0),
            user_data.get('audio_content_views', 0),
            user_data.get('text_content_views', 0),
            user_data.get('practice_exercises_completed', 0),
            user_data.get('avg_session_duration', 0),
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data):
        """
        Train the K-means clustering model.
        
        Args:
            training_data: DataFrame with user interaction features
        """
        logger.info("Training learning style detector...")
        
        # Prepare data
        X = training_data.values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA for dimensionality reduction
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Train K-means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        self.model.fit(X_pca)
        
        logger.info("Learning style detector trained successfully")
        
        # Save model
        self.save_model()
    
    def predict(self, user_data):
        """
        Predict learning style for a user.
        
        Args:
            user_data: Dict containing user interaction metrics
        
        Returns:
            str: Predicted learning style
        """
        if self.model is None:
            self.load_model()
        
        # Extract and prepare features
        features = self.extract_features(user_data)
        features_scaled = self.scaler.transform(features)
        features_pca = self.pca.transform(features_scaled)
        
        # Predict cluster
        cluster = self.model.predict(features_pca)[0]
        
        # Map cluster to learning style
        style_mapping = {
            0: 'visual',
            1: 'auditory',
            2: 'reading_writing',
            3: 'kinesthetic'
        }
        
        return style_mapping.get(cluster, 'unknown')
    
    def get_cluster_characteristics(self, cluster_id):
        """Get characteristics of a specific cluster."""
        if self.model is None:
            return None
        
        centroid = self.model.cluster_centers_[cluster_id]
        return centroid
    
    def save_model(self):
        """Save the trained model to disk."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'pca': self.pca,
        }
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a trained model from disk."""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.pca = model_data['pca']
            logger.info(f"Model loaded from {self.model_path}")
        else:
            logger.warning(f"No model found at {self.model_path}")


# Singleton instance
learning_style_detector = LearningStyleDetector()