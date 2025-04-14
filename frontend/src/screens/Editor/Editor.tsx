import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { X, Download } from "lucide-react";
import WordEditor from "../../components/ui/word_editor";
import PDFViewer from "../../components/ui/pdf_viewer";
import { parseResume } from "../../api/resume_api";
import { useEffect, useState } from "react";
import { ResumeData } from "../../types/resume";

export const Editor = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  const { file } = location.state as { file: File };
  const [parsedResume, setParsedResume] = useState<ResumeData | null>(null);
  const [feedbackSections, setFeedback] = useState<any>(null);
  const [resumeScore, setResumeScore] = useState<number | null>(null);
  const [piExpanded, setPiExpanded] = useState<Boolean>(false);
  const [summaryExpanded, setSummaryExpanded] = useState<Boolean>(false);
  const [weExpanded, setWeExpanded] = useState<Boolean>(false);
  const [eduExpanded, setEduExpanded] = useState<Boolean>(false);
  const [skillsExpanded, setSkillsExpanded] = useState<Boolean>(false);
  const [parseLoading, setParseLoading] = useState<Boolean>(false);

  useEffect(() => {
    if (!parsedResume && !feedbackSections && !resumeScore) {
      setParseLoading(true);
      parseResume(file)
        .then((data) => {
          setParsedResume(data.result.parsed_resume);
          setFeedback(data.result.feedback.sections);
          setResumeScore(data.result.feedback.score);
          setParseLoading(false);
        })
        .catch((error) => {
          console.error("Error parsing resume:", error);
        });
    }
  }, []);

  const handleCancel = () => {
    navigate("/");
  };

  const handleDownload = () => {
    const url = URL.createObjectURL(file);
    const a = document.createElement("a");
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
        <div className="text-lg font-medium text-gray-800">{file.name}</div>
        <div className="flex gap-4">
          {resumeScore !== null && (
            <div
              className={`text-white px-4 rounded-full flex items-center justify-center text-sm font-medium ${
                resumeScore >= 80
                  ? "bg-green-600"
                  : resumeScore >= 60
                  ? "bg-blue-600"
                  : resumeScore >= 40
                  ? "bg-yellow-600"
                  : "bg-red-600"
              }`}
              style={{ fontSize: "14px" }}
            >
              Resume Score: {resumeScore}
            </div>
          )}
          <Button
            variant="outline"
            className="flex items-center gap-2"
            onClick={handleCancel}
          >
            <X className="w-4 h-4" />
            Cancel
          </Button>
          <Button className="flex items-center gap-2" onClick={handleDownload}>
            <Download className="w-4 h-4" />
            Download
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex h-[calc(100vh-4rem)]">
        {/* PDF Viewer */}
        <div className="w-[60%] bg-gray-50 overflow-auto p-8">
          {file.type === "application/pdf" ? (
            <PDFViewer file={file} />
          ) : (
            <WordEditor file={file} />
          )}
        </div>

        {/* Toolbar area */}
        <div className="w-[40%] bg-white border-l border-gray-200 p-6">
          {/* Resume Sections Dropdown */}
          {parseLoading ? (
            <div className="flex flex-col items-center justify-center h-64">
              <div className="w-12 h-12 border-4 border-t-blue-500 border-gray-200 rounded-full animate-spin"></div>
              <p className="mt-4 text-gray-600">Evaluating your resume...</p>
            </div>
          ) : (
            <div className="mb-6">
              <button className="w-full flex items-center justify-between bg-gray-100 text-gray-800 font-medium py-2 px-4 rounded-md">
                RESUME SECTIONS
              </button>
              <div className="mt-2 space-y-2">
                {parsedResume?.personal_information && (
                  <div>
                    <div
                      onClick={() => setPiExpanded(!piExpanded)}
                      className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5">📄</span> Personal Information
                      </div>
                      <div className="flex items-center gap-2">
                        {feedbackSections?.personal_information && (
                          <div className="bg-gray-700 text-white px-4 h-6 rounded-full flex items-center justify-center text-xs font-medium">
                            Score: {feedbackSections.personal_information.score}
                          </div>
                        )}
                        <span>{piExpanded ? "▲" : "▼"}</span>
                      </div>
                    </div>
                    {piExpanded && (
                      <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                        {parsedResume?.personal_information.name && (
                          <p>Name: {parsedResume.personal_information.name}</p>
                        )}
                        {parsedResume?.personal_information.email && (
                          <p>
                            Email: {parsedResume.personal_information.email}
                          </p>
                        )}
                        {parsedResume?.personal_information.phone && (
                          <p>
                            Phone: {parsedResume.personal_information.phone}
                          </p>
                        )}
                        {parsedResume?.personal_information.location && (
                          <p>
                            Location:{" "}
                            {parsedResume.personal_information.location}
                          </p>
                        )}
                        {parsedResume?.personal_information.linkedin_url && (
                          <p>
                            Linkedin:{" "}
                            {parsedResume.personal_information.linkedin_url}
                          </p>
                        )}
                        {parsedResume?.personal_information.portfolio_url && (
                          <p>
                            Portfolio:{" "}
                            {parsedResume.personal_information.portfolio_url}
                          </p>
                        )}
                        {parsedResume?.personal_information.github_url && (
                          <p>
                            Github:{" "}
                            {parsedResume.personal_information.github_url}
                          </p>
                        )}
                        {parsedResume?.personal_information.other_links && (
                          <p>
                            Other:{" "}
                            {parsedResume.personal_information.other_links}
                          </p>
                        )}

                        {feedbackSections?.personal_information && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.personal_information.feedback}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
                {parsedResume?.summary && (
                  <div>
                    <div
                      onClick={() => setSummaryExpanded(!summaryExpanded)}
                      className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5">≡</span> Summary
                      </div>
                      <div className="flex items-center gap-2">
                        {feedbackSections?.summary && (
                          <div className="bg-gray-700 text-white px-4 h-6 rounded-full flex items-center justify-center text-xs font-medium">
                            Score: {feedbackSections.summary.score}
                          </div>
                        )}
                        <span>{summaryExpanded ? "▲" : "▼"}</span>
                      </div>
                    </div>
                    {summaryExpanded && (
                      <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                        {parsedResume?.summary && <p>{parsedResume.summary}</p>}
                        {feedbackSections?.summary && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.summary.feedback}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
                {parsedResume?.work_experience && (
                  <div>
                    <div
                      onClick={() => setWeExpanded(!weExpanded)}
                      className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5">👥</span> Work Experience
                      </div>
                      <div className="flex items-center gap-2">
                        {feedbackSections?.work_experience && (
                          <div className="bg-gray-700 text-white px-4 h-6 rounded-full flex items-center justify-center text-xs font-medium">
                            Score: {feedbackSections.work_experience.score}
                          </div>
                        )}
                        <span>{weExpanded ? "▲" : "▼"}</span>
                      </div>
                    </div>
                    {weExpanded && (
                      <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                        {parsedResume?.work_experience?.map((job, index) => (
                          <>
                          <div
                            key={index}
                            className="mb-3 pb-3 border-b border-gray-100"
                          >
                            <p className="font-medium">
                              {job.job_title} - {job.company}
                            </p>
                            {job.start_date && job.end_date && (
                              <p className="text-xs text-gray-500">
                                {job.start_date} - {job.end_date}
                              </p>
                            )}
                            {job.location && (
                              <p className="text-xs text-gray-500 mt-1">
                                {job.location}
                              </p>
                            )}
                            {job.description && (
                              <p className="mt-1">{job.description}</p>
                            )}
                          </div>
                          {feedbackSections?.work_experience && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.work_experience.feedback[index]}
                            </p>
                          </div>
                        )}
                        </>
                        ))}
                        {parsedResume?.work_experience?.length === 0 && (
                          <p>No work experience found</p>
                        )}
                        {/* {feedbackSections?.work_experience && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.work_experience.feedback}
                            </p>
                          </div>
                        )} */}
                      </div>
                    )}
                  </div>
                )}
                {parsedResume?.education && (
                  <div>
                    <div
                      onClick={() => setEduExpanded(!eduExpanded)}
                      className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5">🎓</span> Education
                      </div>
                      <div className="flex items-center gap-2">
                        {feedbackSections?.education && (
                          <div className="bg-gray-700 text-white px-4 h-6 rounded-full flex items-center justify-center text-xs font-medium">
                            Score: {feedbackSections.education.score}
                          </div>
                        )}
                        <span>{eduExpanded ? "▲" : "▼"}</span>
                      </div>
                    </div>
                    {eduExpanded && (
                      <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                        {parsedResume?.education?.map((edu, index) => (
                          <div
                            key={index}
                            className="mb-3 pb-3 border-b border-gray-100"
                          >
                            <p className="font-medium">
                              {edu.degree} - {edu.institution}
                            </p>
                            {edu.start_date && edu.end_date && (
                              <p className="text-xs text-gray-500">
                                {edu.start_date} - {edu.end_date}
                              </p>
                            )}
                            {edu.major && (
                              <p className="text-xs text-gray-500">
                                Major: {edu.major}
                              </p>
                            )}
                            {edu.location && (
                              <p className="text-xs text-gray-500 mt-1">
                                {edu.location}
                              </p>
                            )}
                            {edu.details && (
                              <p className="mt-1">{edu.details}</p>
                            )}
                          </div>
                        ))}
                        {parsedResume?.education?.length === 0 && (
                          <p>No education details found</p>
                        )}
                        {feedbackSections?.education && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.education.feedback}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
                {parsedResume?.skills && (
                  <div>
                    <div
                      onClick={() => setSkillsExpanded(!skillsExpanded)}
                      className="flex items-center justify-between gap-2 text-gray-700 py-1 px-2 hover:bg-gray-50 rounded cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5">🔵</span> Skills
                      </div>
                      <div className="flex items-center gap-2">
                        {feedbackSections?.skills && (
                          <div className="bg-gray-700 text-white px-4 h-6 rounded-full flex items-center justify-center text-xs font-medium">
                            Score: {feedbackSections.skills.score}
                          </div>
                        )}
                        <span>{skillsExpanded ? "▲" : "▼"}</span>
                      </div>
                    </div>
                    {skillsExpanded && (
                      <div className="ml-7 mt-1 text-sm text-gray-600 border-l-2 border-gray-200 pl-2">
                        {parsedResume?.skills?.map((skill) => (
                          <p className="font-medium">{skill}</p>
                        ))}
                        {parsedResume?.skills?.length === 0 && (
                          <p>No skills found</p>
                        )}
                        {feedbackSections?.skills && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            <p className="font-medium text-black-700">
                              Feedback:
                            </p>
                            <p className="text-black-600">
                              {feedbackSections.skills.feedback}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

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
