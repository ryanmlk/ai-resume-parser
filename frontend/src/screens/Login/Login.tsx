import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { AuthContext } from "../../auth/AuthContext";

export const Login = (): JSX.Element => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState<string | null>(null);
  const authContext = useContext(AuthContext);
  const navigate = useNavigate(); // Initialize useNavigate

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleLogin = async () => {
    setError(null); // Clear previous errors
    try {
      const response = await fetch("http://localhost:8080/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: formData.email,
          password: formData.password,
        }),
      });

      if (!response.ok) {
        throw new Error("Invalid email or password");
      }

      const data = await response.json();
      console.log("Login successful:", data);

      // Use AuthContext to handle login
      authContext?.login(data.access_token);

      // Redirect to the landing page
      navigate("/");
    } catch (error: any) {
      setError(error.message);
    }
  };

  return (
    <div className="bg-[#eeeeee] flex flex-row justify-center w-full">
      <div className="bg-[#eeeeee] overflow-hidden w-screen h-screen relative">
        {/* Decorative circles */}
        {/* ... (same as before) */}

        {/* Main content section */}
        <header className="absolute w-[795px] h-[327px] top-[349px] left-1/2 -translate-x-1/2 bg-transparent flex flex-col items-center z-20">
          <h1 className="[font-family:'Gotham_Rounded-Bold',Helvetica] font-bold text-[#213344] text-7xl text-center tracking-[0] leading-[72px]">
            Welcome Back!
          </h1>

          <form
            className="mt-[36px] flex flex-col items-center w-full"
            onSubmit={(e) => {
              e.preventDefault();
              handleLogin();
            }}
          >
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-[400px] h-[50px] px-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-[400px] h-[50px] px-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <Button
              className="w-[186px] h-[63px] bg-[#1865ff] rounded-[28px] text-base"
              type="submit"
            >
              Log In
            </Button>
          </form>
        </header>
      </div>
    </div>
  );
};