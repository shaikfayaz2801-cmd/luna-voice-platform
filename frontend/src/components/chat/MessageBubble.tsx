import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/atom-one-dark.css';
import { Message } from '../../types';
import clsx from 'clsx';
import { format } from 'date-fns';

interface MessageBubbleProps {
  message: Message;
  isLast?: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isLast }) => {
  const isUser = message.role === 'user';

  return (
    <div className={clsx("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div className={clsx("flex gap-4 max-w-[85%]", isUser ? "flex-row-reverse" : "flex-row")}>
        
        {/* Avatar */}
        <div className="shrink-0 mt-auto mb-1">
          {isUser ? (
            <div className="w-8 h-8 rounded-full bg-white/10 border border-white/20 flex items-center justify-center">
              <span className="text-xs text-white">U</span>
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center shadow-[0_0_10px_rgba(139,92,246,0.3)]">
              <span className="text-white font-bold text-xs">L</span>
            </div>
          )}
        </div>

        {/* Bubble */}
        <div className={clsx(
          "flex flex-col gap-1",
          isUser ? "items-end" : "items-start"
        )}>
          <div className={clsx(
            "px-5 py-3.5 relative",
            isUser 
              ? "bg-gradient-to-br from-primary-DEFAULT to-indigo-600 text-white rounded-2xl rounded-br-sm shadow-[0_4px_20px_rgba(139,92,246,0.15)]" 
              : "glass text-slate-100 rounded-2xl rounded-bl-sm border border-white/5"
          )}>
            {isUser ? (
              <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
            ) : (
              <div className="prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-black/40 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-xl">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeHighlight]}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>
          
          {/* Metadata */}
          <div className="flex items-center gap-2 px-1">
            <span className="text-[10px] text-slate-500">
              {format(new Date(message.created_at || new Date()), 'h:mm a')}
            </span>
            {!isUser && message.tokens_used && (
              <span className="text-[10px] text-slate-600 bg-white/5 px-1.5 py-0.5 rounded">
                {message.tokens_used} tokens
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
