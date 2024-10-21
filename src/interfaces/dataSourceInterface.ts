export interface DataSources {
  id: number | string;
  name: string;
  type: string;
  connection_url?: string;
  table_name?: string;
  created_at: string;
}

export interface FileInfo {
  name: string;
  size: number;
  progress: number;
  status: 'uploading' | 'completed';
}


export interface GetDataSourcesResponse {
  data_sources: DataSources[];
}

export interface UploadSpreadSheetResponse {
  table_name: string,
  rows_processed: number,
  data_source_id: number
}