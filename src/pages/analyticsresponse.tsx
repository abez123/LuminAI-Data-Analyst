import React, { useState } from 'react'
// import { Book, MessageSquare, Database, Settings, Moon } from 'lucide-react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const chartData = {
  labels: ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6', 'Category 7', 'Category 8', 'Category 9'],
  datasets: [
    {
      data: [300, 50, 100, 200, 75, 50, 400, 250, 350],
      backgroundColor: 'rgba(99, 102, 241, 0.5)',
      borderColor: 'rgb(99, 102, 241)',
      borderWidth: 1,
    },
  ],
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      type: 'category' as const,
    },
    y: {
      type: 'linear' as const,
      beginAtZero: true,
      ticks: {
        callback: function(value: number) {
          return '$' + value
        }
      }
    },
  },
}

export default function DataAnalysisDashboard() {
  const [question, setQuestion] = useState('')

  return (
    <div className="">
      {/* Sidebar */}


      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Section - Question and Chart */}
        <div className="w-1/2 p-8 border-r border-gray-200 overflow-y-auto">
          <div className="flex items-center mb-6">
            <img src="/placeholder.svg" alt="User" className="w-8 h-8 rounded-full mr-3" />
            <h2 className="text-xl font-semibold text-gray-800">
              Which Product Categories Generate The Most Revenue?
            </h2>
          </div>
          <div className="mb-6">
            <Bar data={chartData} options={chartOptions} />
          </div>
          <div className="mb-4 text-sm text-gray-600">
            Current margin: April Spendings
            <span className="float-right">
              <span className="font-semibold">$350.00</span> / $640.00
            </span>
          </div>
          <p className="mb-6 text-sm">
            The Product Category Generating The Most Revenue Is <span className="text-green-500 font-semibold">Beleza_saude</span>
          </p>
          <div className="relative">
            <textarea
              className="w-full h-32 p-4 bg-gray-100 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Type Your Question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            ></textarea>
            <button className="absolute bottom-4 right-4 text-gray-400 hover:text-gray-600">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>

        {/* Right Section - Process Steps */}
        <div className="w-1/2 p-8 space-y-6">
          <div>
            <p className="text-gray-600 mb-2">Relevant tables and columns retrieved 🎉</p>
            <div className="flex space-x-2">
              <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">olist_products</span>
              <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">olist_orders</span>
            </div>
          </div>
          <div>
            <p className="text-gray-600 mb-2">SQL query generated 🚀</p>
            <div className="bg-gray-800 rounded-lg p-4 text-sm">
              <pre className="text-green-400">
                {`CREATE TABLE IF NOT EXISTS "chats" (
  "id" uuid PRIMARY KEY DEFAULT
gen_random_uuid() NOT NULL,
  "title" text,
  "atlas_user_id" uuid NOT NULL,
  "created_at" timestamp DEFAULT now()
);`}
              </pre>
            </div>
          </div>
          <div>
            <p className="text-gray-600 flex items-center">
              SQL query is correct no issues found
              <svg className="w-5 h-5 text-green-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </p>
          </div>
          <div>
            <p className="text-gray-600 flex items-center">
              SQL Query executed
              <svg className="w-5 h-5 text-green-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </p>
          </div>
          <div>
            <p className="text-gray-600">
              I am using a <span className="font-semibold">Bar Chart</span> because the query results display product
              categories and their total revenue, making it ideal for comparing
              the revenue generated by each category.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}