import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./chat.css";

const API = import.meta.env.VITE_API_URL;
console.log("API URL =", API);

export default function ChatRoom() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const messageToSend = input;

    setMessages(prev => [
      ...prev,
      { text: messageToSend, sender: "me" }
    ]);

    setInput("");

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          group_id: id,
          username: "Sai",
          message: messageToSend
        })
      });

      const data = await res.json();
console.log("Backend response:", data);


      if (data.reply) {
        setMessages(prev => [
          ...prev,
          { text: data.reply, sender: "bot" }
        ]);
      }

    } catch (error) {
      setMessages(prev => [
        ...prev,
        { text: "Server error. Try again.", sender: "bot" }
      ]);
    }
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
