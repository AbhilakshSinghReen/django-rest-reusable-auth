import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import GetSignupInvite from "./pages/auth/GetSignupInvite";
import Layout from "./components/Layout";
import ThemeRegistry from "./components/ThemeRegistry";

import "./App.css";

export default function App() {
  const savedThemeMode = localStorage.getItem("themeMode");
  const [themeMode, setThemeMode] = useState(savedThemeMode !== null ? savedThemeMode : "light");

  useEffect(() => {
    localStorage.setItem("themeMode", themeMode);
  }, [themeMode]);

  return (
    <ThemeRegistry themeMode={themeMode}>
      <Router>
        <Layout themeMode={themeMode} setThemeMode={setThemeMode}>
          <Routes>
            <Route path="/auth/get-signup-email" element={<GetSignupInvite />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeRegistry>
  );
}
