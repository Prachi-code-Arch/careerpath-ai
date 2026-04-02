import axios from "axios";

const API_URL = "https://careerpath-backend-66798922244.us-central1.run.app";

export const sendMessage = async (userId, message, sessionId) => {
  const response = await axios.post(`${API_URL}/chat`, {
    user_id: userId,
    message,
    session_id: sessionId || null
  });
  return response.data;
};

export const createProfile = async (profile) => {
  const response = await axios.post(`${API_URL}/profile`, profile);
  return response.data;
};
