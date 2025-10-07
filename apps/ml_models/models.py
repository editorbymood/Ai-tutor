"""
Models for ML model management.
"""
from django.db import models
import uuid


class MLModel(models.Model):
    """Track ML models and their versions."""
    
    MODEL_TYPE_CHOICES = [
        ('learning_style', 'Learning Style Clustering'),
        ('performance_prediction', 'Performance Prediction'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('recommendation', 'Recommendation System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=30, choices=MODEL_TYPE_CHOICES)
    version = models.CharField(max_length=50)
    
    # Model details
    description = models.TextField()
    algorithm = models.CharField(max_length=100)
    hyperparameters = models.JSONField(default=dict)
    
    # Performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    # File path
    model_file_path = models.CharField(max_length=500)
    
    # Status
    is_active = models.BooleanField(default=False)
    
    # Timestamps
    trained_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ml_models'
        ordering = ['-trained_at']
    
    def __str__(self):
        return f"{self.name} v{self.version}"