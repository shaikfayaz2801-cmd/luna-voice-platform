import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Bell, CheckCheck, Trash2 } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { formatDistanceToNow } from 'date-fns';
import { api } from '../../lib/api';
import { Notification } from '../../types';
import Badge from '../common/Badge';

interface NotificationPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const NotificationPanel: React.FC<NotificationPanelProps> = ({ isOpen, onClose }) => {
  const queryClient = useQueryClient();

  const { data: notifications = [] } = useQuery<Notification[]>({
    queryKey: ['notifications'],
    queryFn: () => api.get('/notifications/').then((r) => r.data.results ?? r.data),
    enabled: isOpen,
  });

  const markAllRead = useMutation({
    mutationFn: () => api.post('/notifications/mark-all-read/'),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notifications'] }),
  });

  const deleteNotification = useMutation({
    mutationFn: (id: string) => api.delete(`/notifications/${id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notifications'] }),
  });

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="fixed inset-0 z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="fixed right-4 top-16 z-50 w-80 rounded-2xl border border-white/10 bg-[#12121f]/95 backdrop-blur-xl shadow-2xl overflow-hidden"
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ type: 'spring', damping: 25, stiffness: 350 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <Bell size={16} className="text-violet-400" />
                <span className="font-semibold text-white text-sm">Notifications</span>
                {unreadCount > 0 && (
                  <Badge variant="purple" size="sm">{unreadCount}</Badge>
                )}
              </div>
              <div className="flex items-center gap-1">
                {unreadCount > 0 && (
                  <button
                    onClick={() => markAllRead.mutate()}
                    className="p-1.5 text-slate-400 hover:text-cyan-400 transition-colors"
                    title="Mark all read"
                  >
                    <CheckCheck size={14} />
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="p-1.5 text-slate-400 hover:text-white transition-colors"
                >
                  <X size={14} />
                </button>
              </div>
            </div>

            {/* List */}
            <div className="max-h-80 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-slate-500">
                  <Bell size={28} className="mb-2 opacity-40" />
                  <p className="text-sm">No notifications yet</p>
                </div>
              ) : (
                notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`flex items-start gap-3 px-4 py-3 border-b border-white/5 hover:bg-white/5 transition-colors group ${
                      !n.is_read ? 'bg-violet-500/5' : ''
                    }`}
                  >
                    {!n.is_read && (
                      <div className="mt-1.5 w-2 h-2 rounded-full bg-violet-400 flex-shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white truncate">{n.title}</p>
                      <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{n.body}</p>
                      <p className="text-xs text-slate-600 mt-1">
                        {formatDistanceToNow(new Date(n.created_at), { addSuffix: true })}
                      </p>
                    </div>
                    <button
                      onClick={() => deleteNotification.mutate(n.id)}
                      className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-red-400 transition-all flex-shrink-0"
                    >
                      <Trash2 size={12} />
                    </button>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default NotificationPanel;
