import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Plus, BrainCircuit, Star, Trash2, Edit2, Calendar } from 'lucide-react';

const MemoryPage = () => {
  const [activeTab, setActiveTab] = useState('all');

  const tabs = [
    { id: 'all', label: 'All Memories' },
    { id: 'preference', label: 'Preferences' },
    { id: 'goal', label: 'Goals' },
    { id: 'event', label: 'Events' },
    { id: 'fact', label: 'Facts' },
  ];

  // Dummy data
  const memories = [
    { id: '1', content: 'User prefers dark mode interfaces.', type: 'preference', importance: 8, date: '2023-10-24' },
    { id: '2', content: 'Wants to learn conversational Spanish by end of year.', type: 'goal', importance: 9, date: '2023-10-20' },
    { id: '3', content: 'Has a meeting with Sarah on Friday at 3 PM.', type: 'event', importance: 5, date: '2023-10-25' },
    { id: '4', content: 'Allergic to peanuts.', type: 'fact', importance: 10, date: '2023-09-15' },
  ];

  const getTypeColor = (type: string) => {
    switch(type) {
      case 'preference': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'goal': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      case 'event': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'fact': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const filteredMemories = activeTab === 'all' ? memories : memories.filter(m => m.type === activeTab);

  return (
    <div className="p-8 max-w-6xl mx-auto h-full flex flex-col">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <BrainCircuit className="w-8 h-8 text-primary-DEFAULT" />
            Core Memory
          </h1>
          <p className="text-slate-400 mt-2">Everything Luna knows about you.</p>
        </div>
        <button className="bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white px-4 py-2 rounded-xl flex items-center gap-2 shadow-[0_0_15px_rgba(139,92,246,0.3)] transition-all shrink-0">
          <Plus className="w-5 h-5" /> Add Memory
        </button>
      </div>

      {/* Search & Filter */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search memories syntactically or semantically..." 
            className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white focus:outline-none focus:border-primary-DEFAULT transition-colors"
          />
        </div>
        <button className="glass px-4 py-3 rounded-xl flex items-center gap-2 text-slate-300 hover:text-white transition-colors">
          <Filter className="w-5 h-5" /> Filter
        </button>
      </div>

      {/* Tabs */}
      <div className="flex overflow-x-auto pb-2 mb-6 gap-2 hide-scrollbar">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-full whitespace-nowrap transition-colors text-sm font-medium ${
              activeTab === tab.id 
                ? 'bg-primary-DEFAULT text-white' 
                : 'bg-white/5 text-slate-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Memory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 overflow-y-auto pb-8">
        {filteredMemories.map((memory, i) => (
          <motion.div
            key={memory.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            className="glass rounded-2xl p-6 group relative hover:border-white/20 transition-all"
          >
            <div className="flex justify-between items-start mb-4">
              <span className={`text-xs px-2.5 py-1 rounded-full border ${getTypeColor(memory.type)} uppercase tracking-wider font-semibold`}>
                {memory.type}
              </span>
              <div className="flex items-center gap-1 bg-white/5 px-2 py-1 rounded-full text-amber-400 text-xs">
                <Star className="w-3 h-3 fill-amber-400" /> {memory.importance}/10
              </div>
            </div>
            
            <p className="text-white text-lg mb-6 leading-relaxed">
              "{memory.content}"
            </p>
            
            <div className="flex items-center justify-between border-t border-white/5 pt-4 mt-auto">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Calendar className="w-3.5 h-3.5" />
                {memory.date}
              </div>
              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button className="p-1.5 rounded-lg hover:bg-white/10 text-slate-400 hover:text-white transition-colors">
                  <Edit2 className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {filteredMemories.length === 0 && (
        <div className="flex-1 flex flex-col items-center justify-center text-center">
          <BrainCircuit className="w-16 h-16 text-slate-600 mb-4" />
          <h3 className="text-xl font-medium text-white mb-2">No memories found</h3>
          <p className="text-slate-400 max-w-sm">Luna hasn't stored any memories of this type yet. Chat with Luna to build your core memory.</p>
        </div>
      )}
    </div>
  );
};

export default MemoryPage;
