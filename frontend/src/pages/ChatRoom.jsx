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

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      { text: userMessage, sender: "me" }
    ]);

    setInput("");

    try {
      console.log("Sending to:", API);

      await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      const res = await fetch(`${API}/recommend`, {
        method: "POST"
      });

      const data = await res.json();

      console.log("Recommendation response:", data);

      if (data.recommendations?.length > 0) {
        const top = data.recommendations[0];

        setMessages((prev) => [
          ...prev,
          {
            text: `Suggested city: ${top.city}
Days: ${top.suggested_days}
Cost per person: ₹${top.total_cost_per_person}`,
            sender: "bot"
          }
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { text: "No matching destinations found.", sender: "bot" }
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
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
