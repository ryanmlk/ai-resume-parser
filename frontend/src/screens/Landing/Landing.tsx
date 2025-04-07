import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";

export const Landing = (): JSX.Element => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      navigate('/editor', { state: { file } });
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

        {/* Hidden file input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
          accept=".docx, .doc, .pdf"
        />

        {/* Main content section */}
        <header className="absolute w-[795px] h-[327px] top-[349px] left-1/2 -translate-x-1/2 bg-transparent flex flex-col items-center z-20">
          <h1 className="[font-family:'Gotham_Rounded-Bold',Helvetica] font-bold text-[#213344] text-7xl text-center tracking-[0] leading-[72px]">
            Boost Your Resume, <br />
            Land Your Dream Job
          </h1>

          <p className="w-[651px] mt-[27px] font-m3-body-large font-[number:var(--m3-body-large-font-weight)] text-black text-[length:var(--m3-body-large-font-size)] text-center tracking-[var(--m3-body-large-letter-spacing)] leading-[var(--m3-body-large-line-height)] [font-style:var(--m3-body-large-font-style)]">
            ResumeBoost supercharges your resume with AI-powered insights.
            Upload your file, get tailored suggestions, and match your skills to
            real job postings—fast, simple, and effective.
          </p>

          <Button 
            className="mt-[36px] w-[186px] h-[63px] bg-[#1865ff] rounded-[28px] text-base"
            onClick={handleUploadClick}
          >
            Upload Resume
          </Button>
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
            onClick={handleUploadClick}
          >
            Upload Resume
          </Button>
        </Card>
      </div>
    </div>
  );
};