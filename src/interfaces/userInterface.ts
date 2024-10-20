export interface User {
    user_id: number;
    name: string;
    email: string;
    access_token:string
  }

  export interface SignupUser {
    name: string;
    email: string;
    password: string;
  }
  export interface LoginSignupResponse {
    user_id: number;
    name: string;
    email: string;
    access_token:string
  }

  export interface LoginUser {
    email: string;
    password: string;
  }
  
export interface UserStore {
    user: User | null;
    isLoading: boolean;
    setUser: (payload: User) => void;
    signupUser: (payload: SignupUser) => void;
    // loginUser: (payload: LoginUser) => Promise<void>;
    // fetchUser: (id: string) => Promise<void>;
  }