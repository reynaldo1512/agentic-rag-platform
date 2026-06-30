import { useState } from "react";
import type { FormEvent } from "react";
 
interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}
 
export function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [value, setValue] = useState("");
 
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  }
 
  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3">
      <input
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Escribe un mensaje para el agente…"
        disabled={disabled}
        className="flex-1 rounded-xl border border-white/10 bg-surface px-4 py-3 text-sm text-white placeholder:text-muted disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="rounded-xl bg-accent px-5 py-3 text-sm font-medium text-ink disabled:opacity-40"
      >
        Enviar
      </button>
    </form>
  );
}
