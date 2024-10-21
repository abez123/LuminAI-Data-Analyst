/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosRequestConfig } from 'axios';
import { API_BASE_URL } from '../apis/endPoints';
import { getUser } from '../../utils/localstorageUtils';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  const user = getUser();
  if (user && user.access_token) {
    config.headers.Authorization = `Bearer ${user.access_token}`;
  }
  return config;
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
