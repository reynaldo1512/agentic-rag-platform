export interface ChatRequestPayload {
  message: string;
}
 
export interface ChatResponsePayload {
  reply: string;
  received_message: string;
}
 
export type ChatRole = "user" | "agent";
 
export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  timestamp: number;
}
