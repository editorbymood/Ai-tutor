from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'interactions', views.VoiceInteractionViewSet, basename='voice-interaction')
router.register(r'preferences', views.VoicePreferencesViewSet, basename='voice-preference')
router.register(r'transcriptions', views.AudioTranscriptionViewSet, basename='audio-transcription')
router.register(r'tts', views.TextToSpeechViewSet, basename='text-to-speech')

urlpatterns = [
    path('', include(router.urls)),
    path('stt/', views.speech_to_text, name='speech-to-text'),
    path('tts/', views.text_to_speech, name='text-to-speech'),
    path('commands/', views.voice_commands_help, name='voice-commands'),
]