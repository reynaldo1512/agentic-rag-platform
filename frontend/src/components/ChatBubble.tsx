import type { ChatMessage } from "../types/chat";
 
interface ChatBubbleProps {
  message: ChatMessage;
}
 
export function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === "user";
 
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={[
          "max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser ? "bg-accent/15 text-white" : "border border-white/5 bg-surface text-white",
        ].join(" ")}
      >
        <p className="mb-1 text-[10px] uppercase tracking-widest text-muted">
          {isUser ? "Tú" : "Agente"}
        </p>
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}
