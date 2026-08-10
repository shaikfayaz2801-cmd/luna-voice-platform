import React, { useState } from 'react';
import { User, Mic, Volume2, Shield, Bell, Save } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

const SettingsPage = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState('profile');

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'voice', label: 'Voice & Audio', icon: Mic },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'security', label: 'Security', icon: Shield },
  ];

  return (
    <div className="p-8 max-w-5xl mx-auto h-full flex flex-col">
      <h1 className="text-3xl font-bold text-white mb-8">Settings</h1>

      <div className="flex flex-col md:flex-row gap-8 flex-1">
        {/* Settings Sidebar */}
        <div className="w-full md:w-64 shrink-0 space-y-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                activeTab === tab.id
                  ? 'bg-primary-DEFAULT/20 text-white border border-primary-DEFAULT/30 shadow-[inset_0_0_15px_rgba(139,92,246,0.1)]'
                  : 'text-slate-400 hover:bg-white/5 hover:text-white border border-transparent'
              }`}
            >
              <tab.icon className={`w-5 h-5 ${activeTab === tab.id ? 'text-primary-DEFAULT' : ''}`} />
              <span className="font-medium">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Settings Content */}
        <div className="flex-1 glass rounded-3xl p-8 relative overflow-y-auto">
          {activeTab === 'profile' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-primary-DEFAULT/20 border-2 border-primary-DEFAULT/50 flex items-center justify-center text-3xl font-bold text-white">
                  {user?.first_name?.[0] || 'U'}
                </div>
                <div>
                  <button className="bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-white/10">
                    Change Avatar
                  </button>
                  <p className="text-xs text-slate-400 mt-2">JPG, GIF or PNG. Max size of 2MB.</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300">First Name</label>
                  <input type="text" defaultValue={user?.first_name} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-primary-DEFAULT focus:outline-none transition-colors" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300">Last Name</label>
                  <input type="text" defaultValue={user?.last_name} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-primary-DEFAULT focus:outline-none transition-colors" />
                </div>
                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium text-slate-300">Email Address</label>
                  <input type="email" defaultValue={user?.email} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-primary-DEFAULT focus:outline-none transition-colors" />
                </div>
                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium text-slate-300">Language</label>
                  <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-primary-DEFAULT focus:outline-none transition-colors appearance-none">
                    <option value="en">English</option>
                    <option value="ur">Urdu</option>
                    <option value="te">Telugu</option>
                  </select>
                </div>
              </div>
              
              <div className="pt-4 border-t border-white/10 flex justify-end">
                <button className="bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white px-6 py-2.5 rounded-xl font-medium transition-all shadow-[0_0_15px_rgba(139,92,246,0.3)] flex items-center gap-2">
                  <Save className="w-4 h-4" /> Save Changes
                </button>
              </div>
            </div>
          )}

          {activeTab === 'voice' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-xl font-semibold text-white border-b border-white/10 pb-4">Voice Synthesis</h3>
              
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300">Luna's Voice</label>
                  <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-primary-DEFAULT focus:outline-none transition-colors">
                    <option>Luna (Default, Warm)</option>
                    <option>Nova (Energetic)</option>
                    <option>Echo (Professional)</option>
                  </select>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between">
                    <label className="text-sm font-medium text-slate-300">Speaking Speed</label>
                    <span className="text-sm text-slate-400">1.0x</span>
                  </div>
                  <input type="range" min="0.5" max="2" step="0.1" defaultValue="1" className="w-full accent-primary-DEFAULT h-2 bg-white/10 rounded-lg appearance-none cursor-pointer" />
                </div>
              </div>

              <h3 className="text-xl font-semibold text-white border-b border-white/10 pb-4 mt-8">Input Settings</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5">
                  <div className="flex items-center gap-3">
                    <Volume2 className="w-5 h-5 text-primary-DEFAULT" />
                    <div>
                      <p className="font-medium text-white">Push to Talk</p>
                      <p className="text-sm text-slate-400">Require holding a button to speak</p>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-white/10 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-DEFAULT"></div>
                  </label>
                </div>
              </div>
            </div>
          )}
          
          {/* Add placeholders for other tabs to complete the file */}
          {activeTab === 'notifications' && (
            <div className="text-slate-400">Notification settings coming soon.</div>
          )}
          {activeTab === 'security' && (
            <div className="text-slate-400">Security settings coming soon.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
