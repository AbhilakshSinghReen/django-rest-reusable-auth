import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { BeatLoader } from "react-spinners";
import { CSSTransition } from "react-transition-group";

import apiClient from "../../api/apiClient";
import { appName } from "../../config/config";

export default function RequestPasswordReset() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasSentEmail, setHasSentEmail] = useState(false);
  const [email, setEmail] = useState("");

  const handleContinueButtonClick = async (_e) => {
    setIsLoading(true);

    const responseData = await apiClient.requestPasswordResetViaEmail(email);
    if (!responseData.success) {
      window.alert(responseData.error.user_friendly_message);
      setIsLoading(false);
      return;
    }

    setIsLoading(false);
    setHasSentEmail(true);
  };

  useEffect(() => {
    document.title = `Reset Your Password - ${appName}`;
  }, []);

  return (
    <Container
      maxWidth="sm"
      sx={{
        position: "relative",
        width: "100%",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      <CSSTransition in={!hasSentEmail} timeout={500} classNames="fade" unmountOnExit>
        <Box
          sx={{
            width: "100%",
            position: "absolute",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
            alignItems: "center",
            marginTop: 2,
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
              marginTop: 1,
              marginBottom: 2,
            }}
          >
            {appName}
          </Typography>
          <Box
            sx={{
              width: "80%",
              marginTop: 2,
              marginBottom: 2,
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-start",
              alignItems: "center",
            }}
          >
            <Typography variant="h5" gutterBottom>
              <strong>Reset Your Password</strong>
            </Typography>
            <Box
              sx={{
                width: "80%",
                borderBottom: "1px solid grey",
              }}
            />
          </Box>

          <Typography variant="body1" sx={{ marginBottom: 2 }}>
            Enter your email to continue. A link to reset your password will be shared with you.
          </Typography>

          <TextField
            placeholder="Your Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            sx={{
              width: "80%",
              maxWidth: "350px",
              marginBottom: 2,
            }}
          />

          <Button variant="contained" color="primary" onClick={handleContinueButtonClick} disabled={isLoading}>
            {isLoading ? <BeatLoader color="white" loading={true} size={10} /> : "Continue"}
          </Button>
        </Box>
      </CSSTransition>
      <CSSTransition in={hasSentEmail} timeout={500} classNames="fade" unmountOnExit>
        <Box
          sx={{
            width: "100%",
            position: "absolute",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
            alignItems: "center",
            marginTop: "20vh",
          }}
        >
          <Box
            sx={{
              width: "80%",
              marginTop: 2,
              marginBottom: 2,
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-start",
              alignItems: "center",
            }}
          >
            <Typography variant="h5" gutterBottom>
              Check Your Email
            </Typography>
            <Box
              sx={{
                width: "80%",
                borderBottom: "1px solid grey",
              }}
            />
          </Box>
          <Typography variant="body1">We've sent you a link to reset your password.</Typography>
        </Box>
      </CSSTransition>
    </Container>
  );
}
