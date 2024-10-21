import { DATA_SOURCE_ENDPOINTS } from './endPoints';
import { get, post } from './apiClient';
import {
  GetDataSourcesResponse,
  UploadSpreadSheetResponse,
} from '../../interfaces/dataSourceInterface';
import { ApiResponse } from '../../interfaces/globalInterfaces';

type ApiFunction<TInput, TOutput> = (data: TInput) => Promise<ApiResponse<TOutput>>;

export const uploadSpreadsheet:ApiFunction<File, UploadSpreadSheetResponse> = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('table_name', file.name.split('.')[0]);
    return await post(DATA_SOURCE_ENDPOINTS.UPLOAD_SPREADSHEET, formData);
  }

// export const uploadSpreadsheet: ApiFunction<
//   { file: File; onProgress?: (progress: number) => void },
//   UploadSpreadSheetResponse
// > = async ({ file, onProgress }) => {
//   const formData = new FormData();
//   formData.append('file', file);
//   formData.append('table_name', file.name.split('.')[0]);

//   const config = {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//     // eslint-disable-next-line @typescript-eslint/no-explicit-any
//     onUploadProgress: (progressEvent: any) => {
//       if (progressEvent.total && onProgress) {
//         const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
//         onProgress(percentCompleted);
//       }
//     },
//   };

//   return await post(DATA_SOURCE_ENDPOINTS.UPLOAD_SPREADSHEET, formData, config);
// };

export const uploadDocument = async () => {};

export const addDataSource = async () => {};
// #GetDataSourcesResponse
export const getDataSources: ApiFunction<void, GetDataSourcesResponse> = async () => {
  return await get(DATA_SOURCE_ENDPOINTS.GET_DATA_SOURCES);
};

export const getDataSourceTables = async () => {};
