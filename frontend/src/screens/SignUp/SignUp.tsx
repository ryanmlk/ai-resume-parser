import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";
import { AuthContext } from "../../auth/AuthContext";

export const SignUp = (): JSX.Element => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "job_seeker", // Default role
  });

  const [error, setError] = useState<string | null>(null);
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSignUp = async () => {
    setError(null); // Clear previous errors
    try {
      // Sign up the user
      const signUpResponse = await fetch("http://localhost:8080/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!signUpResponse.ok) {
        throw new Error("Failed to sign up");
      }

      console.log("Sign up successful");

      // Automatically log the user in
      const loginResponse = await fetch("http://localhost:8080/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: formData.email,
          password: formData.password,
        }),
      });

      if (!loginResponse.ok) {
        throw new Error("Failed to log in after sign up");
      }

      const loginData = await loginResponse.json();
      console.log("Login successful:", loginData);

      // Use AuthContext to handle login
      authContext?.login(loginData.access_token);

      // Redirect to the landing page
      navigate("/");
    } catch (error: any) {
      setError(error.message);
      console.error("Error during sign up or login:", error);
    }
  };

  return (
    <div className="bg-[#eeeeee] flex flex-row justify-center w-full">
      <div className="bg-[#eeeeee] overflow-hidden w-screen h-screen relative">
        {/* Decorative circles */}
        <div className="absolute w-32 h-32 rounded-full bg-blue-500/70 blur-xl top-20 left-24 animate-pulse" />
        <div className="absolute w-28 h-28 rounded-full bg-purple-500/70 blur-xl top-16 right-32 animate-pulse" />
        <div className="absolute w-36 h-36 rounded-full bg-pink-500/70 blur-xl top-[450px] left-16 animate-pulse" />
        <div className="absolute w-40 h-40 rounded-full bg-indigo-500/70 blur-xl bottom-32 right-20 animate-pulse" />
        <div className="absolute w-24 h-24 rounded-full bg-teal-500/70 blur-xl top-[350px] right-12 animate-pulse" />
        <div className="absolute w-28 h-28 rounded-full bg-cyan-500/70 blur-xl bottom-24 left-36 animate-pulse" />
        <div className="absolute w-32 h-32 rounded-full bg-rose-500/70 blur-xl top-[200px] left-[45%] animate-pulse" />
        <div className="absolute w-24 h-24 rounded-full bg-emerald-500/70 blur-xl top-[600px] right-[40%] animate-pulse" />
        <div className="absolute w-36 h-36 rounded-full bg-violet-500/70 blur-xl bottom-48 left-[30%] animate-pulse" />
        <div className="absolute w-28 h-28 rounded-full bg-sky-500/70 blur-xl top-40 right-[35%] animate-pulse" />

        {/* Main content section */}
        <header className="absolute w-[795px] h-[327px] top-[349px] left-1/2 -translate-x-1/2 bg-transparent flex flex-col items-center z-20">
          <h1 className="[font-family:'Gotham_Rounded-Bold',Helvetica] font-bold text-[#213344] text-7xl text-center tracking-[0] leading-[72px]">
            Create an Account
          </h1>

          <p className="w-[651px] mt-[27px] font-m3-body-large font-[number:var(--m3-body-large-font-weight)] text-black text-[length:var(--m3-body-large-font-size)] text-center tracking-[var(--m3-body-large-letter-spacing)] leading-[var(--m3-body-large-line-height)] [font-style:var(--m3-body-large-font-style)]">
            Sign up to access personalized resume insights and job matches.
          </p>

          <form className="mt-[36px] flex flex-col items-center w-full">
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleInputChange}
              className="w-[400px] h-[50px] px-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-[400px] h-[50px] px-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-[400px] h-[50px] px-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Button
              className="w-[186px] h-[63px] bg-[#1865ff] rounded-[28px] text-base"
              onClick={handleSignUp}
              type="button"
            >
              Sign Up
            </Button>
          </form>
        </header>

        {/* Navigation bar */}
        <Card className="absolute w-[1312px] h-[87px] top-[45px] left-1/2 -translate-x-1/2 rounded-[40px] flex items-center justify-between px-20 bg-white/80 backdrop-blur-sm z-30">
          <img
            src="/logo.png"
            alt="ResumeBoost Logo"
            className="h-[55px]"
          />

          <Button
            className="w-[186px] h-[63px] bg-[#1865ff] rounded-[28px] text-base"
            onClick={() => navigate("/login")}
          >
            Log In
          </Button>
        </Card>
      </div>
    </div>
  );
};