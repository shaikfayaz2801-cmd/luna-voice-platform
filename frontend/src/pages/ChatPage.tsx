import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Mic, Paperclip, MoreVertical, Search, Plus, Archive, Trash2 } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import MessageBubble from '../components/chat/MessageBubble';
import { useNavigate, useParams } from 'react-router-dom';

const ChatPage = () => {
  const { conversationId } = useParams();
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const { conversations, messages, sendMessage, isSending } = useChat(conversationId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isSending) return;
    
    const content = input;
    setInput('');
    // Ideally this creates a conversation if none exists, then sends
    await sendMessage(content);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex h-full w-full relative">
      {/* Sidebar - Conversation List */}
      <div className="w-80 border-r border-white/10 glass flex flex-col z-10 hidden lg:flex">
        <div className="p-4 border-b border-white/5 space-y-4">
          <button 
            onClick={() => navigate('/chat')}
            className="w-full flex items-center justify-center gap-2 bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white py-2.5 rounded-xl transition-all shadow-[0_0_15px_rgba(139,92,246,0.3)]"
          >
            <Plus className="w-5 h-5" /> New Chat
          </button>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search conversations..." 
              className="w-full bg-white/5 border border-white/10 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-primary-DEFAULT transition-colors"
            />
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.map((conv) => (
            <div 
              key={conv.id}
              onClick={() => navigate(`/chat/${conv.id}`)}
              className={`p-3 rounded-xl cursor-pointer transition-colors ${
                conv.id === conversationId ? 'bg-white/10 border border-white/5' : 'hover:bg-white/5 border border-transparent'
              }`}
            >
              <h3 className="text-sm font-medium text-white truncate">{conv.title}</h3>
              <p className="text-xs text-slate-400 mt-1 flex justify-between">
                <span>{new Date(conv.updated_at).toLocaleDateString()}</span>
                <span>{conv.message_count} msgs</span>
              </p>
            </div>
          ))}
          {conversations.length === 0 && (
            <div className="text-center p-4 text-slate-500 text-sm">No conversations yet.</div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full bg-background relative z-0">
        {/* Header */}
        <div className="h-16 border-b border-white/10 glass flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center shadow-[0_0_10px_rgba(139,92,246,0.5)]">
              <span className="text-white font-bold text-sm">L</span>
            </div>
            <div>
              <h2 className="text-white font-medium">{conversations.find(c => c.id === conversationId)?.title || 'New Conversation'}</h2>
              <p className="text-xs text-slate-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span> Online
              </p>
            </div>
          </div>
          {conversationId && (
            <div className="flex items-center gap-2">
              <button className="p-2 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                <Archive className="w-5 h-5" />
              </button>
              <button className="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors">
                <Trash2 className="w-5 h-5" />
              </button>
              <button className="p-2 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                <MoreVertical className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto">
              <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center mb-6 animate-float shadow-[0_0_30px_rgba(139,92,246,0.3)]">
                <span className="text-white font-bold text-3xl">L</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Hello! I'm Luna.</h3>
              <p className="text-slate-400 mb-8">I'm your AI companion. How can I help you today?</p>
              
              <div className="grid grid-cols-2 gap-3 w-full">
                {['Plan a trip', 'Draft an email', 'Practice Spanish', 'Tell me a joke'].map((suggestion) => (
                  <button 
                    key={suggestion}
                    onClick={() => setInput(suggestion)}
                    className="p-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-sm text-slate-300 transition-colors text-left"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <motion.div 
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <MessageBubble message={msg} isLast={i === messages.length - 1} />
              </motion.div>
            ))
          )}
          {isSending && (
            <div className="flex items-start gap-4">
               <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center shrink-0">
                <span className="text-white font-bold text-xs">L</span>
              </div>
              <div className="glass p-4 rounded-2xl rounded-tl-sm w-16 h-12 flex items-center justify-center">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary-DEFAULT rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                  <div className="w-2 h-2 bg-primary-DEFAULT rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-primary-DEFAULT rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-background border-t border-white/5 z-10 relative">
          <div className="max-w-4xl mx-auto relative flex items-end gap-2 bg-white/5 border border-white/10 rounded-2xl p-2 focus-within:border-primary-DEFAULT/50 focus-within:bg-white/[0.07] transition-all">
            <button className="p-2 text-slate-400 hover:text-white transition-colors shrink-0 mb-1">
              <Paperclip className="w-5 h-5" />
            </button>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message Luna..."
              className="w-full max-h-48 min-h-[44px] bg-transparent text-white placeholder-slate-500 resize-none py-2.5 px-2 focus:outline-none scrollbar-thin"
              rows={1}
              style={{ fieldSizing: 'content' } as any}
            />
            <div className="flex gap-2 mb-1 shrink-0">
              <button 
                type="button"
                onClick={() => navigate('/voice')}
                className="p-2 text-slate-400 hover:text-accent transition-colors"
                title="Voice Mode"
              >
                <Mic className="w-5 h-5" />
              </button>
              <button 
                onClick={handleSend}
                disabled={!input.trim() || isSending}
                className={`p-2 rounded-xl flex items-center justify-center transition-all ${
                  input.trim() && !isSending
                    ? 'bg-primary-DEFAULT text-white shadow-[0_0_10px_rgba(139,92,246,0.5)]' 
                    : 'bg-white/10 text-slate-500'
                }`}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
          <div className="text-center mt-2">
            <p className="text-[10px] text-slate-500">Luna can make mistakes. Consider verifying important information.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
