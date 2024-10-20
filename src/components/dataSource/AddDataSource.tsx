import React, { useState } from 'react';

type AddDataSourceProps = {
  setComponent: React.Dispatch<React.SetStateAction<string>>;
};

const AddDataSource: React.FC<AddDataSourceProps> = ({ setComponent }) => {
  const [sourceName, setSourceName] = useState('');
  const [dbUrl, setDbUrl] = useState('');

  return (
    <form>
      <div className="mb-6">
        <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
          Source Name
        </label>
        <input
          type="text"
          id="source_name"
          className="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter source name"
          value={sourceName}
          onChange={(e) => setSourceName(e.target.value)}
        />
      </div>
      <div className="mb-6">
        <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
          Database URL
        </label>
        <input
          type="text"
          id="source_name"
          className="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your database url"
          value={dbUrl}
          onChange={(e) => setDbUrl(e.target.value)}
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mb-6"
      >
        Connect Database
      </button>

      <button
        onClick={() => setComponent('uploadFile')}
        className="font-medium text-blue-600 hover:text-blue-500 text-center w-full"
      >
        Upload Data Source
      </button>
    </form>
  );
};

export default AddDataSource;
