"""
Admin configuration for voice app.
"""
from django.contrib import admin
from .models import VoiceInteraction, VoicePreferences, AudioTranscription, TextToSpeech


@admin.register(VoiceInteraction)
class VoiceInteractionAdmin(admin.ModelAdmin):
    """Admin for VoiceInteraction model."""
    list_display = ['user', 'session', 'language', 'confidence_score', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['user__email', 'transcript']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'session']


@admin.register(VoicePreferences)
class VoicePreferencesAdmin(admin.ModelAdmin):
    """Admin for VoicePreferences model."""
    list_display = ['user', 'voice_engine', 'voice_language', 'speech_rate']
    list_filter = ['voice_engine', 'voice_language']
    search_fields = ['user__email']
    raw_id_fields = ['user']


@admin.register(AudioTranscription)
class AudioTranscriptionAdmin(admin.ModelAdmin):
    """Admin for AudioTranscription model."""
    list_display = ['user', 'language', 'status', 'confidence_score', 'created_at']
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['user__email', 'transcript']
    readonly_fields = ['created_at', 'completed_at']
    raw_id_fields = ['user']


@admin.register(TextToSpeech)
class TextToSpeechAdmin(admin.ModelAdmin):
    """Admin for TextToSpeech model."""
    list_display = ['user', 'voice_engine', 'language', 'status', 'created_at']
    list_filter = ['voice_engine', 'language', 'status', 'created_at']
    search_fields = ['user__email', 'text']
    readonly_fields = ['created_at', 'completed_at']
    raw_id_fields = ['user']
