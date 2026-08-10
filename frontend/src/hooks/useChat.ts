import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { Conversation, Message } from '../types';

export const useChat = (conversationId?: string) => {
  const queryClient = useQueryClient();

  const conversationsQuery = useQuery({
    queryKey: ['conversations'],
    queryFn: async () => {
      const { data } = await api.get<Conversation[]>('/chat/conversations');
      return data;
    },
  });

  const messagesQuery = useQuery({
    queryKey: ['messages', conversationId],
    queryFn: async () => {
      if (!conversationId) return [];
      const { data } = await api.get<Message[]>(`/chat/conversations/${conversationId}/messages`);
      return data;
    },
    enabled: !!conversationId,
  });

  const sendMessageMutation = useMutation({
    mutationFn: async (content: string) => {
      const { data } = await api.post(`/chat/conversations/${conversationId}/messages`, { content });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['messages', conversationId] });
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });

  // Note: Streaming SSE logic would usually go here or in a dedicated component.
  // For simplicity, we expose a standard mutation, and streaming will be handled in the UI
  // using native EventSource or fetch API to update optimistic state.

  return {
    conversations: conversationsQuery.data || [],
    isLoadingConversations: conversationsQuery.isLoading,
    messages: messagesQuery.data || [],
    isLoadingMessages: messagesQuery.isLoading,
    sendMessage: sendMessageMutation.mutateAsync,
    isSending: sendMessageMutation.isPending,
  };
};
