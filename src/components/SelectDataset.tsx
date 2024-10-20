import {useState} from 'react'
import { MdKeyboardArrowDown } from "react-icons/md";

const SelectDataset:React.FC = () => {

    const [selectedDataSource, setSelectedDataSource] = useState('');

  return (
    <div className='mx-auto mb-24'>
    <h1 className={`text-center text-2xl font-bold text-navy-800`}>
      Have Something In Mind?
    </h1>

    <p className={`text-center text-sm text-navy-600 my-4`}>
      Select Or Add A Data Set, Ask Me Anything About The Data Set,
      <br />
      Get Meaningful Insight From Me.
    </p>

    <div className="flex justify-center items-center mt-4">
      <div className="relative">
        <select
          className={`appearance-none bg-blue-gray-50 border-blue-gray-100 text-gray-700 border rounded-[12px] py-2 pr-8 pl-4 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
          value={selectedDataSource}
          onChange={(e) => setSelectedDataSource(e.target.value)}
        >
          <option value="">Select Tables</option>
          {/* Add your data source options here */}
        </select>
        <div className={`mr-l pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700`}>
          <MdKeyboardArrowDown className="h-5 w-5" />
        </div>
      </div>
      <span className={`mx-4 text-gray-400`}>|</span>
      <div className="relative">
        <select
          className={`appearance-none bg-blue-gray-50 border-blue-gray-100 text-gray-700 border rounded-[12px] py-2 pr-8 pl-4 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
          value={selectedDataSource}
          onChange={(e) => setSelectedDataSource(e.target.value)}
        >
          <option value="">Select LLM Model</option>
          {/* Add your data source options here */}
        </select>
        <div className={`mr-l pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700`}>
          <MdKeyboardArrowDown className="h-5 w-5" />
        </div>
      </div>
    </div>
  </div>
  )
}

export default SelectDataset