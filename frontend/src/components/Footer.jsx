import { useLocation } from "react-router-dom";

export default function Footer() {
  const { pathname } = useLocation();

  if (pathnamesToHideFooterOn.includes(pathname)) {
    return null;
  }

  return (
    <div>
      (<h1>Footer</h1>)
    </div>
  );
}

const pathnamesToHideFooterOn = ["/auth/get-signup-email"];
