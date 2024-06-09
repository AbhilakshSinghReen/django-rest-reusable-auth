import { createTheme, CssBaseline, responsiveFontSizes, ThemeProvider } from "@mui/material";

export default function ThemeRegistry({ themeMode, children }) {
  const themeOptions = {
    palette: {
      mode: themeMode,
    },
  };

  const theme = responsiveFontSizes(createTheme(themeOptions));

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
