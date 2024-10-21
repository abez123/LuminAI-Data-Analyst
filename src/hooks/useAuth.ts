// hooks/useAuth.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import { SignupUser, LoginUser, LoginSignupResponse, User } from "../interfaces/userInterface";
import {ApiResponse} from "../interfaces/globalInterfaces";
import { signupUser, loginUser, fetchUser } from "../zustand/apis/userApi";
import { AxiosError } from 'axios';
import useStore from '../zustand/stores/useStore';
import { saveUser } from '../utils/localstorageUtils';
import { useNavigate } from 'react-router-dom';


interface ErrorResponse {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any; 
}

export const useSignupMutation = () => {
//   const setUser = useStore((state) => state.setUser);
  return useMutation<ApiResponse<LoginSignupResponse>, Error, SignupUser>({
    mutationFn: signupUser,
    onSuccess: (data) => {
      console.log(data);
    //   setUser(data.user);
      // Handle successful signup (e.g., store token, redirect)
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