import { useEffect, useRef } from "react";
 
import { ChatBubble } from "../components/ChatBubble";
import { ChatInput } from "../components/ChatInput";
import { TypingIndicator } from "../components/TypingIndicator";
import { useChat } from "../utils/useChat";
 
export function Agent() {
  const { messages, isSending, error, sendMessage } = useChat();
  const scrollRef = useRef<HTMLDivElement>(null);
 
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);
 
  return (
    <main className="flex h-screen flex-col px-8 py-6">
      <header className="mb-4">
        <h1 className="text-2xl font-semibold">Chat con el agente</h1>
      </header>
 
      <div className="flex-1 space-y-4 overflow-y-auto rounded-2xl border border-white/5 bg-ink/40 p-6">
        {messages.length === 0 && (
          <p className="text-center text-sm text-muted">
            Envía un mensaje para iniciar la conversación.
          </p>
        )}
 
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
 
        {isSending && <TypingIndicator />}
 
        <div ref={scrollRef} />
      </div>
 
      {error && <p className="mt-3 text-sm text-danger">{error}</p>}
 
      <div className="mt-4">
        <ChatInput onSend={sendMessage} disabled={isSending} />
      </div>
    </main>
  );
}
