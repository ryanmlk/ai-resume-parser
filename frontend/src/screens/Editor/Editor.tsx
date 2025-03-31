import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from "../../components/ui/button";
import { X, Download } from 'lucide-react';
import WordEditor from '../../components/ui/word_editor';
import PDFViewer from '../../components/ui/pdf_viewer';

export const Editor = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { file } = location.state as { file: File };

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
          {/* Toolbar content will be added later */}
        </div>
      </div>
    </div>
  );
};