import React from 'react';
import { BiFile } from 'react-icons/bi';

interface FileInfo {
  name: string;
  description: string;
  size: string;
  dateUploaded: string;
  lastUpdated: string;
  uploadedBy: string;
}

const DataSource: React.FC = () => {
  // Mock data - replace with your actual data source
  const files: FileInfo[] = Array(5).fill({
    name: 'Filename',
    description: 'Description',
    dateUploaded: '10.02.2022 18:38',
    lastUpdated: '10.02.2022 18:38',
  });

  return (
    <div className="flex flex-col py-8 pr-8 h-screen">
      <div className="h-full rounded-[20px] bg-white border border-blue-gray-100 dark:bg-maroon-400 dark:border-maroon-600 w-full">
        <div className="bg-white rounded-[20px] shadow-sm overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <th className="px-6 py-3">Type</th>
                <th className="px-6 py-3">Source name</th>
                <th className="px-6 py-3">Date uploaded</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {files.map((file, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <BiFile className="h-6 w-6 text-blue-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{file.name}</div>
                        <div className="text-sm text-gray-500">{file.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file.dateUploaded}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file.lastUpdated}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DataSource;
