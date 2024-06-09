import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Link from "@mui/material/Link";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { BeatLoader } from "react-spinners";

import apiClient from "../../api/apiClient";
import { appName, userSelfRegistrationEnabled } from "../../config/config";
import SunriseLogo from "../../components/SunriseLogo";

export default function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLoginButtonClick = async (_e) => {
    setIsLoading(true);

    const responseData = await apiClient.obtainAuthTokenPair(email, password);

    console.log(responseData);
    if (!responseData.success) {
      window.alert(responseData.error.user_friendly_message);
      setIsLoading(false);
      return;
    }

    window.alert("Login Successful");

    // set user

    setIsLoading(false);
  };

  useEffect(() => {
    document.title = `Login - ${appName}`;
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
        <SunriseLogo />
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

        <TextField
          placeholder="Your Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{
            width: "80%",
            maxWidth: "350px",
            marginBottom: 2,
          }}
        />

        <Button variant="contained" color="primary" onClick={handleLoginButtonClick} disabled={isLoading}>
          {isLoading ? <BeatLoader color="white" loading={true} size={10} /> : "Login"}
        </Button>

        <Box
          sx={{
            marginTop: 2,
            marginBottom: 1,
            width: "100%",
            borderBottom: "1px solid grey",
          }}
        />

        <Link href="/auth/get-signup-email">
          {userSelfRegistrationEnabled ? "Register A New Account" : "Registering a new account?"}
        </Link>

        <Link href="/auth/request-password-reset">Forgot Your Password?</Link>
      </Box>
    </Container>
  );
}
