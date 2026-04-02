const AGENT_COLORS = {
  coach_agent: "#6366f1",
  achievement_agent: "#10b981",
  skillbuild_agent: "#f59e0b",
  schedule_agent: "#3b82f6",
  orchestrator: "#8b5cf6"
};

const AGENT_ICONS = {
  coach_agent: "🧠",
  achievement_agent: "🏆",
  skillbuild_agent: "📚",
  schedule_agent: "📅",
  orchestrator: "⚡"
};

export default function AgentFeed({ activityLog, loading }) {
  return (
    <div className="agent-feed">
      <div className="feed-header">
        <span>Agent Activity</span>
        {loading && <span className="pulse">●</span>}
      </div>
      <div className="agents-list">
        {["orchestrator","coach_agent","achievement_agent","skillbuild_agent","schedule_agent"].map(agent => {
          const activity = activityLog.find(a => a.agent === agent);
          return (
            <div key={agent} className={`agent-card ${activity ? "active" : ""}`}>
              <div className="agent-icon" style={{ background: AGENT_COLORS[agent] + "22" }}>
                {AGENT_ICONS[agent]}
              </div>
              <div className="agent-info">
                <div className="agent-name" style={{ color: AGENT_COLORS[agent] }}>
                  {agent.replace("_agent","").replace("_"," ")}
                </div>
                <div className="agent-status">
                  {activity ? (
                    <span className="status-done">✓ {activity.status}</span>
                  ) : loading && agent === "orchestrator" ? (
                    <span className="status-thinking">thinking...</span>
                  ) : (
                    <span className="status-idle">idle</span>
                  )}
                </div>
                {activity?.preview && (
                  <div className="agent-preview">{activity.preview.slice(0,60)}...</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      <div className="feed-footer">
        <small>Powered by Vertex AI + Gemini</small>
      </div>
    </div>
  );
}
