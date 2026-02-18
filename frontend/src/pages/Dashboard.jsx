import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "../styles.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [createGroupName, setCreateGroupName] = useState("");
  const [joinGroupName, setJoinGroupName] = useState("");

  const handleCreate = () => {
    if (!createGroupName) return;
    navigate(`/chat/${createGroupName}`);
  };

  const handleJoin = () => {
    if (!joinGroupName) return;
    navigate(`/chat/${joinGroupName}`);
  };

  const handleLogout = () => {
    navigate("/");
  };

  return (
    <div className="page-container">

      <button onClick={handleLogout}>Logout</button>

      <h2>Create Group</h2>

      <div className="form-block">
        <label>Name</label>
        <input
          type="text"
          value={createGroupName}
          onChange={(e) => setCreateGroupName(e.target.value)}
        />

        <button onClick={handleCreate}>
          Create Group
        </button>
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

        <button onClick={handleJoin}>
          Join Group
        </button>
      </div>

    </div>
  );
}
