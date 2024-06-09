import Container from "@mui/material/Container";

import Footer from "./Footer";
import Header from "./Header";

export default function Layout({ themeMode, setThemeMode, children }) {
  return (
    <div>
      <Header themeMode={themeMode} setThemeMode={setThemeMode} />
      <Container>{children}</Container>
      {/* <Footer /> */}
    </div>
  );
}
