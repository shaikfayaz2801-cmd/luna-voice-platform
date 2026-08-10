import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, PhoneOff, Settings, Minimize2, Globe } from 'lucide-react';
import { useVoice } from '../hooks/useVoice';
import { useVoiceStore } from '../store/voiceStore';
import clsx from 'clsx';
import { useNavigate } from 'react-router-dom';

const VoicePage = () => {
  const navigate = useNavigate();
  const { connectToVoice, startListening, stopListening } = useVoice();
  const { isConnected, isListening, voiceState, currentTranscript } = useVoiceStore();
  const [isMuted, setIsMuted] = useState(false);

  useEffect(() => {
    connectToVoice();
    return () => {
      stopListening();
    };
  }, [connectToVoice]);

  const toggleListen = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const getRingColor = () => {
    switch (voiceState) {
      case 'listening': return 'border-accent shadow-[0_0_50px_rgba(6,182,212,0.6)]';
      case 'processing': return 'border-yellow-400 shadow-[0_0_50px_rgba(250,204,21,0.4)] border-dashed animate-spin-slow';
      case 'speaking': return 'border-primary-DEFAULT shadow-[0_0_60px_rgba(139,92,246,0.8)] animate-pulse-slow';
      default: return 'border-white/20 shadow-[0_0_20px_rgba(255,255,255,0.1)]';
    }
  };

  const getStatusText = () => {
    switch (voiceState) {
      case 'listening': return 'Listening...';
      case 'processing': return 'Thinking...';
      case 'speaking': return 'Speaking...';
      default: return 'Tap to speak';
    }
  };

  return (
    <div className="absolute inset-0 z-50 bg-background flex flex-col items-center justify-between overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className={clsx(
          "absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full blur-[120px] transition-all duration-1000",
          voiceState === 'listening' ? 'bg-accent/10 scale-110' :
          voiceState === 'speaking' ? 'bg-primary-DEFAULT/20 scale-125' : 'bg-primary-DEFAULT/5 scale-100'
        )} />
      </div>

      {/* Top Bar */}
      <div className="w-full p-6 flex justify-between items-center relative z-10">
        <button onClick={() => navigate(-1)} className="p-3 glass rounded-full hover:bg-white/10 transition-colors text-white">
          <Minimize2 className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2 glass px-4 py-2 rounded-full border-white/5">
          <Globe className="w-4 h-4 text-slate-400" />
          <span className="text-sm font-medium text-slate-200">English (US)</span>
        </div>
        <button className="p-3 glass rounded-full hover:bg-white/10 transition-colors text-white">
          <Settings className="w-5 h-5" />
        </button>
      </div>

      {/* Main Avatar Area */}
      <div className="flex-1 flex flex-col items-center justify-center relative z-10 w-full max-w-2xl px-6">
        
        {/* Status Text */}
        <div className="mb-12 h-8">
          <AnimatePresence mode="wait">
            <motion.p
              key={voiceState}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="text-slate-400 uppercase tracking-[0.2em] text-sm font-medium"
            >
              {getStatusText()}
            </motion.p>
          </AnimatePresence>
        </div>

        {/* Luna Orb */}
        <div className="relative cursor-pointer" onClick={toggleListen}>
          {/* Animated rings based on state */}
          {voiceState === 'speaking' && (
            <>
              <div className="absolute inset-[-40px] rounded-full border border-primary-DEFAULT/30 animate-[ping_2s_ease-out_infinite] pointer-events-none"></div>
              <div className="absolute inset-[-80px] rounded-full border border-primary-DEFAULT/10 animate-[ping_2s_ease-out_infinite_0.5s] pointer-events-none"></div>
            </>
          )}
          
          <motion.div 
            animate={{ 
              scale: voiceState === 'speaking' ? [1, 1.05, 1] : 1,
            }}
            transition={{ repeat: voiceState === 'speaking' ? Infinity : 0, duration: 1 }}
            className={clsx(
              "w-48 h-48 rounded-full flex items-center justify-center border-4 transition-all duration-500 bg-gradient-to-tr from-background to-white/5 backdrop-blur-xl z-10 relative overflow-hidden",
              getRingColor()
            )}
          >
            {/* Inner glow */}
            <div className={clsx(
              "absolute inset-0 opacity-50 transition-all duration-500",
              voiceState === 'listening' ? 'bg-gradient-to-t from-accent/40 to-transparent' :
              voiceState === 'speaking' ? 'bg-gradient-to-t from-primary-DEFAULT/60 to-transparent' : 'bg-transparent'
            )} />
            
            <span className="text-white font-bold text-7xl relative z-20 drop-shadow-[0_0_15px_rgba(255,255,255,0.5)] text-glow">L</span>
          </motion.div>
        </div>

        {/* Transcript */}
        <div className="mt-16 h-24 w-full flex items-center justify-center text-center">
          <p className="text-xl md:text-2xl text-white font-medium max-w-lg leading-relaxed drop-shadow-md">
            {currentTranscript || (voiceState === 'idle' ? "How can I help you today?" : "...")}
          </p>
        </div>
      </div>

      {/* Controls */}
      <div className="w-full pb-12 pt-6 flex justify-center items-center gap-6 relative z-10">
        <button 
          onClick={() => setIsMuted(!isMuted)}
          className={clsx(
            "p-4 rounded-full transition-all border",
            isMuted ? "bg-red-500/20 text-red-400 border-red-500/30" : "glass text-white hover:bg-white/10"
          )}
        >
          {isMuted ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
        </button>
        
        <button 
          onClick={() => navigate(-1)}
          className="p-5 rounded-full bg-red-500 hover:bg-red-600 text-white shadow-[0_0_20px_rgba(239,68,68,0.4)] hover:shadow-[0_0_30px_rgba(239,68,68,0.6)] transition-all"
        >
          <PhoneOff className="w-8 h-8" />
        </button>

        <button className="p-4 rounded-full glass text-white hover:bg-white/10 transition-all border border-white/10">
          <Settings className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
};

export default VoicePage;
