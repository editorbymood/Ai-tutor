from rest_framework import serializers
from .models import VoiceInteraction, VoicePreferences, AudioTranscription, TextToSpeech


class VoiceInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceInteraction
        fields = ['id', 'session', 'audio_file', 'transcript', 'response_text',
                 'response_audio', 'confidence_score', 'language', 'duration_seconds',
                 'created_at']


class VoicePreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoicePreferences
        fields = ['id', 'user', 'voice_engine', 'voice_language', 'voice_gender',
                 'speech_rate', 'volume', 'enable_auto_play', 'enable_voice_commands']


class AudioTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTranscription
        fields = ['id', 'audio_file', 'transcript', 'language', 'status',
                 'confidence_score', 'duration_seconds', 'created_at', 'completed_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TextToSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToSpeech
        fields = ['id', 'text', 'audio_file', 'voice_engine', 'language', 'status',
                 'created_at', 'completed_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)