
export interface ChatRequestBody {
  question: string;
  type: "url" | "spreadsheet" | string;
  conversaction_id: number;
  dataset_id: number;
  selected_tables: string[];

}

export type StreamCallback = (chunk: string) => void;

export interface StreamConfig {
  onChunk: StreamCallback;
  signal?: AbortSignal;
}

export interface InitiateConversationRequestBody {
  data_source_id: number;
}

export interface InitiateConversationResponse {
  conversaction_id: number;
  conversaction_title: string;
  data_source_id: number;
}
