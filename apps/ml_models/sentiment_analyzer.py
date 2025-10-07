"""
Sentiment analysis for student feedback and chat messages.
"""
from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Analyze sentiment of text using TextBlob.
    
    Used for:
    - Course reviews
    - Student feedback
    - Chat messages
    """
    
    def analyze(self, text):
        """
        Analyze sentiment of text.
        
        Args:
            text: String to analyze
        
        Returns:
            dict: Sentiment analysis results
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Classify sentiment
            if polarity > 0.1:
                label = 'positive'
            elif polarity < -0.1:
                label = 'negative'
            else:
                label = 'neutral'
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'label': label,
                'confidence': abs(polarity)
            }
        
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'label': 'neutral',
                'confidence': 0.0
            }
    
    def analyze_batch(self, texts):
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of strings
        
        Returns:
            list: List of sentiment analysis results
        """
        return [self.analyze(text) for text in texts]
    
    def get_overall_sentiment(self, texts):
        """
        Get overall sentiment from multiple texts.
        
        Args:
            texts: List of strings
        
        Returns:
            dict: Aggregated sentiment
        """
        results = self.analyze_batch(texts)
        
        if not results:
            return {
                'average_polarity': 0.0,
                'average_subjectivity': 0.0,
                'overall_label': 'neutral'
            }
        
        avg_polarity = sum(r['polarity'] for r in results) / len(results)
        avg_subjectivity = sum(r['subjectivity'] for r in results) / len(results)
        
        # Classify overall sentiment
        if avg_polarity > 0.1:
            overall_label = 'positive'
        elif avg_polarity < -0.1:
            overall_label = 'negative'
        else:
            overall_label = 'neutral'
        
        return {
            'average_polarity': avg_polarity,
            'average_subjectivity': avg_subjectivity,
            'overall_label': overall_label,
            'sample_count': len(results)
        }


# Singleton instance
sentiment_analyzer = SentimentAnalyzer()