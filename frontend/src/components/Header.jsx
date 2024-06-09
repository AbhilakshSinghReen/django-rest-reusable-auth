import { useLocation } from "react-router-dom";

import Navbar from "./Navbar";

export default function Header({ themeMode, setThemeMode }) {
  const { pathname } = useLocation();

  if (pathnamesToHideHeaderOn.includes(pathname)) {
    return null;
  }

  return (
    <div>
      <Navbar themeMode={themeMode} setThemeMode={setThemeMode} />
      <div style={{ paddingTop: 55 }}></div> {/* TODO: make this dynamic according to the Navbar height */}
    </div>
  );
}

const pathnamesToHideHeaderOn = [
  // "/auth/get-signup-email"
];
