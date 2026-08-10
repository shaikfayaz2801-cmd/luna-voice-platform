import React from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, PhoneCall, BrainCircuit, Activity, ArrowRight, Play } from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { Link, useNavigate } from 'react-router-dom';

const DashboardPage = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const greeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  const stats = [
    { label: 'Conversations', value: '24', icon: MessageSquare, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Voice Calls', value: '12', icon: PhoneCall, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Memories', value: '148', icon: BrainCircuit, color: 'text-purple-400', bg: 'bg-purple-400/10' },
    { label: 'Avg Mood', value: 'Happy', icon: Activity, color: 'text-amber-400', bg: 'bg-amber-400/10' },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Welcome Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-8 relative overflow-hidden flex flex-col md:flex-row items-center justify-between border-primary-DEFAULT/20"
      >
        <div className="absolute -right-20 -top-20 w-64 h-64 bg-primary-DEFAULT/20 rounded-full blur-[100px]" />
        <div className="relative z-10 flex-1 mb-6 md:mb-0">
          <h1 className="text-4xl font-bold mb-2 text-white">
            {greeting()}, <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-DEFAULT to-accent">{user?.first_name || 'User'}</span>!
          </h1>
          <p className="text-slate-400 text-lg">Luna is ready to assist you today. What would you like to do?</p>
          
          <div className="flex gap-4 mt-6">
            <button onClick={() => navigate('/chat')} className="bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_25px_rgba(139,92,246,0.5)] flex items-center gap-2">
              <MessageSquare className="w-5 h-5" /> Start Chat
            </button>
            <button onClick={() => navigate('/voice')} className="bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 border border-white/10">
              <PhoneCall className="w-5 h-5" /> Voice Call
            </button>
          </div>
        </div>
        
        <div className="relative z-10 hidden md:block">
          <div className="relative">
            <div className="w-32 h-32 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center border-4 border-background animate-float">
              <span className="text-white font-bold text-5xl">L</span>
            </div>
            <div className="absolute inset-0 rounded-full border border-white/20 animate-ping opacity-20"></div>
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass p-6 rounded-2xl flex items-center gap-4 hover:bg-white-[0.07] transition-colors"
          >
            <div className={`p-4 rounded-xl ${stat.bg} ${stat.color}`}>
              <stat.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400">{stat.label}</p>
              <p className="text-2xl font-bold text-white">{stat.value}</p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activity */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2 glass rounded-2xl p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Recent Conversations</h2>
            <Link to="/chat" className="text-sm text-primary-DEFAULT hover:text-white transition-colors flex items-center gap-1">
              View all <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="space-y-4">
            {[1, 2, 3].map((_, i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer group">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary-DEFAULT/20 flex items-center justify-center text-primary-DEFAULT">
                    <MessageSquare className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-medium text-white group-hover:text-primary-DEFAULT transition-colors">Planning for weekend trip</h3>
                    <p className="text-sm text-slate-400">Today at 2:30 PM</p>
                  </div>
                </div>
                <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <Play className="w-4 h-4 text-white" />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Luna's State */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass rounded-2xl p-6 flex flex-col"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Luna Status</h2>
          <div className="flex-1 flex flex-col items-center justify-center space-y-6">
            <div className="relative">
              <div className="w-24 h-24 rounded-full border-4 border-primary-DEFAULT border-t-transparent animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <BrainCircuit className="w-8 h-8 text-primary-DEFAULT" />
              </div>
            </div>
            <div className="text-center space-y-2">
              <p className="text-lg font-medium text-white">System Online</p>
              <p className="text-sm text-slate-400">All neural pathways active.</p>
              <div className="flex items-center justify-center gap-2 mt-2">
                <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]"></span>
                <span className="text-xs text-slate-400 uppercase tracking-wider">Ready</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default DashboardPage;
