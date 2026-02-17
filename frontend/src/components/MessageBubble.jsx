import React from "react";

export default function MessageBubble({ message }) {

  return (
    <div className={`bubble ${message.sender === "me" ? "me" : "other"}`}>
      <div>{message.text}</div>
      <small>{message.time}</small>
    </div>
  );
}
