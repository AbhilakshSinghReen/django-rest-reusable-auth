import axiosInstance from "./axiosInstance";
import apiEndpoints from "./apiEndpoints";

class APIClient {
  constructor() {
    this.requestMethods = {
      GET: axiosInstance.get,
      POST: axiosInstance.post,
      PUT: axiosInstance.put,
      PATCH: axiosInstance.patch,
      DELETE: axiosInstance.delete,
    };

    this.badResponse = {
      success: false,
      error: {
        user_friendly_message: "Server Error.",
      },
    };
  }

  async makeRequest(method, url, body = {}, headers = {}, addAuth = false) {
    if (addAuth) {
      // Refresh Access token if required
      // Add Auth header
    }

    try {
      const response = await this.requestMethods[method](url, body, headers);
      const responseData = await response.data;
      return responseData;
    } catch (error) {
      if (!error.response) {
        return this.badResponse;
      }

      const contentType = error.response.headers["content-type"];
      if (!contentType || !contentType.includes("application/json")) {
        return this.badResponse;
      }

      const responseData = await error.response.data;
      return responseData;
    }
  }

  async requestEmailUserInvite(email) {
    const requestBody = {
      email: email,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.requestEmailUserInvite(), requestBody);
  }

  async getUserDataFromInviteToken(inviteToken) {
    const requestBody = {
      token: inviteToken,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.getUserDataFromInviteToken(), requestBody);
  }

  async signupUsingInviteToken(inviteToken, email, fullName, password) {
    const requestBody = {
      token: inviteToken,
      email: email,
      full_name: fullName,
      password: password,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.signupUsingInviteToken(), requestBody);
  }

  async requestPasswordResetViaEmail(email) {
    const requestBody = {
      email: email,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.requestPasswordResetViaEmail(), requestBody);
  }

  async getUserDataFromPasswordResetToken(passwordResetToken) {
    const requestBody = {
      token: passwordResetToken,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.getUserDataFromPasswordResetToken(), requestBody);
  }

  async resetPasswordUsingPasswordResetToken(passwordResetToken, email, newPassword) {
    const requestBody = {
      token: passwordResetToken,
      email: email,
      new_password: newPassword,
    };

    return await this.makeRequest("POST", apiEndpoints.auth.resetPasswordUsingPasswordResetToken(), requestBody);
  }

  async obtainAuthTokenPair() {}

  async refreshAccessToken() {}

  async blacklistRefreshToken() {}
}

const apiClient = new APIClient();
export default apiClient;
