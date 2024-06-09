const appName = "M.I.D.R.E.A.M.";

const urlParser = new URL(window.location.href);
const urlOrigin = urlParser.origin;

let apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
let mediaBaseUrl = process.env.REACT_APP_MEDIA_BASE_URL;

if (!process.env.REACT_APP_API_BASE_URL) {
  apiBaseUrl = urlOrigin + "/api/v1";
  console.warn(`Environment variable REACT_APP_API_BASE_URL not defined, will default to ${apiBaseUrl}`);
}

if (!process.env.REACT_APP_MEDIA_BASE_URL) {
  mediaBaseUrl = urlOrigin + "/media";
  console.warn(`Environment variable REACT_APP_MEDIA_BASE_URL not defined, will default to ${mediaBaseUrl}`);
}

const userSelfRegistrationEnabled = process.env.REACT_APP_USER_SELF_REGISTRATION_ENABLED === "true";

export { appName, apiBaseUrl, mediaBaseUrl, userSelfRegistrationEnabled };
