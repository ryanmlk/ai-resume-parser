import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import TextAlign from '@tiptap/extension-text-align';
import Highlight from '@tiptap/extension-highlight';
import { ResumeData } from '../../types/resume';
import './resume.scss';

export default function TiptapEditor({ resumeData, onChange }: { resumeData: ResumeData, onChange?: (html: string) => void }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Highlight,
      TextAlign.configure({
        types: ['heading', 'paragraph'],
      })
    ],
    content: generateResumeHTML(resumeData),
    onUpdate: ({ editor }) => {
      const html = editor.getHTML();
      onChange?.(html);
    },
  });

  if (!editor) return null;

  return (
    <div className="editor-wrapper">
      <MenuBar editor={editor} />
      <div className="bg-white rounded-lg shadow p-6 max-w-4xl mx-auto my-10">
        <EditorContent editor={editor} className="tiptap" />
      </div>
    </div>
  );
}

function generateResumeHTML(data: ResumeData): string {
  const safe = (str: string | null) => str || '';

  return `
    <h1 style="text-align:center">${safe(data.personal_information.name)}</h1>
    <h3 style="text-align:center">Fullstack Developer</h3>
    <p style="text-align:center">
      ${safe(data.personal_information.email)}<br>
      ${safe(data.personal_information.phone)}<br>
      ${safe(data.personal_information.location)}
    </p>
    <h2 style="text-align:center">Summary</h2>
    <p style="text-align:justify">${safe(data.summary)}</p>
    <h2 style="text-align:center">Work Experience</h2>
    ${data.work_experience.map(exp => `
      <h3>${safe(exp.job_title)} - ${safe(exp.company)}</h3>
      <p><em>${safe(exp.start_date)} - ${safe(exp.end_date)}</em></p>
      <p>${safe(exp.description)}</p>
    `).join('')}
    <h2 style="text-align:center">Education</h2>
    ${data.education.map(edu => `
      <h3>${safe(edu.degree)} in ${safe(edu.major)}</h3>
      <p><em>${safe(edu.institution)} | ${safe(edu.start_date)} - ${safe(edu.end_date)}</em></p>
      <p>${safe(edu.details)}</p>
    `).join('')}
    <h2 style="text-align:center">Skills</h2>
    <ul>
      ${data.skills.map(skill => `<li>${skill}</li>`).join('')}
    </ul>
  `;
}

function MenuBar({ editor }: { editor: any }) {
  if (!editor) return null;

  return (
    <div className="control-group p-4 bg-gray-100 rounded mb-4">
      <div className="button-group flex flex-wrap gap-2">
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}>H1</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}>H2</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}>H3</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().setParagraph().run()}>Paragraph</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleBold().run()}>Bold</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleItalic().run()}>Italic</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleStrike().run()}>Strike</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().toggleHighlight().run()}>Highlight</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().setTextAlign('left').run()}>Left</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().setTextAlign('center').run()}>Center</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().setTextAlign('right').run()}>Right</button>
        <button className="px-3 py-1 border rounded bg-white hover:bg-gray-50" onClick={() => editor.chain().focus().setTextAlign('justify').run()}>Justify</button>
      </div>
    </div>
  );
}

// Utility to split skills into 4 columns
function chunkArray(arr: string[], columns: number) {
  const result = new Array(columns).fill(null).map(() => [] as string[]);
  arr.forEach((item, idx) => {
    result[idx % columns].push(item);
  });
  return result;
}


