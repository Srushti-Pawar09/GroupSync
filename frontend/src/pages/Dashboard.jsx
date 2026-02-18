import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "../styles.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [createGroupName, setCreateGroupName] = useState("");
  const [createPassword, setCreatePassword] = useState("");

  const [joinGroupName, setJoinGroupName] = useState("");
  const [joinPassword, setJoinPassword] = useState("");

  const handleCreate = () => {
    if (!createGroupName.trim() || !createPassword.trim()) {
      alert("Group name and password required");
      return;
    }

    navigate(`/chat/${createGroupName}`);
  };

  const handleJoin = () => {
    if (!joinGroupName.trim() || !joinPassword.trim()) {
      alert("Group name and password required");
      return;
    }

    navigate(`/chat/${joinGroupName}`);
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate("/")}>Logout</button>

      <h2>Create Group</h2>
      <div className="form-block">
        <label>Name</label>
        <input
          type="text"
          value={createGroupName}
          onChange={(e) => setCreateGroupName(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          value={createPassword}
          onChange={(e) => setCreatePassword(e.target.value)}
        />

        <button onClick={handleCreate}>Create Group</button>
      </div>

      <p>Or</p>

      <h2>Join Group</h2>
      <div className="form-block">
        <label>Name</label>
        <input
          type="text"
          value={joinGroupName}
          onChange={(e) => setJoinGroupName(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          value={joinPassword}
          onChange={(e) => setJoinPassword(e.target.value)}
        />

        <button onClick={handleJoin}>Join Group</button>
      </div>
    </div>
  );
}
