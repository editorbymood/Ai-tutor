"""
Machine Learning model for predicting student performance using Random Forest.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PerformancePredictor:
    """
    Predict student performance and identify at-risk students.
    
    Features used:
    - Quiz scores
    - Time spent studying
    - Engagement metrics
    - Learning style
    - Course progress
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = os.path.join(
            settings.ML_MODELS_DIR,
            'performance_predictor.pkl'
        )
    
    def extract_features(self, student_data):
        """
        Extract features from student data.
        
        Args:
            student_data: Dict containing student metrics
        
        Returns:
            numpy array of features
        """
        # Encode learning style
        learning_style_encoding = {
            'visual': 0,
            'auditory': 1,
            'reading_writing': 2,
            'kinesthetic': 3,
            'unknown': 4
        }
        
        features = [
            student_data.get('average_quiz_score', 0),
            student_data.get('total_study_time', 0),
            student_data.get('current_streak', 0),
            student_data.get('courses_enrolled', 0),
            student_data.get('lessons_completed', 0),
            student_data.get('quizzes_taken', 0),
            student_data.get('chat_messages_sent', 0),
            student_data.get('average_session_duration', 0),
            learning_style_encoding.get(
                student_data.get('learning_style', 'unknown'),
                4
            ),
            student_data.get('days_since_enrollment', 0),
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data, labels):
        """
        Train the Random Forest classifier.
        
        Args:
            training_data: DataFrame with student features
            labels: Array of performance labels (0: at-risk, 1: on-track, 2: excelling)
        """
        logger.info("Training performance predictor...")
        
        # Prepare data
        X = training_data.values
        y = labels
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        logger.info(f"Model trained - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
        
        # Save model
        self.save_model()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def predict(self, student_data):
        """
        Predict student performance.
        
        Args:
            student_data: Dict containing student metrics
        
        Returns:
            dict: Prediction results
        """
        if self.model is None:
            self.load_model()
        
        # Extract and prepare features
        features = self.extract_features(student_data)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Map prediction to label
        label_mapping = {
            0: 'at_risk',
            1: 'on_track',
            2: 'excelling'
        }
        
        return {
            'prediction': label_mapping.get(prediction, 'unknown'),
            'confidence': float(max(probabilities)),
            'probabilities': {
                'at_risk': float(probabilities[0]),
                'on_track': float(probabilities[1]),
                'excelling': float(probabilities[2])
            }
        }
    
    def get_feature_importance(self):
        """Get feature importance scores."""
        if self.model is None:
            return None
        
        feature_names = [
            'average_quiz_score',
            'total_study_time',
            'current_streak',
            'courses_enrolled',
            'lessons_completed',
            'quizzes_taken',
            'chat_messages_sent',
            'average_session_duration',
            'learning_style',
            'days_since_enrollment'
        ]
        
        importances = self.model.feature_importances_
        return dict(zip(feature_names, importances))
    
    def save_model(self):
        """Save the trained model to disk."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
        }
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a trained model from disk."""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            logger.info(f"Model loaded from {self.model_path}")
        else:
            logger.warning(f"No model found at {self.model_path}")


# Singleton instance
performance_predictor = PerformancePredictor()