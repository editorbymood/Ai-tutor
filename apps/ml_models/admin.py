"""
Admin configuration for ML models.
"""
from django.contrib import admin
from .models import MLModel


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    """Admin interface for ML Model."""
    
    list_display = [
        'name', 'model_type', 'version', 'algorithm',
        'accuracy', 'is_active', 'trained_at'
    ]
    list_filter = ['model_type', 'is_active', 'trained_at']
    search_fields = ['name', 'description']
    readonly_fields = ['trained_at']