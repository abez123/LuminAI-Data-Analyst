import { CHAT_ENDPOINTS } from './endPoints';
import { post, postStream } from './apiClient';
import {
    InitiateConversationRequestBody,
    InitiateConversationResponse,
    ChatRequestBody
} from '../../interfaces/chatInterface';
import { ApiResponse } from '../../interfaces/globalInterfaces';

type ApiFunction<TInput, TOutput> = (data: TInput) => Promise<ApiResponse<TOutput>>;

export const initiateConversation:ApiFunction<InitiateConversationRequestBody, InitiateConversationResponse> = async (data) => {
    return await post(CHAT_ENDPOINTS.INITIATE_CONVERSATION, data);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const askQuestion= async (data: ChatRequestBody,onDataChunk:any): Promise<Response> => {
    return await postStream(CHAT_ENDPOINTS.ASK_QUESTION, data,onDataChunk);
  };