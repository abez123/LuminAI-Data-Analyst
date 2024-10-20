/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosRequestConfig } from 'axios';
import { API_BASE_URL } from '../apis/endPoints';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

const getAuthHeader = (token?: string): AxiosRequestConfig => {
  if (token) {
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }
  return {};
};

export const get = async <T>(url: string, token?: string): Promise<T> => {
  const config = getAuthHeader(token);
  const response = await apiClient.get<T>(url, config);
  return response.data;
};

export const post = async <T>(url: string, data: any, token?: string): Promise<T> => {
  const config = getAuthHeader(token);
  const response = await apiClient.post<T>(url, data, config);
  return response.data;
};

export const put = async <T>(url: string, data: any, token?: string): Promise<T> => {
  const config = getAuthHeader(token);
  const response = await apiClient.put<T>(url, data, config);
  return response.data;
};

export const del = async <T>(url: string, token?: string): Promise<T> => {
  const config = getAuthHeader(token);
  const response = await apiClient.delete<T>(url, config);
  return response.data;
};
