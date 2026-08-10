import { useRef, useEffect, useCallback } from 'react';
import { useVoiceStore } from '../store/voiceStore';
import { useAuthStore } from '../store/authStore';

export const useVoice = () => {
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const { tokens } = useAuthStore();
  const { setConnected, setListening, setSpeaking, setTranscript, setVoiceState } = useVoiceStore();

  const connectToVoice = useCallback(() => {
    if (wsRef.current) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = import.meta.env.VITE_WS_URL || `${protocol}//${host}/ws/voice/`;
    
    // In a real app we might pass token in query string or subprotocol
    wsRef.current = new WebSocket(`${wsUrl}?token=${tokens?.access}`);

    wsRef.current.onopen = () => {
      setConnected(true);
      setVoiceState('idle');
    };

    wsRef.current.onmessage = async (event) => {
      // Handle incoming binary audio (TTS) or JSON (transcript)
      if (typeof event.data === 'string') {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'transcript') {
            setTranscript(data.text);
          } else if (data.type === 'state') {
            setVoiceState(data.state);
          }
        } catch (e) {
          console.error('WS message error', e);
        }
      } else if (event.data instanceof Blob) {
        // Handle audio playback
        setSpeaking(true);
        if (!audioContextRef.current) {
          audioContextRef.current = new AudioContext();
        }
        const arrayBuffer = await event.data.arrayBuffer();
        const audioBuffer = await audioContextRef.current.decodeAudioData(arrayBuffer);
        const source = audioContextRef.current.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContextRef.current.destination);
        source.onended = () => setSpeaking(false);
        source.start(0);
      }
    };

    wsRef.current.onclose = () => {
      setConnected(false);
      setVoiceState('idle');
      wsRef.current = null;
    };
  }, [tokens, setConnected, setVoiceState, setTranscript, setSpeaking]);

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(event.data);
        }
      };
      
      mediaRecorderRef.current.start(250); // Send chunk every 250ms
      setListening(true);
    } catch (err) {
      console.error('Error accessing microphone', err);
    }
  };

  const stopListening = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    setListening(false);
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
      if (audioContextRef.current) audioContextRef.current.close();
      stopListening();
    };
  }, []);

  return { connectToVoice, startListening, stopListening };
};
