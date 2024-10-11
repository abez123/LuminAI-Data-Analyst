import { useRoutes } from "react-router-dom";

import Login from "./pages/login";
import Chat from "./pages/chat";
import Layout from "./components/Layout";
import ChatHistory from "./pages/chatHistory";
import DataSource from "./pages/dataSource";
import Settings from "./pages/settings";

// A simplified PrivateRoute component to handle auth logic
// const PrivateRoute = ({ element }) => {
//   const isAuthenticated = localStorage.getItem("userToken");

//   return isAuthenticated ? (
//     element
//   ) : (
//     <Navigate to="/" /> // Redirect to login page if not authenticated
//   );
// };

// Define your routing logic
const AppRoutes = () => {
  const routes = useRoutes([
    { path: "/", element: <Login /> },
    { path: "/chat", element: <Layout><Chat /></Layout> },
    { path: "/chat-history", element: <Layout><ChatHistory /></Layout> },
    { path: "/data-sources", element: <Layout><DataSource /></Layout> },
    { path: "/settings", element: <Layout><Settings /></Layout> },
    // { path: "/form", element: <Registration /> },
    // { path: "/edit/:id", element: <EditUser /> },
    // { path: "/thankyouPage", element: <ThankYouPage /> },

    // Protected route for Dashboard
    // {
    //   path: "/dashboard",
    //   element: (
    //     <PrivateRoute
    //       element={
    //         <Layout>
    //           <Dashboard />
    //         </Layout>
    //       }
    //     />
    //   ),
    // },

  ]);

  return routes;
};

export default AppRoutes;
