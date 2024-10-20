import { create } from 'zustand'
import {UserStore,User, SignupUser} from "../../interfaces/userInterface";
import {signupUser} from "../../zustand/apis/userApi";

const useStore = create<UserStore>()((set) => ({
  user: null,
  isLoading: false,
  signupUser: (payload: SignupUser) => {
     signupUser(payload)
    // set({ user })
  },
  // loginUser: (data: LoginUser) => loginUser(data)
  setUser: (user:User) => set({ user })
}))

export default useStore