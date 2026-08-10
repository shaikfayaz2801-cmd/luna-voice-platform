import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import AppLayout from '../components/layout/AppLayout';
import AuthPage from '../pages/AuthPage';
import DashboardPage from '../pages/DashboardPage';
import ChatPage from '../pages/ChatPage';
import VoicePage from '../pages/VoicePage';
import MemoryPage from '../pages/MemoryPage';
import CallsPage from '../pages/CallsPage';
import SettingsPage from '../pages/SettingsPage';
import AdminPage from '../pages/AdminPage';
import ResetPasswordPage from '../pages/ResetPasswordPage';

const ProtectedRoute = ({ children, requireAdmin = false }: { children: JSX.Element, requireAdmin?: boolean }) => {
  const { isAuthenticated, user } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  if (requireAdmin && user?.role !== 'admin') {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

export const router = createBrowserRouter([
  {
    path: '/auth',
    element: <AuthPage />,
  },
  {
    path: '/auth/reset-password',
    element: <ResetPasswordPage />,
  },
  {
    path: '/',
    element: <ProtectedRoute><AppLayout /></ProtectedRoute>,
    children: [
      { path: '/', element: <DashboardPage /> },
      { path: '/chat', element: <ChatPage /> },
      { path: '/chat/:conversationId', element: <ChatPage /> },
      { path: '/voice', element: <VoicePage /> },
      { path: '/memory', element: <MemoryPage /> },
      { path: '/calls', element: <CallsPage /> },
      { path: '/settings', element: <SettingsPage /> },
      { 
        path: '/admin', 
        element: <ProtectedRoute requireAdmin><AdminPage /></ProtectedRoute> 
      },
    ],
  },
]);
