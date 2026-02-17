import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getGroups, saveGroups } from "../utils/storage";

export default function Dashboard() {

  const [groupName, setGroupName] = useState("");
  const [groupPass, setGroupPass] = useState("");
  const navigate = useNavigate();

  const createGroup = () => {

    if (!groupName || !groupPass) return alert("Fill all fields");

    const groups = getGroups();
    const exists = groups.find(g => g.name === groupName);

    if (exists) return alert("Group already exists");

    const newGroup = {
      id: Date.now(),
      name: groupName,
      password: groupPass
    };

    groups.push(newGroup);
    saveGroups(groups);

    navigate(`/chat/${newGroup.id}`);
  };

  const joinGroup = () => {

    const groups = getGroups();
    const group = groups.find(
      g => g.name === groupName && g.password === groupPass
    );

    if (!group) return alert("Invalid group credentials");

    navigate(`/chat/${group.id}`);
  };

  return (
    <div className="dashboard">

      <h2>Welcome {localStorage.getItem("currentUser")}</h2>

      <div className="group-box">
        <h3>Create Group</h3>

        <input
          placeholder="Group Name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
        />

        <input
          type="password"
          placeholder="Group Password"
          value={groupPass}
          onChange={(e) => setGroupPass(e.target.value)}
        />

        <button onClick={createGroup}>Create</button>
      </div>

      <div className="group-box">
        <h3>Join Group</h3>
        <button onClick={joinGroup}>Join</button>
      </div>

    </div>
  );
}
