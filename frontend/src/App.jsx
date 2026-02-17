import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ChatRoom from "./pages/ChatRoom";
import React from "react";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/chat/:groupId" element={<ChatRoom />} />
    </Routes>
  );
}
