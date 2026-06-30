import { useCallback, useState } from "react";
 
import { sendChatMessage } from "../services/chatService";
import type { ChatMessage } from "../types/chat";
 
interface UseChatResult {
  messages: ChatMessage[];
  isSending: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
}
 
function createMessage(role: ChatMessage["role"], content: string): ChatMessage {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    role,
    content,
    timestamp: Date.now(),
  };
}
 
export function useChat(): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
 
  const sendMessage = useCallback(async (content: string) => {
    const trimmed = content.trim();
    if (!trimmed) return;
 
    setError(null);
    setMessages((prev) => [...prev, createMessage("user", trimmed)]);
    setIsSending(true);
 
    try {
      const response = await sendChatMessage(trimmed);
      setMessages((prev) => [...prev, createMessage("agent", response.reply)]);
    } catch {
      setError("No se pudo contactar al agente. Verifica que el Backend esté disponible.");
    } finally {
      setIsSending(false);
    }
  }, []);
 
  return { messages, isSending, error, sendMessage };
}
