import { apiClient } from "../api/client";
import type { ChatRequestPayload, ChatResponsePayload } from "../types/chat";
 
export async function sendChatMessage(message: string): Promise<ChatResponsePayload> {
  const payload: ChatRequestPayload = { message };
  const { data } = await apiClient.post<ChatResponsePayload>("/api/v1/chat", payload);
  return data;
}
