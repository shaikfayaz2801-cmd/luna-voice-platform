import { useMutation } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useAuthStore } from '../store/authStore';
import { AuthTokens, User } from '../types';

export const useAuth = () => {
  const { login, logout, user, isAuthenticated } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: async (credentials: any) => {
      const response = await api.post<{ tokens: AuthTokens; user: User }>('/auth/login', credentials);
      return response.data;
    },
    onSuccess: (data) => {
      login(data.tokens, data.user);
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (userData: any) => {
      const response = await api.post<{ tokens: AuthTokens; user: User }>('/auth/register', userData);
      return response.data;
    },
    onSuccess: (data) => {
      login(data.tokens, data.user);
    },
  });

  return {
    user,
    isAuthenticated,
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout,
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
  };
};
