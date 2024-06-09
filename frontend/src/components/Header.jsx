import { useLocation } from "react-router-dom";

import Navbar from "./Navbar";
import { isPathnameIncluded } from "../utils/routeUtils";

export default function Header({ themeMode, setThemeMode }) {
  const { pathname } = useLocation();

  if (isPathnameIncluded(pathnamesToHideHeaderOn, pathname)) {
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
  "/auth/get-signup-email",
  "/auth/complete-signup",
  "/auth/request-password-reset",
  "/auth/reset-password",
  "/auth/signin",
];
