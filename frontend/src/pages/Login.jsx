import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUsers, saveUsers } from "../utils/storage";

export default function Login(props) {
  const setUser = props?.setUser;


  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = () => {

    if (!username || !password) return alert("Fill all fields");

    const users = getUsers();

    if (isRegister) {
      const exists = users.find(u => u.username === username);
      if (exists) return alert("Username already exists");

      users.push({ username, password });
      saveUsers(users);

      localStorage.setItem("currentUser", username);
      navigate("/dashboard");

    } else {
      const user = users.find(
        u => u.username === username && u.password === password
      );

      if (!user) return alert("Invalid credentials");

      localStorage.setItem("currentUser", username);
if (setUser) setUser(username);

navigate("/dashboard");

    }
  };

  return (
    <div className="auth-container">

      <div className="auth-card">

        <h2>{isRegister ? "Register" : "Login"}</h2>

        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleSubmit}>
          {isRegister ? "Register" : "Login"}
        </button>

        <p onClick={() => setIsRegister(!isRegister)} className="toggle">
          {isRegister ? "Already have account? Login" : "New user? Register"}
        </p>

      </div>
    </div>
  );
}
