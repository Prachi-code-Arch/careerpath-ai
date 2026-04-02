import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import AgentFeed from "./components/AgentFeed";
import ProfileCard from "./components/ProfileCard";
import "./App.css";

const PRIYA = {
  user_id: "priya_001",
  name: "Priya Sharma",
  role: "Software Engineer",
  company: "TCS",
  city: "Delhi",
  years_exp: 3,
  first_gen: true,
  mentor: false
};

function App() {
  const [messages, setMessages] = useState([{
    role: "assistant",
    content: "Hi Priya! I'm CareerPath AI — your personal career coach. I have 4 specialist agents ready to help you with coaching, achievements, skill building, and scheduling. What's on your mind today?",
    agents_called: []
  }]);
  const [activityLog, setActivityLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userContext, setUserContext] = useState({ wins_logged: 0, active_goals: 0 });

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <span className="logo">CareerPath AI</span>
          <span className="tagline">Multi-Agent Career Coach</span>
        </div>
        <div className="header-right">
          <span className="badge">4 Agents Active</span>
          <span className="badge green">Live on Google Cloud</span>
        </div>
      </header>
      <div className="main">
        <div className="sidebar-left">
          <ProfileCard profile={PRIYA} userContext={userContext} />
        </div>
        <div className="chat-area">
          <ChatWindow
            messages={messages}
            setMessages={setMessages}
            setActivityLog={setActivityLog}
            setUserContext={setUserContext}
            loading={loading}
            setLoading={setLoading}
            profile={PRIYA}
          />
        </div>
        <div className="sidebar-right">
          <AgentFeed activityLog={activityLog} loading={loading} />
        </div>
      </div>
    </div>
  );
}

export default App;
