import { useEffect } from 'react';
import { FiCommand } from 'react-icons/fi';
import Prism from 'prismjs';
import 'prismjs/themes/prism-okaidia.css'; // Dark theme
import 'prismjs/components/prism-sql'; // SQL language support

const sqlCode = `
CREATE TABLE IF NOT EXISTS "chats" (
    "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
    "title" text,
    "atlas_user_id" uuid NOT NULL,
    "created_at" timestamp DEFAULT now()
);
`;

const SQLCode: React.FC = () => {
  useEffect(() => {
    Prism.highlightAll();
  }, []);

  return (
    <pre>
      <code
        className="language-sql"
        style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', overflow: 'visible' }}
      >
        {sqlCode}
      </code>
    </pre>
  );
};

const Steps: React.FC = () => {
  return (
    <div className="w-1/2 bg-yellow-gray-50 rounded-r-[20px] border-l border-l-blue-gray-100 p-6 flex flex-col items-start justify-start ">
      <div className="flex items-center p-6 w-full bg-white rounded-[18px] border border-yellow-gray-100">
        <FiCommand className="w-5 h-5 text-gray-400 animate-spin mr-3" />
        <span className="text-gray-600">Retrieve the relevant tables and columns...</span>
      </div>

      <div className="p-6 mt-4 w-full bg-white rounded-[18px] border border-yellow-gray-100">
        <p className="text-gray-600">Retrieve the relevant tables and columns...</p>
        <div>
          <SQLCode />
        </div>
      </div>
    </div>
  );
};

export default Steps;
