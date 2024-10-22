import React, { useEffect } from 'react';
import { BiUpload, BiFile, BiLink } from 'react-icons/bi';
import { IoIosArrowForward } from 'react-icons/io';
import { FiCommand } from 'react-icons/fi';
import { toast } from 'react-toastify';
import { useGetDataSourcesMutation, useUploadSpreadsheetMutation } from '../../hooks/useDataSet';
import dataSetStore from '../../zustand/stores/dataSetStore';
import { DataSourceTableLoader } from '../loaders/DataSourceTableLoader';
import { Link } from 'react-router-dom';

type UploadFileProps = {
  setComponent: React.Dispatch<React.SetStateAction<string>>;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

const UploadFile: React.FC<UploadFileProps> = ({ setComponent,setIsOpen }) => {
  const dataSets = dataSetStore((state) => state.dataSets);
  const { mutate: uploadSpreadSheet, status: uploadSpreadSheetStatus } = useUploadSpreadsheetMutation();
  const {
    mutate: getDataSource,
    status: dataSourceStatus,
    isError,
    error,
    data,
  } = useGetDataSourcesMutation();

  console.log({
    dataSourceStatus,
    data,
    error,
    isError,
  });

  useEffect(() => {
    if (!dataSets) {
      getDataSource();
    }
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      const fileName = file.name;
      const fileExtension = fileName.slice(((fileName.lastIndexOf('.') - 1) >>> 0) + 2);

      // Define allowed file types
      const allowedExtensions = ['csv', 'xlsx', 'xls', 'pdf', 'txt'];
      const allowedMimeTypes = [
        'text/csv',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // xlsx
        'application/vnd.ms-excel', // xls
        'application/pdf',
        'text/plain',
      ];

      // Check if the file type is allowed
      if (allowedExtensions.includes(fileExtension) && allowedMimeTypes.includes(file.type)) {
        if (['csv', 'xlsx', 'xls'].includes(fileExtension)) {
          uploadSpreadSheet(file);
        } else {
          console.log('Upload document');
        }
      } else {
        toast.error('Invalid file type. Please upload Excel, CSV, PDF, or Text files only.');
      }
    }
  };

  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">Add your data source</h3>

      <div className="mt-2">
        <p className="text-sm text-gray-500 mb-4">Select and upload the files of your choice</p>

        <div
          className={`border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-4 relative
        ${uploadSpreadSheetStatus === 'pending' ? 'bg-blue-50' : ''}`}
        >
          {/* Dark overlay when pending */}
          {uploadSpreadSheetStatus === 'pending' && (
            <div className="absolute inset-0 bg-black/10 rounded-lg" />
          )}

          {/* Spinner */}
          {uploadSpreadSheetStatus === 'pending' && (
            <div className="absolute inset-0 flex items-center justify-center z-20">
              <FiCommand className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          )}
          <div className="relative z-50">
            <BiUpload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg font-medium mb-2">Choose a file or drag & drop it here</p>
            <p className="text-sm text-gray-500 mb-4">
              Excel, CSV, PDF, and Text files, up to 50MB
            </p>
            <div className="flex flex-row align-center justify-center">
              <button
                disabled={dataSourceStatus === 'pending'}
                className="bg-white text-gray-700 border border-gray-300 rounded px-4 py-2 hover:bg-gray-50"
                onClick={() => document.getElementById('fileInput')?.click()}
              >
                Browse File
              </button>
              <p className="my-auto px-4">OR</p>
              <button
                disabled={dataSourceStatus === 'pending'}
                onClick={() => setComponent('ConnectDB')}
                className="bg-white text-gray-700 border border-gray-300 rounded px-4 py-2 hover:bg-gray-50"
              >
                Connect Database
              </button>
            </div>
            <input id="fileInput" type="file" className="hidden" onChange={handleFileChange} />
          </div>
        </div>

        {dataSourceStatus === 'pending' || uploadSpreadSheetStatus === 'pending' ? (
          <DataSourceTableLoader rows={3} />
        ) : (
          <>
            {dataSets?.map((file, index) => (
              <Link
                to={`/chat/${file.id}`}
                onClick={() => setIsOpen(false)}
                key={index}
                className="bg-gray-50 rounded-lg p-3 mb-2 flex items-center cursor-pointer"
              >
                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                  {file.type === 'url' ? (
                    <BiLink className="h-6 w-6 text-blue-600" />
                  ) : (
                    <BiFile className="h-6 w-6 text-blue-600" />
                  )}
                </div>
                <div className="flex-grow">
                  <div className="flex justify-between items-center mb-1">
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{file.name}</div>
                      <div className="text-sm text-gray-500 uppercase">{file.type}</div>
                    </div>
                    <button>
                      <IoIosArrowForward className="w-6 h-6 text-blue-600" />
                    </button>
                  </div>
                </div>
              </Link>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default UploadFile;
