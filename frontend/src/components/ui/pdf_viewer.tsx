import { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

const PDFViewer = ({ file }: { file: File }) => {

    const [numPages, setNumPages] = useState<number>(0);

    return (
      <Document
            file={file}
            onLoadSuccess={({ numPages }) => {
              setNumPages(numPages)
            }}
            className="flex flex-col items-center"
          >
            {Array.from(new Array(numPages), (_, index) => (
              <Page
                key={`page_${index + 1}`}
                pageNumber={index + 1}
                className="mb-8 shadow-lg"
                width={Math.min(window.innerWidth * 0.6, 800)}
                renderTextLayer={false}
              />
            ))}
          </Document>
    );
  };

  export default PDFViewer;