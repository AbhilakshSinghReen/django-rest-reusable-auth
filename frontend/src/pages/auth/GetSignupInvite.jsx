import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { BeatLoader } from "react-spinners";
import { CSSTransition } from "react-transition-group";

import { appName } from "../../config/config";

export default function GetSignupInvite() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasSentEmail, setHasSentEmail] = useState(false);
  const [email, setEmail] = useState("");

  useEffect(() => {
    document.title = `Register Your Account - ${appName}`;
  }, []);

  const apiUrl = "http://localhost:8000/api/v1/auth/request-email-user-invite/";

  const handleContinueButtonClick = async (_e) => {
    setIsLoading(true);

    const requestBody = {
      email: email,
    };

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Invitation sent successfully:", data);
      } else {
        console.error("Error sending invitation:", data);
      }
    } catch (error) {
      console.error("Error:", error);
    }

    // setTimeout(() => {
    setIsLoading(false);
    setHasSentEmail(true);
    // }, 1500);
  };

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
              maxWidth: "350px",
              borderBottom: "1px solid grey",
              marginBottom: 2,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Typography variant="h5" gutterBottom>
              <strong>Register Your Account</strong>
            </Typography>
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
              maxWidth: "350px",
              borderBottom: "1px solid grey",
              marginBottom: 2,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Typography variant="h4" gutterBottom>
              Check Your Email
            </Typography>
          </Box>
          <Typography variant="body1">We've sent you an email. Please check your inbox to proceed.</Typography>
        </Box>
      </CSSTransition>
    </Box>
  );
}
