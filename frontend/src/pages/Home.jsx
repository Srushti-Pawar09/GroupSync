import { useNavigate } from "react-router-dom";
import "../styles.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Welcome to GroupSync</h1>
        <p>Your personalized group trip planner.</p>

        <button onClick={() => navigate("/login")}>
          Login / Register
        </button>
      </div>
    </div>
  );
}
