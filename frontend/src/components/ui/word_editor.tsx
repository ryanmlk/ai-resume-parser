import { useEffect, useRef } from 'react';
import { renderAsync } from 'docx-preview';

const WordEditor = ({ file }: { file: File }) => {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
      const loadDocx = async () => {
        if (file && containerRef.current) {
          const arrayBuffer = await file.arrayBuffer();
          await renderAsync(arrayBuffer, containerRef.current);
        }
      };

      loadDocx();
    }, [file]);

    return (
      <div className="flex flex-col items-center">
        <div
          ref={containerRef}
          className="w-full h-full border border-gray-300 rounded-md p-4 overflow-auto bg-white"
        />
      </div>
    );
  };

  export default WordEditor;