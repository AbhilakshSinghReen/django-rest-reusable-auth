import { useState, useEffect } from "react";
import AppBar from "@mui/material/AppBar";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import LightModeIcon from "@mui/icons-material/LightMode";

import { appName } from "../config/config";

export default function Navbar({ themeMode, setThemeMode }) {
  const [themeModeButtonAnimationClassName, setThemeModeButtonAnimationClassName] = useState("");

  useEffect(() => {
    setThemeModeButtonAnimationClassName(
      themeMode === "light" ? "reverse-animated-theme-mode-icon" : "animated-theme-mode-icon"
    );
  }, [themeMode]);

  return (
    <AppBar position="fixed">
      <Container>
        <Toolbar
          sx={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            height: "100%",
            padding: 0,
          }}
        >
          <Typography
            variant="h4"
            sx={{
              fontWeight: "bold",
              textAlign: "center",
              "&:hover": {
                cursor: "pointer",
              },
              background: "linear-gradient(45deg, #FFD700 30%, #FFA500 90%)",
              "-webkit-background-clip": "text",
              "-webkit-text-fill-color": "transparent",
            }}
          >
            {appName}
          </Typography>

          <IconButton color="inherit" onClick={() => setThemeMode(themeMode === "light" ? "dark" : "light")}>
            <LightModeIcon className={themeModeButtonAnimationClassName} />
          </IconButton>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
