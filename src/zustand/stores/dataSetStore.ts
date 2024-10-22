import { create } from 'zustand'
import { DataSources } from "../../interfaces/dataSourceInterface";

export interface DataSetStore {
  dataSets: DataSources[] | null;
  setDataSet: (dataSets: DataSources[]) => void;
  addDataSet: (dataSet: DataSources) => void;
  updateDataSet: (dataSet: DataSources) => void;
  deleteDataSet: (id: number) => void;
}

const dataSetStore = create<DataSetStore>((set) => ({
  dataSets: null,
  
  setDataSet: (dataSets: DataSources[]) => 
    set({ dataSets }),
  
  addDataSet: (dataSet: DataSources) => 
    set((state) => ({
      dataSets: state.dataSets ? [...state.dataSets, dataSet] : [dataSet]
    })),
  
  updateDataSet: (updatedDataSet: DataSources) =>
    set((state) => ({
      dataSets: state.dataSets?.map(dataSet => 
        dataSet.id === updatedDataSet.id ? updatedDataSet : dataSet
      ) || null
    })),
  
  deleteDataSet: (id: number) =>
    set((state) => ({
      dataSets: state.dataSets?.filter(dataSet => dataSet.id !== id) || null
    })),
}));

export default dataSetStore;