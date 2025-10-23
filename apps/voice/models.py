from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class VoiceInteraction(models.Model):
    """Records of voice interactions with AI tutor"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_interactions')
    session = models.ForeignKey('ai_tutor.ChatSession', on_delete=models.CASCADE, related_name='voice_interactions')
    audio_file = models.FileField(upload_to='voice/audio/', blank=True, null=True)
    transcript = models.TextField()  # Speech-to-text result
    response_text = models.TextField()  # AI response text
    response_audio = models.FileField(upload_to='voice/responses/', blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)  # STT confidence
    language = models.CharField(max_length=10, default='en')
    duration_seconds = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Voice interaction by {self.user.username}"


class VoicePreferences(models.Model):
    """User preferences for voice interactions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voice_preferences')
    voice_engine = models.CharField(max_length=50, choices=[
        ('google', 'Google Text-to-Speech'),
        ('azure', 'Azure Cognitive Services'),
        ('amazon', 'Amazon Polly'),
    ], default='google')
    voice_language = models.CharField(max_length=10, default='en-US')
    voice_gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('neutral', 'Neutral'),
    ], default='neutral')
    speech_rate = models.FloatField(default=1.0, validators=[MinValueValidator(0.5), MaxValueValidator(2.0)])
    volume = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(2.0)])
    enable_auto_play = models.BooleanField(default=True)
    enable_voice_commands = models.BooleanField(default=True)

    def __str__(self):
        return f"Voice preferences for {self.user.username}"


class AudioTranscription(models.Model):
    """General audio transcription service"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transcriptions')
    audio_file = models.FileField(upload_to='voice/transcriptions/')
    transcript = models.TextField(blank=True)
    language = models.CharField(max_length=10, default='en')
    status = models.CharField(max_length=20, choices=[
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='processing')
    confidence_score = models.FloatField(default=0.0)
    duration_seconds = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transcription for {self.user.username}"


class TextToSpeech(models.Model):
    """Text-to-speech conversion records"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tts_requests')
    text = models.TextField()
    audio_file = models.FileField(upload_to='voice/tts/')
    voice_engine = models.CharField(max_length=50, default='google')
    language = models.CharField(max_length=10, default='en-US')
    status = models.CharField(max_length=20, choices=[
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"TTS for {self.user.username}"