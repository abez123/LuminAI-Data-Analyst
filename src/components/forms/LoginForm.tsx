import { useState } from 'react'
import { FaEye,FaEyeSlash } from "react-icons/fa";

const LoginForm: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   console.log('Login attempt with:', { email, password });
  // };

  return (
    <form>
    <div className="mb-6">
      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
        Email
      </label>
      <input
        type="text"
        id="email"
        className="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
    </div>
    <div className="mb-6">
      <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
        Password
      </label>
      <div className="relative">
        <input
          type={showPassword ? 'text' : 'password'}
          id="password"
          className="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="button"
          className="absolute inset-y-0 right-0 pr-3 flex items-center"
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? (
            <FaEye className="h-5 w-5 text-gray-400"/>
          ) : (
            <FaEyeSlash className="h-5 w-5 text-gray-400" />
          )}
        </button>
      </div>
    </div>

    <button
      type="submit"
      className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mb-6"
    >
      Sign in
    </button>
  </form>
  );
};

export default LoginForm;