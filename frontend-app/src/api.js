const API_URL = "https://careerpath-backend-66798922244.us-central1.run.app";

export const sendMessage = async (userId, message, sessionId) => {
  try {
    const res = await fetch(API_URL + "/chat", {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message: message, session_id: sessionId || null })
    });
    const data = await res.json();
    return data;
  } catch(e) {
    console.error("Error:", e);
    throw e;
  }
};

export const createProfile = async (profile) => {
  const res = await fetch(API_URL + "/profile", {
    method: "POST",
    mode: "cors", 
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile)
  });
  return res.json();
};
