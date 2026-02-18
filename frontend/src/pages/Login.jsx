import { useNavigate } from "react-router-dom";
import "../styles.css";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Login</h2>

        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />

        <button onClick={() => navigate("/dashboard")}>
          Login
        </button>

        <p className="auth-link">
          New user? Register
        </p>
      </div>
    </div>
  );
}
