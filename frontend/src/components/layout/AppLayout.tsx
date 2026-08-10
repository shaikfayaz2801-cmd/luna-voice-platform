import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Sidebar from './Sidebar';
import { Bell, UserCircle } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const AppLayout: React.FC = () => {
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(true);
  const { user } = useAuthStore();

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden text-slate-50">
      <Sidebar isExpanded={isSidebarExpanded} setIsExpanded={setIsSidebarExpanded} />
      
      <div className="flex-1 flex flex-col h-full overflow-hidden relative z-0">
        <header className="h-16 flex items-center justify-between px-6 glass z-10">
          <div className="flex items-center space-x-4">
            {/* Can add breadcrumbs or title here */}
          </div>
          <div className="flex items-center space-x-6">
            <button className="relative p-2 rounded-full hover:bg-white/5 transition-colors group">
              <Bell className="w-5 h-5 text-slate-400 group-hover:text-primary-DEFAULT transition-colors" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-primary-DEFAULT rounded-full shadow-[0_0_8px_rgba(139,92,246,0.8)]"></span>
            </button>
            <div className="flex items-center space-x-3 cursor-pointer p-1.5 pr-3 rounded-full hover:bg-white/5 transition-colors border border-transparent hover:border-white/10">
              {user?.avatar ? (
                <img src={user.avatar} alt="User" className="w-8 h-8 rounded-full border border-white/20" />
              ) : (
                <UserCircle className="w-8 h-8 text-slate-400" />
              )}
              <span className="text-sm font-medium hidden sm:block">{user?.first_name || 'User'}</span>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gradient-to-b from-transparent to-background/50 relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={window.location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
