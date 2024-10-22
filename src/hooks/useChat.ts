/* eslint-disable @typescript-eslint/no-explicit-any */

// import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ChatRequestBody, InitiateConversationRequestBody, InitiateConversationResponse } from "../interfaces/chatInterface";
import { AxiosError } from 'axios';
import {ApiResponse} from "../interfaces/globalInterfaces";
import { askQuestion, initiateConversation } from '../zustand/apis/chatApi';
import { toast } from 'react-toastify';
import { parseData } from '../utils/utils';

interface ErrorResponse {
    [key: string]: any; 
}
interface UseStreamChatOptions {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
  onStreamData?: (chunk: any) => void;
}

  export const useInitiateConversationMutation = (
    onInitiated?: (conversation_id: number) => void,
    onFailed?: () => void
  ) => {
    return useMutation<ApiResponse<InitiateConversationResponse>, AxiosError<ErrorResponse>, InitiateConversationRequestBody>({
        mutationFn: initiateConversation,
        onSuccess: (response) => {
          console.log(response.data.conversaction_id);
          onInitiated?.(response.data.conversaction_id)
        },
        onError: (error) => {
          onFailed?.()
          console.log(error.response?.data);
          toast.error(error.response?.data.message)
        },
    })
}

export const useStreamChat = (options?: UseStreamChatOptions) => {
  return useMutation<Response, Error, ChatRequestBody>({
    mutationFn: (requestData: ChatRequestBody) => {
      return askQuestion(
        requestData,
        (chunks: any) => {
          const parsedChunk = parseData(chunks);
          console.log('Received chunks:', String(chunks));
          console.log(parsedChunk);
            options?.onStreamData?.(parsedChunk);
        }
      );
    },
    onSuccess: (data) => {
      console.log('Stream data:', data);
      options?.onSuccess?.();
    },
    onError: (error) => {
      console.error('Stream error:', error);
      options?.onError?.(error);
    },
  });
};