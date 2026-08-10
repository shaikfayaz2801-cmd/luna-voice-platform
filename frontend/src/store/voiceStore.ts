import { create } from 'zustand';

type VoiceState = 'idle' | 'listening' | 'processing' | 'speaking';

interface VoiceStoreState {
  isConnected: boolean;
  isListening: boolean;
  isSpeaking: boolean;
  currentTranscript: string;
  voiceState: VoiceState;
  
  setConnected: (connected: boolean) => void;
  setListening: (listening: boolean) => void;
  setSpeaking: (speaking: boolean) => void;
  setTranscript: (transcript: string) => void;
  setVoiceState: (state: VoiceState) => void;
}

export const useVoiceStore = create<VoiceStoreState>((set) => ({
  isConnected: false,
  isListening: false,
  isSpeaking: false,
  currentTranscript: '',
  voiceState: 'idle',
  
  setConnected: (connected) => set({ isConnected: connected }),
  setListening: (listening) => set({ 
    isListening: listening,
    voiceState: listening ? 'listening' : 'idle'
  }),
  setSpeaking: (speaking) => set({ 
    isSpeaking: speaking,
    voiceState: speaking ? 'speaking' : 'idle'
  }),
  setTranscript: (transcript) => set({ currentTranscript: transcript }),
  setVoiceState: (state) => set({ voiceState: state }),
}));
