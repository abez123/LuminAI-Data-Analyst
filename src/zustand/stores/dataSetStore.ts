import { create } from 'zustand'
import { DataSources } from "../../interfaces/dataSourceInterface";

export interface DataSetStore {
  dataSets: DataSources[] | null;
  setDataSet: (user: DataSources[]) => void;
}

const dataSetStore = create<DataSetStore>((set) => ({
  dataSets: null,
  setDataSet: (dataSets: DataSources[]) => set({ dataSets }),
//   addDataSet: (user: User) => set({ user }),
//   updateDataSet: (user: User) => set({ user }),
//   deleteDataSet: (user: User) => set({ user }),
}));

export default dataSetStore;