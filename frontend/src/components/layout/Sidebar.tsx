import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MessageSquare, Mic, PhoneCall, BrainCircuit, Settings, LogOut, ShieldAlert, ChevronLeft, ChevronRight } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import clsx from 'clsx';

interface SidebarProps {
  isExpanded: boolean;
  setIsExpanded: (expanded: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isExpanded, setIsExpanded }) => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const navItems = [
    { name: 'Chat', icon: MessageSquare, path: '/chat' },
    { name: 'Voice', icon: Mic, path: '/voice' },
    { name: 'Calls', icon: PhoneCall, path: '/calls' },
    { name: 'Memory', icon: BrainCircuit, path: '/memory' },
    { name: 'Settings', icon: Settings, path: '/settings' },
  ];

  if (user?.role === 'admin') {
    navItems.push({ name: 'Admin', icon: ShieldAlert, path: '/admin' });
  }

  return (
    <motion.aside
      initial={false}
      animate={{ width: isExpanded ? 240 : 80 }}
      className="h-full glass flex flex-col border-r border-white/10 relative z-20 flex-shrink-0"
    >
      <div className="h-20 flex items-center justify-center relative border-b border-white/5">
        <NavLink to="/" className="flex items-center space-x-3 group outline-none">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.5)] group-hover:shadow-[0_0_25px_rgba(139,92,246,0.8)] transition-all duration-300">
              <span className="text-white font-bold text-xl">L</span>
            </div>
            <div className="absolute inset-0 rounded-full border-2 border-white/20 animate-pulse-slow"></div>
          </div>
          {isExpanded && (
            <motion.span 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xl font-bold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400"
            >
              Luna
            </motion.span>
          )}
        </NavLink>
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-primary-DEFAULT border border-white/20 flex items-center justify-center hover:scale-110 transition-transform shadow-[0_0_10px_rgba(139,92,246,0.5)]"
        >
          {isExpanded ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>
      </div>

      <div className="flex-1 py-6 flex flex-col gap-2 overflow-y-auto overflow-x-hidden px-3">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => clsx(
              "flex items-center px-3 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
              isActive 
                ? "bg-primary-DEFAULT/20 text-white shadow-[inset_0_0_20px_rgba(139,92,246,0.2)]" 
                : "text-slate-400 hover:text-white hover:bg-white/5"
            )}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-primary-DEFAULT" />
                )}
                <item.icon className={clsx("w-6 h-6 flex-shrink-0 transition-colors duration-200", isActive ? "text-primary-DEFAULT drop-shadow-[0_0_8px_rgba(139,92,246,0.8)]" : "group-hover:text-primary-DEFAULT")} />
                {isExpanded && (
                  <motion.span 
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="ml-4 font-medium whitespace-nowrap"
                  >
                    {item.name}
                  </motion.span>
                )}
                {!isExpanded && (
                  <div className="absolute left-14 px-2 py-1 bg-surface border border-white/10 rounded text-xs opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-50">
                    {item.name}
                  </div>
                )}
              </>
            )}
          </NavLink>
        ))}
      </div>

      <div className="p-4 border-t border-white/5">
        <button 
          onClick={handleLogout}
          className="w-full flex items-center px-3 py-3 rounded-xl text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors group"
        >
          <LogOut className="w-6 h-6 flex-shrink-0 group-hover:drop-shadow-[0_0_8px_rgba(248,113,113,0.8)]" />
          {isExpanded && <span className="ml-4 font-medium whitespace-nowrap">Logout</span>}
        </button>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
