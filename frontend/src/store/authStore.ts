import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthTokens } from '../types';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  login: (tokens: AuthTokens, user: User) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      login: (tokens, user) => set({ tokens, user, isAuthenticated: true }),
      logout: () => set({ user: null, tokens: null, isAuthenticated: false }),
      updateUser: (updatedUser) => set((state) => ({ 
        user: state.user ? { ...state.user, ...updatedUser } : null 
      })),
    }),
    {
      name: 'luna-auth',
    }
  )
);
