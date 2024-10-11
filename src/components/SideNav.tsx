import { useState, useEffect } from 'react';
import { BiPlus, BiBookContent, BiComment, BiSitemap, BiCog, BiMoon, BiSun } from 'react-icons/bi';
import { Link } from 'react-router-dom';

const SideNav = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  return (
    <div className="w-24 dark:bg-maroon-800 flex flex-col items-center py-4 space-y-6">
      <button className="p-2 text-navy-600 hover:bg-gray-200 rounded-lg dark:text-maroon-600">
        <BiBookContent className="w-6 h-6" />
      </button>
      <Link
        to={'/chat'}
        className="p-2 mt-2 text-navy-600 bg-white hover:bg-gray-200 border border-blue-gray-100 rounded-lg dark:bg-maroon-400  dark:text-maroon-600 dark:border-maroon-800"
      >
        <BiPlus className="w-6 h-6" />
      </Link>
      <Link
        to={'/chat-history'}
        className="p-2 text-navy-600 hover:bg-gray-200 rounded-lg dark:text-maroon-600"
      >
        <BiComment className="w-6 h-6" />
      </Link>
      <Link
        to={'/data-sources'}
        className="p-2 text-navy-600 hover:bg-gray-200 rounded-lg dark:text-maroon-600"
      >
        <BiSitemap className="w-6 h-6" />
      </Link>
      <Link
        to={'/settings'}
        className="p-2 text-navy-600 hover:bg-gray-200 rounded-lg dark:text-maroon-600"
      >
        <BiCog className="w-6 h-6" />
      </Link>
      <div className="flex-grow" />
      <button
        onClick={() => setIsDarkMode(!isDarkMode)}
        className="p-2 text-navy-600 hover:bg-blue-gray-700/10 rounded-lg dark:text-maroon-600"
      >
        {isDarkMode ? <BiMoon className="w-6 h-6" /> : <BiSun className="w-6 h-6" />}
      </button>
    </div>
  );
};

export default SideNav;
