import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from "../../components/ui/button";
import { X, Download } from 'lucide-react';
import WordEditor from '../../components/ui/word_editor';
import PDFViewer from '../../components/ui/pdf_viewer';
import { parseResume } from "../../api/resume_api";
import { useEffect, useState } from 'react';
import { ResumeData } from "../../types/resume";

export const Editor = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { file } = location.state as { file: File };
  const [parsedResume, setParsedResume] = useState<ResumeData | null>(null);
  const [piExpanded, setPiExpanded] = useState<Boolean>(false);
  const [summaryExpanded, setSummaryExpanded] = useState<Boolean>(false);
  const [weExpanded, setWeExpanded] = useState<Boolean>(false);
  const [eduExpanded, setEduExpanded] = useState<Boolean>(false);
  const [skillsExpanded, setSkillsExpanded] = useState<Boolean>(false);

  useEffect(() => {
    console.log("Parsing resume:", file);
    parseResume(file)
      .then((data) => {
        setParsedResume(data.result);
      })
      .catch((error) => {
        console.error("Error parsing resume:", error);
      }
    );
  }, []);

  const handleCancel = () => {
    navigate('/');
  };

  const handleDownload = () => {
    const url = URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Toolbar */}
      <div className="h-16 bg-white shadow-sm flex items-center justify-between px-6">
        <div className="text-lg font-medium text-gray-800">
          {file.name}
        </div>
        <div className="flex gap-4">
          <Button
            variant="outline"
            className="flex items-center gap-2"
            onClick={handleCancel}
          >
            <X className="w-4 h-4" />
            Cancel
          </Button>
          <Button
            className="flex items-center gap-2"
            onClick={handleDownload}
          >
            <Download className="w-4 h-4" />
            Download
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex h-[calc(100vh-4rem)]">
        {/* PDF Viewer */}
        <div className="w-[60%] bg-gray-50 overflow-auto p-8">
          {file.type === 'application/pdf' ? (<PDFViewer file={file} />) : (<WordEditor file={file} />)}
        </div>

        {/* Toolbar area */}
        <div className="w-[40%] bg-white border-l border-gray-200 p-6">

        {/* Resume Sections Dropdown */}
        <div className="mb-6">
          <button className="w-full flex items-center justify-between bg-gray-100 text-gray-800 font-medium py-2 px-4 rounded-md">
            RESUME SECTIONS
          </button>
          <div className="mt-2 space-y-2">
            {parsedResume?.personal_information && 
            (<div>
              <div 
              onClick={() => setPiExpanded(!piExpanded)} 
              className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
              >
              <div className="flex items-center gap-2">
                <span className="w-5 h-5">📄</span> Personal Information
              </div>
              <span>{piExpanded ? '▲' : '▼'}</span>
              </div>
              {piExpanded && (
              <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                {parsedResume?.personal_information.name && <p>Name: {parsedResume.personal_information.name}</p>}
                {parsedResume?.personal_information.email && <p>Email: {parsedResume.personal_information.email}</p>}
                {parsedResume?.personal_information.phone && <p>Phone: {parsedResume.personal_information.phone}</p>}
                {parsedResume?.personal_information.location && <p>Location: {parsedResume.personal_information.location}</p>}
                {parsedResume?.personal_information.linkedin_url && <p>Linkedin: {parsedResume.personal_information.linkedin_url}</p>}
                {parsedResume?.personal_information.portfolio_url && <p>Portfolio: {parsedResume.personal_information.portfolio_url}</p>}
                {parsedResume?.personal_information.github_url && <p>Github: {parsedResume.personal_information.github_url}</p>}
                {parsedResume?.personal_information.other_links && <p>Other: {parsedResume.personal_information.other_links}</p>}
              </div>
              )}
            </div>)}
            {parsedResume?.summary && 
            (<div>
              <div 
              onClick={() => setSummaryExpanded(!summaryExpanded)} 
              className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
              >
              <div className="flex items-center gap-2">
              <span className="w-5 h-5">≡</span> Summary
              </div>
              <span>{summaryExpanded ? '▲' : '▼'}</span>
              </div>
              {summaryExpanded && (
              <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                {parsedResume?.summary && <p>{parsedResume.summary}</p>}
              </div>
              )}
            </div>)}
            {parsedResume?.work_experience && 
            (<div>
              <div 
              onClick={() => setWeExpanded(!weExpanded)} 
              className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
              >
              <div className="flex items-center gap-2">
              <span className="w-5 h-5">👥</span> Work Experience
              </div>
              <span>{weExpanded ? '▲' : '▼'}</span>
              </div>
              {weExpanded && (
                <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                {parsedResume?.work_experience?.map((job, index) => (
                  <div key={index} className="mb-3 pb-3 border-b border-gray-100">
                  <p className="font-medium">{job.job_title} - {job.company}</p>
                  {job.start_date && job.end_date && <p className="text-xs text-gray-500">{job.start_date} - {job.end_date}</p>}
                  {job.location && <p className="text-xs text-gray-500 mt-1">{job.location}</p>}
                  {job.description && <p className="mt-1">{job.description}</p>}
                  </div>
                ))}
                {parsedResume?.work_experience?.length === 0 && <p>No work experience found</p>}
                </div>
              )}
            </div>)}
            {parsedResume?.education && 
            (<div>
              <div 
              onClick={() => setEduExpanded(!eduExpanded)} 
              className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
              >
              <div className="flex items-center gap-2">
              <span className="w-5 h-5">🎓</span> Education
              </div>
              <span>{eduExpanded ? '▲' : '▼'}</span>
              </div>
              {eduExpanded && (
                <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                {parsedResume?.education?.map((edu, index) => (
                  <div key={index} className="mb-3 pb-3 border-b border-gray-100">
                  <p className="font-medium">{edu.degree} - {edu.institution}</p>
                  {edu.start_date && edu.end_date && <p className="text-xs text-gray-500">{edu.start_date} - {edu.end_date}</p>}
                  {edu.major && <p className="text-xs text-gray-500">Major: {edu.major}</p>}
                  {edu.location && <p className="text-xs text-gray-500 mt-1">{edu.location}</p>}
                  {edu.details && <p className="mt-1">{edu.details}</p>}
                  </div>
                ))}
                {parsedResume?.education?.length === 0 && <p>No education details found</p>}
                </div>
              )}
            </div>)}
            {parsedResume?.skills && 
            (<div>
              <div 
              onClick={() => setSkillsExpanded(!skillsExpanded)} 
              className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
              >
              <div className="flex items-center gap-2">
              <span className="w-5 h-5">🔵</span> Skills
              </div>
              <span>{skillsExpanded ? '▲' : '▼'}</span>
              </div>
              {skillsExpanded && (
                <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                {parsedResume?.skills?.map((skill) => (
                  <p className="font-medium">{skill}</p>
                ))}
                {parsedResume?.skills?.length === 0 && <p>No skills found</p>}
                </div>
              )}
            </div>)}
          </div>
        </div>

        {/* Spacer to push Download button to bottom */}
        <div className="flex-grow" />

        {/* Download Button (at bottom) */}
        <Button
          className="w-full flex items-center justify-center gap-2"
          onClick={handleDownload}
        >
          <Download className="w-4 h-4" />
          Download
        </Button>
        </div>
      </div>
    </div>
  );
};