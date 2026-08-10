import React, { useState } from 'react';
import { Phone, PhoneIncoming, PhoneOutgoing, Clock, Search, MoreVertical, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

const CallsPage = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  
  // Dummy data
  const calls = [
    { id: '1', number: '+1 (555) 012-3456', direction: 'outbound', status: 'completed', duration: '5m 32s', date: 'Today, 2:30 PM' },
    { id: '2', number: '+1 (555) 987-6543', direction: 'inbound', status: 'missed', duration: '0s', date: 'Today, 11:15 AM' },
    { id: '3', number: '+1 (555) 456-7890', direction: 'outbound', status: 'completed', duration: '12m 45s', date: 'Yesterday, 4:20 PM' },
    { id: '4', number: '+1 (555) 111-2222', direction: 'inbound', status: 'completed', duration: '3m 10s', date: 'Oct 24, 9:00 AM' },
  ];

  const handleKeyPress = (digit: string) => {
    setPhoneNumber(prev => prev + digit);
  };

  const handleBackspace = () => {
    setPhoneNumber(prev => prev.slice(0, -1));
  };

  return (
    <div className="p-8 max-w-6xl mx-auto h-full flex flex-col md:flex-row gap-8">
      {/* Dialer Panel */}
      <div className="w-full md:w-80 flex flex-col gap-6 shrink-0">
        <div className="glass p-6 rounded-3xl flex flex-col items-center">
          <h2 className="text-xl font-semibold text-white mb-6">Make a Call</h2>
          
          <div className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 mb-8 text-center min-h-[72px] flex items-center justify-center relative group">
            <span className="text-2xl font-mono text-white tracking-wider">
              {phoneNumber || 'Enter number'}
            </span>
            {phoneNumber && (
              <button 
                onClick={handleBackspace}
                className="absolute right-4 text-slate-400 hover:text-white transition-colors"
              >
                ⌫
              </button>
            )}
          </div>

          <div className="grid grid-cols-3 gap-4 mb-8 w-full max-w-[240px]">
            {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map((digit) => (
              <button
                key={digit}
                onClick={() => handleKeyPress(digit)}
                className="w-16 h-16 rounded-full glass hover:bg-white/10 flex items-center justify-center text-xl text-white font-medium transition-all active:scale-95 mx-auto border-white/5"
              >
                {digit}
              </button>
            ))}
          </div>

          <button 
            disabled={!phoneNumber}
            className={clsx(
              "w-16 h-16 rounded-full flex items-center justify-center transition-all shadow-[0_0_20px_rgba(34,197,94,0.3)]",
              phoneNumber ? "bg-green-500 hover:bg-green-400 hover:scale-105" : "bg-green-500/50 cursor-not-allowed"
            )}
          >
            <Phone className="w-6 h-6 text-white" />
          </button>
        </div>
      </div>

      {/* Call History */}
      <div className="flex-1 glass rounded-3xl p-6 flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-white">Call History</h2>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search calls..." 
              className="bg-white/5 border border-white/10 rounded-xl py-2 pl-9 pr-4 text-sm text-white focus:outline-none focus:border-primary-DEFAULT transition-colors w-64"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto space-y-2 pr-2">
          {calls.map((call, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              key={call.id}
              className="flex items-center justify-between p-4 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer group border border-transparent hover:border-white/5"
            >
              <div className="flex items-center gap-4">
                <div className={clsx(
                  "w-12 h-12 rounded-full flex items-center justify-center",
                  call.status === 'missed' ? "bg-red-500/20 text-red-400" :
                  call.direction === 'inbound' ? "bg-blue-500/20 text-blue-400" : "bg-green-500/20 text-green-400"
                )}>
                  {call.direction === 'inbound' ? <PhoneIncoming className="w-5 h-5" /> : <PhoneOutgoing className="w-5 h-5" />}
                </div>
                <div>
                  <h3 className="font-medium text-white text-lg">{call.number}</h3>
                  <div className="flex items-center gap-3 text-sm text-slate-400 mt-1">
                    <span className="flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> {call.date}</span>
                    {call.status !== 'missed' && (
                      <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {call.duration}</span>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                <span className={clsx(
                  "px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wider",
                  call.status === 'completed' ? "bg-green-500/10 text-green-400 border border-green-500/20" : 
                  "bg-red-500/10 text-red-400 border border-red-500/20"
                )}>
                  {call.status}
                </span>
                <button className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors opacity-0 group-hover:opacity-100">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CallsPage;
