import React, { useState } from 'react';
import { BiUpload, BiFile, BiX } from 'react-icons/bi';

interface FileInfo {
  name: string;
  size: number;
  progress: number;
  status: 'uploading' | 'completed';
}

type UploadFileProps = {
    setComponent: React.Dispatch<React.SetStateAction<string>>
  };

const UploadFile: React.FC<UploadFileProps> = ({setComponent}) => {
  const [files, setFiles] = useState<FileInfo[]>([
    // { name: 'my-cv.pdf', size: 120 * 1024, progress: 50, status: 'uploading' },
    // { name: 'Google-certificate.pdf', size: 94 * 1024, progress: 100, status: 'completed' },
  ]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Handle file selection logic here
    // For demonstration, let's add a new file to the list
    const file = event.target.files?.[0];
    if (file) {
      setFiles([
        ...files,
        {
          name: file.name,
          size: file.size,
          progress: 0,
          status: 'uploading',
        },
      ]);
    }
  };

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">Add your data source</h3>

      <div className="mt-2">
        <p className="text-sm text-gray-500 mb-4">Select and upload the files of your choice</p>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-4">
          <BiUpload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-lg font-medium mb-2">Choose a file or drag & drop it here</p>
          <p className="text-sm text-gray-500 mb-4">Excel, CSV, PDF, and Text files, up to 50MB</p>
          <div className="flex flex-row align-center justify-center">
            <button
              className="bg-white text-gray-700 border border-gray-300 rounded px-4 py-2 hover:bg-gray-50"
              onClick={() => document.getElementById('fileInput')?.click()}
            >
              Browse File
            </button>
            <p className="my-auto px-4">OR</p>
            <button 
            onClick={() => setComponent("ConnectDB")}
            className="bg-white text-gray-700 border border-gray-300 rounded px-4 py-2 hover:bg-gray-50">
              Connect Database
            </button>
          </div>
          <input id="fileInput" type="file" className="hidden" onChange={handleFileChange} />
        </div>

        {files.map((file, index) => (
          <div key={index} className="bg-gray-50 rounded-lg p-3 mb-2 flex items-center">
            <BiFile className="w-8 h-8 text-red-500 mr-3" />
            <div className="flex-grow">
              <div className="flex justify-between items-center mb-1">
                <span className="font-medium">{file.name}</span>
                <button onClick={() => removeFile(index)}>
                  <BiX className="w-4 h-4 text-gray-500" />
                </button>
              </div>
              <div className="text-xs text-gray-500">
                {file.progress === 100
                  ? 'Completed'
                  : `${Math.round(file.size / 1024)} KB of ${Math.round(file.size / 1024)} KB`}
              </div>
              {file.status === 'uploading' && (
                <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div
                    className="bg-blue-600 h-1.5 rounded-full"
                    style={{ width: `${file.progress}%` }}
                  ></div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UploadFile;
