"""
Emotion detection and response style adaptation for Luna.
"""
import logging
import re
from typing import TypedDict

logger = logging.getLogger(__name__)


class EmotionResult(TypedDict):
    emotion: str
    confidence: float
    valence: float      # -1.0 (negative) to +1.0 (positive)
    arousal: float      # 0.0 (calm) to 1.0 (excited)


# Keyword-based emotion signals
EMOTION_KEYWORDS: dict[str, list[str]] = {
    'happy': [
        'happy', 'great', 'awesome', 'love', 'wonderful', 'excited', 'yay', 'fantastic',
        'good', 'amazing', 'excellent', 'joy', 'thrilled', 'delighted', 'wonderful',
        'خوش', 'اچھا', 'زبردست',  # Urdu
        'సంతోషం', 'మంచి', 'అద్భుతం',  # Telugu
    ],
    'sad': [
        'sad', 'unhappy', 'depressed', 'miserable', 'crying', 'tears', 'lonely',
        'hopeless', 'down', 'upset', 'heartbroken', 'disappointed', 'lost',
        'اداس', 'دکھی', 'رونا',  # Urdu
        'దుఃఖం', 'బాధ', 'ఒంటరి',  # Telugu
    ],
    'anxious': [
        'anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic', 'stress',
        'stressed', 'overwhelmed', 'fear', 'terrified', 'uneasy', 'concerned',
        'پریشان', 'ڈر', 'خوف',  # Urdu
        'ఆందోళన', 'భయం', 'నిరాశ',  # Telugu
    ],
    'angry': [
        'angry', 'furious', 'mad', 'hate', 'annoyed', 'frustrated', 'rage',
        'irritated', 'disgusted', 'outraged', 'livid',
        'غصہ', 'ناراض',  # Urdu
        'కోపం', 'చిరాకు',  # Telugu
    ],
    'neutral': [],
}

VALENCE_MAP = {
    'happy': 0.9,
    'sad': -0.8,
    'anxious': -0.5,
    'angry': -0.7,
    'neutral': 0.0,
}

AROUSAL_MAP = {
    'happy': 0.7,
    'sad': 0.2,
    'anxious': 0.8,
    'angry': 0.9,
    'neutral': 0.3,
}


def detect_emotion(text: str) -> EmotionResult:
    """
    Detect the dominant emotion in the user's message using keyword analysis.
    Returns an EmotionResult dict with emotion, confidence, valence, and arousal.
    """
    if not text:
        return EmotionResult(emotion='neutral', confidence=1.0, valence=0.0, arousal=0.3)

    lower_text = text.lower()
    scores: dict[str, int] = {emotion: 0 for emotion in EMOTION_KEYWORDS}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in lower_text:
                scores[emotion] += 1

    total = sum(scores.values())
    if total == 0:
        return EmotionResult(emotion='neutral', confidence=0.9, valence=0.0, arousal=0.3)

    dominant = max(scores, key=lambda e: scores[e])
    confidence = round(scores[dominant] / max(total, 1), 2)
    confidence = min(0.95, confidence + 0.4)  # Boost baseline confidence

    return EmotionResult(
        emotion=dominant,
        confidence=confidence,
        valence=VALENCE_MAP.get(dominant, 0.0),
        arousal=AROUSAL_MAP.get(dominant, 0.3),
    )


def adjust_response_style(base_prompt: str, emotion_data: EmotionResult) -> str:
    """
    Append emotion-aware style guidance to the system prompt.
    Luna adapts her tone based on the user's emotional state.
    """
    emotion = emotion_data.get('emotion', 'neutral')
    valence = emotion_data.get('valence', 0.0)

    style_guides = {
        'happy': (
            "\n\nThe user seems happy and upbeat right now! Match their positive energy, "
            "be cheerful and enthusiastic. Celebrate with them!"
        ),
        'sad': (
            "\n\nThe user seems sad or troubled. Be extra gentle, warm, and comforting. "
            "Speak softly, validate their feelings, and offer emotional support. "
            "Don't rush to solutions — first acknowledge how they feel."
        ),
        'anxious': (
            "\n\nThe user seems anxious or worried. Be calm, reassuring, and grounding. "
            "Speak at a measured pace. Help them feel safe and understood. "
            "Offer practical comfort and breathing space."
        ),
        'angry': (
            "\n\nThe user seems frustrated or upset. Stay calm and non-defensive. "
            "Acknowledge their frustration without escalating. Be patient and validating. "
            "Help de-escalate gently."
        ),
        'neutral': "",
    }

    style_addition = style_guides.get(emotion, "")
    return base_prompt + style_addition
