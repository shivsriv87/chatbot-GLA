import React, { useState } from 'react';
import Chatbot from './components/Chatbot';
import Navbar from './components/Navbar';
import './App.css';

function App() {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  return (
    <div className="App">
      <Navbar />
      <button className="chatbot-launcher" onClick={toggleChatbot}>
      </button>
      {isChatbotOpen && <Chatbot />}
    </div>
  );
}

export default App;
