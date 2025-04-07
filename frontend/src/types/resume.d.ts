export interface ResumeData {
    personal_information: {
      name: string | null;
      email: string | null;
      phone: string | null;
      location: string | null;
      linkedin_url: string | null;
      portfolio_url: string | null;
      github_url: string | null;
      other_links: string[];
    };
    summary: string | null;
    work_experience: Array<{
      job_title: string | null;
      company: string | null;
      location: string | null;
      start_date: string | null;
      end_date: string | null;
      description: string | null;
    }>;
    education: Array<{
      institution: string | null;
      degree: string | null;
      major: string | null;
      location: string | null;
      start_date: string | null;
      end_date: string | null;
      details: string | null;
    }>;
    skills: string[];
    projects: Array<{
      name: string | null;
      description: string | null;
      technologies_used: string[];
      link: string | null;
    }>;
    certifications: string[];
    languages: string[];
    awards_and_honors: string[];
}
  