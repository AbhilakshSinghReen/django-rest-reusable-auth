import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import CompleteSignup from "./pages/auth/CompleteSignup";
import GetSignupInvite from "./pages/auth/GetSignupInvite";
import RequestPasswordReset from "./pages/auth/RequestPasswordReset";
import ResetPassword from "./pages/auth/ResetPassword";
import Login from "./pages/auth/Login";
import Layout from "./components/Layout";
import ThemeRegistry from "./components/ThemeRegistry";
import UserContextProvider from "./contextProviders/UserContextProvider";

import "react-loading-skeleton/dist/skeleton.css";
import "./App.css";

export default function App() {
  const savedThemeMode = localStorage.getItem("themeMode");
  const [themeMode, setThemeMode] = useState(savedThemeMode !== null ? savedThemeMode : "light");

  useEffect(() => {
    localStorage.setItem("themeMode", themeMode);
  }, [themeMode]);

  return (
    <ThemeRegistry themeMode={themeMode}>
      <UserContextProvider>
        <Router>
          <Layout themeMode={themeMode} setThemeMode={setThemeMode}>
            <Routes>
              <Route path="/auth/get-signup-email" element={<GetSignupInvite />} />
              <Route path="/auth/complete-signup/:userInviteToken" element={<CompleteSignup />} />
              <Route path="/auth/request-password-reset" element={<RequestPasswordReset />} />
              <Route path="/auth/reset-password/:passwordResetToken" element={<ResetPassword />} />
              <Route path="/auth/signin" element={<Login />} />
            </Routes>
          </Layout>
        </Router>
      </UserContextProvider>
    </ThemeRegistry>
  );
}
