import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "../styles.css";

export default function Login() {
  const navigate = useNavigate();
  const [isRegister, setIsRegister] = useState(false);

  const handleSubmit = () => {
    // For now just redirect
    navigate("/dashboard");
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>{isRegister ? "Register" : "Login"}</h2>

        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />

        <button onClick={handleSubmit}>
          {isRegister ? "Register" : "Login"}
        </button>

        <p
          className="auth-link"
          onClick={() => setIsRegister(!isRegister)}
        >
          {isRegister
            ? "Already have an account? Login"
            : "New user? Register"}
        </p>
      </div>
    </div>
  );
}
