from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
try:
    import speech_recognition as sr
except ImportError:
    sr = None
try:
    from gtts import gTTS
except ImportError:
    gTTS = None
import os
from django.conf import settings
from django.core.files.base import ContentFile
from .models import VoiceInteraction, VoicePreferences, AudioTranscription, TextToSpeech
from .serializers import (
    VoiceInteractionSerializer, VoicePreferencesSerializer,
    AudioTranscriptionSerializer, TextToSpeechSerializer
)


class VoiceInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = VoiceInteractionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return VoiceInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoicePreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = VoicePreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VoicePreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AudioTranscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = AudioTranscriptionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return AudioTranscription.objects.filter(user=self.request.user)


class TextToSpeechViewSet(viewsets.ModelViewSet):
    serializer_class = TextToSpeechSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TextToSpeech.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def speech_to_text(request):
    """Convert speech to text"""
    if sr is None:
        return Response(
            {'error': 'Speech recognition library not installed'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    if 'audio' not in request.FILES:
        return Response(
            {'error': 'No audio file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    audio_file = request.FILES['audio']
    language = request.data.get('language', 'en-US')

    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()  # type: ignore

        # Convert uploaded file to AudioData
        audio_data = sr.AudioData(audio_file.read(), 16000, 2)  # type: ignore # Assuming 16kHz, 2 bytes per sample

        # Perform speech recognition
        transcript = recognizer.recognize_google(audio_data, language=language)

        return Response({
            'transcript': transcript,
            'language': language
        })

    except sr.UnknownValueError:  # type: ignore
        return Response(
            {'error': 'Speech recognition could not understand audio'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except sr.RequestError as e:  # type: ignore
        return Response(
            {'error': f'Could not request results from speech recognition service: {e}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing audio: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def text_to_speech(request):
    """Convert text to speech"""
    if gTTS is None:
        return Response(
            {'error': 'Text-to-speech library not installed'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    text = request.data.get('text')
    language = request.data.get('language', 'en')
    voice_gender = request.data.get('voice_gender', 'neutral')

    if not text:
        return Response(
            {'error': 'No text provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)  # type: ignore

        # Save to temporary file
        temp_filename = f"tts_{request.user.id}_{hash(text)}.mp3"
        temp_path = os.path.join(settings.MEDIA_ROOT, 'voice', 'temp', temp_filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        tts.save(temp_path)

        # Return file URL
        file_url = f"{settings.MEDIA_URL}voice/temp/{temp_filename}"

        return Response({
            'audio_url': file_url,
            'text': text,
            'language': language
        })

    except Exception as e:
        return Response(
            {'error': f'Error generating speech: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def voice_commands_help(request):
    """Get list of available voice commands"""
    commands = [
        {
            'command': 'open course [course name]',
            'description': 'Open a specific course'
        },
        {
            'command': 'start quiz',
            'description': 'Start a quiz'
        },
        {
            'command': 'ask tutor [question]',
            'description': 'Ask the AI tutor a question'
        },
        {
            'command': 'show progress',
            'description': 'Display learning progress'
        },
        {
            'command': 'next lesson',
            'description': 'Go to next lesson'
        },
        {
            'command': 'repeat',
            'description': 'Repeat the last response'
        }
    ]

    return Response({'commands': commands})