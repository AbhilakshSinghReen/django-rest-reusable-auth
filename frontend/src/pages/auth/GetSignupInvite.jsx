import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { BeatLoader } from "react-spinners";
import { CSSTransition } from "react-transition-group";

import apiClient from "../../api/apiClient";
import { appName } from "../../config/config";

export default function GetSignupInvite() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasSentEmail, setHasSentEmail] = useState(false);
  const [email, setEmail] = useState("");

  const handleContinueButtonClick = async (_e) => {
    setIsLoading(true);

    const responseData = await apiClient.requestEmailUserInvite(email);
    if (!responseData.success) {
      window.alert(responseData.error.user_friendly_message);
      setIsLoading(false);
      return;
    }

    setIsLoading(false);
    setHasSentEmail(true);
  };

  useEffect(() => {
    document.title = `Register Your Account - ${appName}`;
  }, []);

  return (
    <Box
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
            marginTop: "10vh",
          }}
        >
          <img src="/logo192.png" />
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
              <strong>Register Your Account</strong>
            </Typography>
            <Box
              sx={{
                width: "80%",
                borderBottom: "1px solid grey",
              }}
            />
          </Box>
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
          <Typography variant="body1">We've sent you an email. Please check your inbox to proceed.</Typography>
        </Box>
      </CSSTransition>
    </Box>
  );
}
