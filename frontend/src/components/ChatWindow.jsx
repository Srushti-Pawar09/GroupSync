import { useState } from "react";
import MessageBubble from "./MessageBubble";
import MessageInput from "./MessageInput";

export default function ChatWindow({ groupId }) {

  const [messages, setMessages] = useState([]);

  const sendMessage = (text) => {
    const newMsg = {
      id: Date.now(),
      text,
      time: new Date().toLocaleTimeString(),
      sender: "me"
    };

    setMessages((prev) => [...prev, newMsg]);
  };

  return (
    <div className="chat-window">

      <div className="chat-header">
        Group ID: {groupId}
      </div>

      <div className="messages">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>

      <MessageInput onSend={sendMessage} />

    </div>
  );
}
