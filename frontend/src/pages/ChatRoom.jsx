import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./chat.css";

export default function ChatRoom() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    setMessages([...messages, { text: input, sender: "me" }]);
    setInput("");
  };

  return (
    <div className="chat-app">
      <div className="sidebar">
        <div className="sidebar-header">Members</div>
        <div className="member">You</div>
      </div>

      <div className="chat-section">
        <div className="chat-header">
          <span>Group name : {id}</span>
          <button onClick={() => navigate("/")}>Logout</button>
        </div>

        <div className="messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender === "me" ? "me" : "other"}`}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="message-input">
          <input
            type="text"
            placeholder="Enter text..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}
