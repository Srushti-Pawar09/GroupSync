import { useParams } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import React from "react";

export default function ChatRoom() {
  const { groupId } = useParams();

  return (
    <div className="chat-layout">
      <Sidebar />
      <ChatWindow groupId={groupId} />
    </div>
  );
}
