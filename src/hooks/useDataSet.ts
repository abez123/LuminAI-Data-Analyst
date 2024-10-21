import { useMutation } from '@tanstack/react-query';
import { GetDataSourcesResponse, UploadSpreadSheetResponse } from "../interfaces/dataSourceInterface";
import { AxiosError } from 'axios';
import {ApiResponse} from "../interfaces/globalInterfaces";
import { getDataSources,uploadSpreadsheet } from "../zustand/apis/dataSourceApi";
import dataSetStore from '../zustand/stores/dataSetStore';
// import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

interface ErrorResponse {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any; 
}

export const useGetDataSourcesMutation = () => {
    const setDataSet = dataSetStore((state) => state.setDataSet);
    return useMutation<ApiResponse<GetDataSourcesResponse>, AxiosError<ErrorResponse>, void>({
      mutationFn: getDataSources,
      onSuccess: (response) => {
        setDataSet(response.data.data_sources)
      },
      onError: (error) => {
        console.log(error.response?.data);
      },
    });
  };

export const useUploadSpreadsheet= () => {
  return useMutation<ApiResponse<UploadSpreadSheetResponse>, AxiosError<ErrorResponse>, File>({
    mutationFn: uploadSpreadsheet,
    onSuccess: (response) => {
      console.log(response)
      toast.success(response.message)
      // setDataSet(response.data.data_sources)
    },
    onError: (error) => {
      console.log(error.response?.data.message);
      toast.error(error.response?.data.message)
    },
  });
}

