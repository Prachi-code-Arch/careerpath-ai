export default function ProfileCard({ profile, userContext }) {
  return (
    <div className="profile-card">
      <div className="avatar">
        {profile.name.split(" ").map(n => n[0]).join("")}
      </div>
      <div className="profile-name">{profile.name}</div>
      <div className="profile-role">{profile.role}</div>
      <div className="profile-company">{profile.company} · {profile.city}</div>
      <div className="profile-stats">
        <div className="stat">
          <div className="stat-value">{profile.years_exp}</div>
          <div className="stat-label">Years exp</div>
        </div>
        <div className="stat">
          <div className="stat-value">{userContext.wins_logged || 0}</div>
          <div className="stat-label">Wins logged</div>
        </div>
        <div className="stat">
          <div className="stat-value">{userContext.active_goals || 0}</div>
          <div className="stat-label">Active goals</div>
        </div>
      </div>
      <div className="profile-tags">
        {profile.first_gen && <span className="tag">First-gen</span>}
        {!profile.mentor && <span className="tag">No mentor</span>}
        <span className="tag green">APAC</span>
      </div>
      <div className="demo-label">Demo Persona</div>
    </div>
  );
}
