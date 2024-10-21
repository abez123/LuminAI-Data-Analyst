// hooks/useAuth.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import { SignupUser, LoginUser, LoginSignupResponse, User } from "../interfaces/userInterface";
import {ApiResponse} from "../interfaces/globalInterfaces";
import { signupUser, loginUser, fetchUser } from "../zustand/apis/userApi";
import { AxiosError } from 'axios';
import useStore from '../zustand/stores/useStore';
import { saveUser } from '../utils/localstorageUtils';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

interface ErrorResponse {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any; 
}

export const useSignupMutation = () => {
  const navigate = useNavigate();
  const setUser = useStore((state) => state.setUser);
  return useMutation<ApiResponse<LoginSignupResponse>, AxiosError<ErrorResponse>, SignupUser>({
    mutationFn: signupUser,
    onSuccess: (response) => {
      const data: User = response.data;
      setUser(data);
      saveUser(data);
      navigate('/data-sources');
      toast.success(`Welcome to LUMIN ${data.name}`);
    },
    onError: (error) => {
      console.log(error.response?.data);
    },
  });
};

export const useLoginMutation = () => {
  const setUser = useStore((state) => state.setUser);
  const navigate = useNavigate();

  return useMutation<ApiResponse<LoginSignupResponse>, AxiosError<ErrorResponse>, LoginUser>({
    mutationFn: loginUser,
    onSuccess: (response) => {
      const data: User = response.data;
      setUser(data);
      saveUser(data);
      navigate('/data-sources');
      toast.success(`Welcome back ${data.name}`);
    },
    onError: (error) => {
      console.log(error.response?.data);
    },
  });
};

export const useFetchUser = (token: string) => {
//   const setUser = useStore((state) => state.setUser);
//   const setLoader = useStore((state) => state.setLoader);
  return useQuery<User, Error>({
    queryKey: ['user'],
    queryFn: () => fetchUser(token),
    // onSuccess: (data) => {
    //   setUser(data);
    //   setLoader({ userLoaded: true });
    // },
  });
};