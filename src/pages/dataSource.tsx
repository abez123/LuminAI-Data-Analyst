import React,{useEffect} from 'react';
import { BiFile } from 'react-icons/bi';
import { useGetDataSourcesMutation } from '../hooks/useDataSet';
import dataSetStore from '../zustand/stores/dataSetStore';
import {DataSourceTableLoader} from '../components/loaders/DataSourceTableLoader';

const DataSource: React.FC = () => {

  const dataSets = dataSetStore((state) => state.dataSets);
  const { mutate: getDataSource,status, isError, error,data } = useGetDataSourcesMutation();

  useEffect(() => {
    if(!dataSets){
      getDataSource()
    }
  }, [])

  console.log({
    status, isError, error,data
  })


  return (
    <div className="flex flex-col py-8 pr-8 h-screen">
      <div className="h-full rounded-[20px] bg-white border border-blue-gray-100 dark:bg-maroon-400 dark:border-maroon-600 w-full">
        <div className="bg-white rounded-[20px] shadow-sm overflow-hidden">
          {
            status === 'pending'? 
            <DataSourceTableLoader rows={3} />
            :
            <table className="w-full">
            <thead>
              <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <th className="px-6 py-3">Type</th>
                <th className="px-6 py-3">Source name</th>
                <th className="px-6 py-3">Date uploaded</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {dataSets?.map((file, index) => (
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
                        <div className="text-sm text-gray-500">{file.type}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file?.table_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file?.created_at}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          }

        </div>
      </div>
    </div>
  );
};

export default DataSource;
