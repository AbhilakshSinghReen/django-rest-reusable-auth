import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import LinearProgress from "@mui/material/LinearProgress";
import Skeleton from "@mui/material/Skeleton";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import { BeatLoader } from "react-spinners";
import { CSSTransition } from "react-transition-group";

import apiClient from "../../api/apiClient";
import { appName } from "../../config/config";
import SunriseLogo from "../../components/SunriseLogo";

export default function CompleteSignup() {
  const navigate = useNavigate();
  const { userInviteToken } = useParams();

  const [isVerifyingToken, setIsVerifyingToken] = useState(true);
  const [isRegistrationTokenValid, setisRegistrationTokenValid] = useState(false);
  const [tokenVerificationResultMessage, setTokenVerificationResultMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSignupCompleted, setHasSignupCompleted] = useState(false);
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const verifyInviteTokenAndGetUserData = async () => {
    const responseData = await apiClient.getUserDataFromInviteToken(userInviteToken);
    console.log(responseData);

    if (!responseData.success) {
      window.alert(responseData.error.user_friendly_message);

      if (responseData.error.user_friendly_message !== "Server Error.") {
        setTokenVerificationResultMessage(responseData.error.user_friendly_message);
        setisRegistrationTokenValid(false);
      }

      setIsVerifyingToken(false);
      return;
    }

    setEmail(responseData.result.user_invite.email);

    setisRegistrationTokenValid(true);
    setIsVerifyingToken(false);
  };

  const handleRegisterButtonClick = async (_e) => {
    setIsLoading(true);

    if (password !== confirmPassword) {
      window.alert("Passwords do not match.");
      setIsLoading(false);
      return;
    }

    const responseData = await apiClient.signupUsingInviteToken(userInviteToken, email, fullName, password);
    if (!responseData.success) {
      window.alert(responseData.error.user_friendly_message);
      setIsLoading(false);
      return;
    }

    setIsLoading(false);
    setHasSignupCompleted(true);

    setTimeout(() => {
      navigate("/auth/signin");
    }, 2500);
  };

  useEffect(() => {
    document.title = `Register Your Account - ${appName}`;

    verifyInviteTokenAndGetUserData();
  }, []);

  if (isVerifyingToken) {
    return (
      <Box
        sx={{
          width: "100%",
          position: "absolute",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          alignItems: "center",
          marginTop: 1,
        }}
      >
        <Skeleton variant="circular" width={192} height={192} animation="wave" />
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
          <Skeleton
            variant="text"
            animation="wave"
            sx={{
              width: "250px",
              height: 50,
            }}
          />
        </Box>

        <Skeleton
          variant="text"
          animation="wave"
          sx={{
            width: "80%",
            height: 50,
            maxWidth: "350px",
          }}
        />

        <Skeleton
          variant="text"
          animation="wave"
          sx={{
            width: "80%",
            height: 50,
            maxWidth: "350px",
          }}
        />

        <Skeleton
          variant="text"
          animation="wave"
          sx={{
            width: "80%",
            height: 50,
            maxWidth: "350px",
          }}
        />

        <Skeleton
          variant="text"
          animation="wave"
          sx={{
            width: "80%",
            height: 50,
            maxWidth: "350px",
          }}
        />

        <Skeleton
          variant="text"
          animation="wave"
          sx={{
            width: "100px",
            height: 50,
          }}
        />
      </Box>
    );
  }

  if (!isRegistrationTokenValid) {
    return (
      <Box
        sx={{
          width: "100%",
          position: "absolute",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          alignItems: "center",
          marginTop: 1,
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
            <strong>The Registration Link is Invalid.</strong>
          </Typography>
          <Box
            sx={{
              width: "80%",
              borderBottom: "1px solid grey",
            }}
          />

          <Typography variant="h6">{tokenVerificationResultMessage}</Typography>
        </Box>
      </Box>
    );
  }

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
      <CSSTransition in={!hasSignupCompleted} timeout={500} classNames="fade" unmountOnExit>
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
          <Tooltip title="You can't edit this, the registration link is tied to your email!">
            <TextField
              placeholder="Your Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={true}
              sx={{
                width: "80%",
                maxWidth: "350px",
                marginBottom: 2,
              }}
            />
          </Tooltip>

          <TextField
            placeholder="Your Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            sx={{
              width: "80%",
              maxWidth: "350px",
              marginBottom: 2,
            }}
          />

          <TextField
            placeholder="A Strong Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{
              width: "80%",
              maxWidth: "350px",
              marginBottom: 2,
            }}
          />

          <TextField
            placeholder="Confirm your Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            sx={{
              width: "80%",
              maxWidth: "350px",
              marginBottom: 2,
            }}
          />

          <Button variant="contained" color="primary" onClick={handleRegisterButtonClick} disabled={isLoading}>
            {isLoading ? <BeatLoader color="white" loading={true} size={10} /> : "Register"}
          </Button>
        </Box>
      </CSSTransition>
      <CSSTransition in={hasSignupCompleted} timeout={500} classNames="fade" unmountOnExit>
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
              <strong>Registration Complete</strong>
            </Typography>
            <Box
              sx={{
                width: "80%",
                borderBottom: "1px solid grey",
              }}
            />
          </Box>
          <Typography variant="body1">Redirecting you to the Login Page ...</Typography>
          <Box
            sx={{
              width: "100%",
              marginTop: 2,
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-start",
              alignItems: "center",
            }}
          >
            <LinearProgress
              color="warning"
              variant="indeterminate"
              sx={{
                width: "80%",
                maxWidth: "350px",
                height: "5px",
              }}
            />
          </Box>
        </Box>
      </CSSTransition>
    </Container>
  );
}
