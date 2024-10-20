import {AUTH_ENDPOINTS} from './endPoints';
import { post, get } from './apiClient';
import { SignupUser, LoginUser,User } from '../../interfaces/userInterface';

export const signupUser = async (data: SignupUser) => {
    try{
        return await post<User>(AUTH_ENDPOINTS.SIGNUP, data);
    }catch(err){
        console.log(err);
    }
};

export const loginUser = async (data: LoginUser) => {
    try{
        return await post<unknown>(AUTH_ENDPOINTS.LOGIN, data);
    }catch(err){
        console.log(err);
    }
};

export const fetchUser = async (token: string) => {
    try{
        return await get<unknown>(AUTH_ENDPOINTS.GET_USER, token);
    }catch(err){
        console.log(err);
    }
};

  