import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';
import chatLogo from './chat_logo-_2_.png';  // Ensure this path is correct based on your structure

function Chatbox() {
    const [isActive, setIsActive] = useState(false);
    const [messages, setMessages] = useState([
        { type: "operator", text: "Hello! Welcome to GLA University Chatbot. How can I assist you today?" }
    ]);
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (input.trim() !== "") {
            const userMessage = { type: "visitor", text: input };
            setMessages(prevMessages => [...prevMessages, userMessage]);
            setInput("");

            try {
                const response = await axios.post('http://127.0.0.1:5000/predict', { message: input });
                const botMessage = { type: "operator", text: response.data.answer };
                setMessages(prevMessages => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending message to chatbot:', error);
            }
        }
    };

    const renderMessageText = (text) => {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.split(urlRegex).map((part, index) => {
            if (part.match(urlRegex)) {
                return <a key={index} href={part} target="_blank" rel="noopener noreferrer">{part}</a>;
            }
            return part;
        });
    };

    return (
        <div className="chatbox">
            <div className={`chatbox__support ${isActive ? 'chatbox--active' : ''}`}>
                <div className="chatbox__header">
                    <div className="chatbox__image--header">
                        <img src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-5--v1.png" alt="User" />
                    </div>
                    <div className="chatbox__content--header">
                        <h4 className="chatbox__heading--header">Chat support</h4>
                        <p className="chatbox__description--header">Hi. I am GLA CHATBOT How can I help you?</p>
                    </div>
                    <button className="chatbox__close--header" onClick={() => setIsActive(false)}>
                        &times;
                    </button>
                </div>
                <div className="chatbox__messages">
                    {messages.map((message, index) => (
                        <div key={index} className={`messages__item messages__item--${message.type}`}>
                            {renderMessageText(message.text)}
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>
                <div className="chatbox__footer">
                    <input
                        type="text"
                        placeholder="Write a message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <button className="chatbox__send--footer send__button" onClick={sendMessage}>
                        <i className="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
            <div className="chatbox__button" onClick={() => setIsActive(!isActive)}>
                <button><img src={chatLogo} alt="Chat" /></button>
            </div>
        </div>
    );
}

export default Chatbox;
