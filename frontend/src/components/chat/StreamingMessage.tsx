import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface StreamingMessageProps {
  content: string;
  isStreaming: boolean;
  speed?: number; // ms per character
}

const StreamingMessage: React.FC<StreamingMessageProps> = ({
  content,
  isStreaming,
  speed = 12,
}) => {
  const [displayed, setDisplayed] = useState('');
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    if (!isStreaming) {
      setDisplayed(content);
      return;
    }

    if (charIndex < content.length) {
      const timer = setTimeout(() => {
        setDisplayed(content.slice(0, charIndex + 1));
        setCharIndex((prev) => prev + 1);
      }, speed);
      return () => clearTimeout(timer);
    }
  }, [content, charIndex, isStreaming, speed]);

  // Reset when new streaming starts
  useEffect(() => {
    if (isStreaming && content.length === 0) {
      setDisplayed('');
      setCharIndex(0);
    }
  }, [isStreaming, content.length]);

  // If not streaming, just show content immediately
  useEffect(() => {
    if (!isStreaming) {
      setDisplayed(content);
      setCharIndex(content.length);
    }
  }, [isStreaming, content]);

  const showCursor = isStreaming && charIndex <= content.length;

  return (
    <span className="whitespace-pre-wrap break-words leading-relaxed">
      {displayed}
      {showCursor && (
        <motion.span
          className="inline-block w-0.5 h-4 bg-violet-400 ml-0.5 align-middle"
          animate={{ opacity: [1, 0, 1] }}
          transition={{ duration: 0.7, repeat: Infinity, ease: 'steps(1)' }}
        />
      )}
    </span>
  );
};

export default StreamingMessage;
