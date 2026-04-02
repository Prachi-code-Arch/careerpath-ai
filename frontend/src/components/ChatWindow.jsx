import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../api";

const AGENT_COLORS = {
  coach_agent: "#6366f1",
  achievement_agent: "#10b981",
  skillbuild_agent: "#f59e0b",
  schedule_agent: "#3b82f6",
  orchestrator: "#8b5cf6"
};

const AGENT_LABELS = {
  coach_agent: "Coach",
  achievement_agent: "Achievement",
  skillbuild_agent: "Skill Builder",
  schedule_agent: "Scheduler",
  orchestrator: "Orchestrator"
};

export default function ChatWindow({ messages, setMessages, setActivityLog, setUserContext, loading, setLoading, profile }) {
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);
    setActivityLog([{ agent: "orchestrator", status: "thinking", preview: "Analyzing your message..." }]);
    try {
      const data = await sendMessage(profile.user_id, userMessage, sessionId);
      setSessionId(data.session_id);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: data.response,
        agents_called: data.agents_called || []
      }]);
      setActivityLog(data.activity_log || []);
      setUserContext(data.user_context || {});
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, something went wrong. Please try again.",
        agents_called: []
      }]);
    }
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="bubble">
              <p>{msg.content}</p>
              {msg.agents_called && msg.agents_called.length > 0 && (
                <div className="agents-used">
                  {msg.agents_called.map(agent => (
                    <span key={agent} className="agent-tag"
                      style={{ background: AGENT_COLORS[agent]+"22", color: AGENT_COLORS[agent], border: `1px solid ${AGENT_COLORS[agent]}44` }}>
                      {AGENT_LABELS[agent] || agent}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="input-area">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask Priya's career coach anything... (Enter to send)"
          rows={2}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
