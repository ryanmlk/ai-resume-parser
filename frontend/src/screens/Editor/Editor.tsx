import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { X, Download } from "lucide-react";
import WordEditor from "../../components/ui/word_editor";
import PDFViewer from "../../components/ui/pdf_viewer";
import { parseResume } from "../../api/api_calls";
import { useEffect, useState } from "react";
import { ResumeData } from "../../types/resume";
import TiptapEditor from "../../components/tiptap/Tiptap";
import html2pdf from 'html2pdf.js';

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
  const [resumeHTML, setResumeHTML] = useState("");

  useEffect(() => {
    if (!parsedResume && !feedbackSections && !resumeScore) {
      setParseLoading(true);
      setParsedResume({
        personal_information: {
          name: "Ryan Moses",
          email: "ryanmoses99@gmail.com",
          phone: "613-293-1197",
          location: "Ottawa, ON K2C3N1",
          linkedin_url: null,
          portfolio_url: null,
          github_url: null,
          other_links: [],
        },
        summary:
          "I am an international student pursuing a postgraduate certificate in Artificial Intelligence and Machine Learning at Lambton College Ottawa. With over 4 years of experience in software development roles and a passion for solving real-world problems, I am eager to contribute to applied research. My detail-oriented nature, adaptability, and collaborative experience prepare me to excel as a Student Researcher. I am excited to apply my technical skills and dedication to support Lambton College Research.",
        work_experience: [
          {
            job_title: "Software Engineer",
            company: "Rooverr Technologies",
            location: "Colombo, Sri Lanka",
            start_date: "Jan 2023",
            end_date: "Aug 2024",
            description:
              "Developed a web application using Next.js for the frontend and Nest.js for the backend.\nContributed significantly to both frontend and backend development, including making UI improvements using Figma and adding new pages.\nDeployed the web application on AWS and configured a CI/CD pipeline.\nUtilized various AWS services, such as SQS, SNS, Api Gateway, ECS, EC2, DynamoDB, Amplify, and Lambdas to enhance the application's functionality.\nAssumed a leadership role in launching a mobile app, selecting the Flutter framework for the architecture, and setting up the initial project structure for the team.\nIntroduced Agile methodologies to the team, establishing a structured sprint framework with daily meetings and bi-weekly sprint reviews, significantly improving project organization and efficiency.",
          },
          {
            job_title: "Trainee Software Developer",
            company: "IFS R&D International (Pvt) Ltd",
            location: "Colombo, Sri Lanka",
            start_date: "Jan 2020",
            end_date: "Dec 2022",
            description:
              "Enhanced existing software, addressing errors, adapting to new hardware, and upgrading interfaces to boost performance.\nEnsured product quality through feedback analysis, integration management, and continuous testing.\nCollaborated with senior engineers to implement Agile development methodologies for prototype tasks.\nGained insights through design and code reviews, enhancing knowledge of development processes.\nExpanded programming language skills to write high-quality object-oriented code.\nImplemented CI/CD pipelines to elevate product quality, including automated integrated tests.",
          },
        ],
        education: [
          {
            institution: "Lambton College",
            degree: "Artificial Intelligence and Machine Learning",
            major: null,
            location: "Ottawa",
            start_date: "Sep 2024",
            end_date: "Present",
            details: null,
          },
          {
            institution: "Sri Lanka Institute of Information Technology",
            degree: "B.Sc. (Hons) in Information Technology",
            major: null,
            location: null,
            start_date: "Jan 2019",
            end_date: "Dec 2022",
            details: "GPA 3.66",
          },
        ],
        skills: [
          "JavaScript",
          "TypeScript",
          "Python",
          "SQL",
          "Next.js",
          "Nest.js",
          "Flutter",
          "AWS (SQS, SNS, Lambda, API Gateway, EC2, DynamoDB)",
          "CI/CD pipelines",
          "MySQL",
          "DynamoDB",
          "Git",
          "Docker",
          "JIRA",
          "Jenkin",
          "Attention to Detail",
          "Adaptable",
          "Good Communication",
        ],
        projects: [],
        certifications: [],
        languages: [],
        awards_and_honors: [
          "Consistent High Performance : Maintained a high academic standard with a GPA above 3.6",
          "Achievement-Oriented : Earned scholarships multiple times by ranking in the top 3% of my undergraduate class",
          "Reliability and Initiative : Awarded a full scholarship and the opportunity to work as a Trainee Software Developer based on exceptional academic performance",
          "Quality Assurance and Attention to Detail : Worked as the QA counterpart in my team at IFS, collaborating closely to ensure high-quality outcomes, highlighting my attention to detail, responsibility, and ability to work effectively within a team.",
        ],
      });
      setFeedback({
        personal_information: {
          score: 0.6,
          feedback: [
            "Consider adding a LinkedIn profile to boost credibility.",
            "Consider adding a portfolio or GitHub link.",
          ],
        },
        summary: {
          score: 0.5,
          feedback: [
            "Avoid vague buzzwords like 'detail-oriented', 'collaborative'. Focus on measurable skills or impact instead.",
            "Good! But consider adding more skills like time, customer.",
          ],
        },
        work_experience: {
          score: 0.6,
          feedback: [
            "Entry 1: Consider mentioning at least one technical skill (e.g., management, microsoft, problem)",
            "Entry 2: Good! But consider adding more skills like time, customer.",
          ],
        },
        education: {
          score: 1,
          feedback: ["Education section looks good."],
        },
        skills: {
          score: 1,
          feedback: ["Skills section is well populated."],
        },
      });
      setParseLoading(false);
      // parseResume(file)
      //   .then((data) => {
      //     setParsedResume(data.result.parsed_resume);
      //     setFeedback(data.result.feedback.sections);
      //     setResumeScore(data.result.feedback.score);
      //     setParseLoading(false);
      //   })
      //   .catch((error) => {
      //     console.error("Error parsing resume:", error);
      //   });
    }
    // console.log("Parsed Resume:", parsedResume);
    // console.log("Feedback Sections:", feedbackSections);
  }, []);

  const handleCancel = () => {
    navigate("/");
  };

  const handleExportPDF = () => {
    const element = document.querySelector('.tiptap');
    if (element) {
      html2pdf().from(element).set({
        margin: 0.5,
        filename: 'resume.pdf',
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
      }).save();
    }
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
          <Button className="flex items-center gap-2" onClick={handleExportPDF}>
            <Download className="w-4 h-4" />
            Download
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex h-[calc(100vh-4rem)]">
        {/* PDF Viewer */}
        <div className="w-[60%] bg-gray-50 overflow-auto p-8">
          {/* {file.type === "app lication/pdf" ? (
            <PDFViewer file={file} />
          ) : (
            <WordEditor file={file} />
          )} */}
          {parsedResume && (
            <TiptapEditor onChange={setResumeHTML} resumeData={parsedResume} />
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
                        {feedbackSections?.personal_information && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            {feedbackSections.personal_information.feedback?.map(
                              (feedback: string) => (
                                <p className="text-black-600">{feedback}</p>
                              )
                            )}
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
                        {feedbackSections?.summary && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            {feedbackSections.summary.feedback?.map(
                              (feedback: string) => (
                                <p className="text-black-600">{feedback}</p>
                              )
                            )}
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
                        {feedbackSections?.work_experience && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            {feedbackSections.work_experience.feedback?.map(
                              (feedback: string) => (
                                <p className="text-black-600">{feedback}</p>
                              )
                            )}
                          </div>
                        )}
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
                        {feedbackSections?.education && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            {feedbackSections.education.feedback?.map(
                              (feedback: string) => (
                                <p className="text-black-600">{feedback}</p>
                              )
                            )}
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
                        {feedbackSections?.skills && (
                          <div className="mt-3 bg-gray-100 p-3 rounded-md">
                            {feedbackSections.skills.feedback?.map(
                              (feedback: string) => (
                                <p className="text-black-600">{feedback}</p>
                              )
                            )}
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
            onClick={handleExportPDF}
          >
            <Download className="w-4 h-4" />
            Download
          </Button>
        </div>
      </div>
    </div>
  );
};
