import React from 'react';
import ChartComponent from '../components/ChartComponent';
// import axios from 'axios';

const ChatHistory = () => {
  return (
    <div className="flex flex-col py-8 pr-8 h-screen">
      {/* <div className="h-full flex rounded-[20px] bg-white border border-blue-gray-100 dark:bg-maroon-400 dark:border-maroon-600 w-full">
        <div className="w-1/6 bg-yellow-gray-50 rounded-l-[20px] border-r border-l-blue-gray-100 p-6 flex flex-col items-start justify-start "></div>
        <div>

          
        </div>
      </div> */}

<ChartComponent
        type='bar'
        data={{
          "labels": [
              "beleza_saude",
              "relogios_presentes",
              "cama_mesa_banho",
              "esporte_lazer",
              "informatica_acessorios",
              "moveis_decoracao",
              "cool_stuff",
              "utilidades_domesticas",
              "automotivo",
              "ferramentas_jardim"
          ],
          "values": [
              {
                  "data": [
                      1258681.339999968
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      1205005.6800000058
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      1036988.6800000716
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      988048.9700000364
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      911954.3200000412
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      729762.4900000462
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      635290.8500000037
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      632248.6600000246
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      592720.110000013
                  ],
                  "label": "Total Sales"
              },
              {
                  "data": [
                      485256.46000001614
                  ],
                  "label": "Total Sales"
              }
          ]
      }}
        />
    </div>
  );
};

export default ChatHistory;
