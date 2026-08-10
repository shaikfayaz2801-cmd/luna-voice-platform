export interface User { 
  id: string; 
  email: string; 
  username: string; 
  first_name: string; 
  last_name: string; 
  avatar?: string; 
  language: 'en'|'ur'|'te'; 
  role?: string;
}

export interface AuthTokens { 
  access: string; 
  refresh: string; 
}

export interface Conversation { 
  id: string; 
  title: string; 
  created_at: string; 
  updated_at: string; 
  is_archived: boolean; 
  message_count: number; 
}

export interface Message { 
  id: string; 
  role: 'user'|'assistant'|'system'; 
  content: string; 
  created_at: string; 
  tokens_used?: number; 
}

export interface Memory { 
  id: string; 
  content: string; 
  memory_type: 'preference'|'goal'|'event'|'fact'; 
  importance: number; 
  created_at: string; 
}

export interface Call { 
  id: string; 
  direction: 'inbound'|'outbound'; 
  phone_number: string; 
  status: string; 
  started_at: string; 
  duration?: number; 
}

export interface CallLog { 
  id: string; 
  speaker: 'user'|'ai'; 
  text: string; 
  timestamp: string; 
}

export interface Personality { 
  id: string; 
  name: string; 
  description: string; 
  traits: Record<string, string>; 
}

export interface VoiceSettings { 
  tts_provider: string; 
  tts_voice_id: string; 
  stt_provider: string; 
  language: string; 
}

export interface Notification { 
  id: string; 
  title: string; 
  body: string; 
  notification_type: string; 
  is_read: boolean; 
  created_at: string; 
}
