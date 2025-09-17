import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProjectHistory, askQuestion } from '../api/apiClient';
import { ArrowLeft, PaperPlaneRight } from "@phosphor-icons/react";

const ChatBubble = ({ message, isUser }) => (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className={`max-w-xl px-4 py-3 rounded-xl shadow-md ${isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800'}`}>
            <p style={{ whiteSpace: 'pre-wrap' }}>{message}</p>
        </div>
    </div>
);

const ProjectChatPage = () => {
    const { projectId } = useParams();
    console.log("Project ID:", projectId); // Debugging line
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        const fetchHistory = async () => {
            setIsLoading(true);
            try {
                const response = await getProjectHistory(projectId);
                const historyMessages = response.data.flatMap(item => [
                    { text: item.question, isUser: true },
                    { text: item.answer, isUser: false }
                ]);
                setMessages(historyMessages);
            } catch (error) {
                console.error("Failed to fetch project history:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchHistory();
    }, [projectId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { text: input, isUser: true };
        console.log("Sending message:", userMessage); // Debugging line
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await askQuestion(projectId, input);
            const aiMessage = { text: response.data.answer, isUser: false };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error("Failed to send message:", error);
            const errorMessage = { text: "Sorry, I encountered an error. Please try again.", isUser: false };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-100">
            <header className="bg-white shadow-md p-4 flex items-center">
                <Link to="/" className="text-blue-500 hover:text-blue-700 mr-4">
                    <ArrowLeft size={24} />
                </Link>
                <h1 className="text-xl font-bold text-gray-800">Project Chat</h1>
            </header>
            
            <main className="flex-1 overflow-y-auto p-6">
                <div className="max-w-4xl mx-auto">
                    {messages.map((msg, index) => (
                        <ChatBubble key={index} message={msg.text} isUser={msg.isUser} />
                    ))}
                    {isLoading && <ChatBubble message="Thinking..." isUser={false} />}
                    <div ref={messagesEndRef} />
                </div>
            </main>
            
            <footer className="bg-white border-t p-4">
                <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question about the codebase..."
                        className="flex-1 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />
                    <button 
                        type="submit" 
                        className="ml-4 bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 disabled:bg-blue-300"
                        disabled={isLoading}
                    >
                        <PaperPlaneRight size={24} />
                    </button>
                </form>
            </footer>
        </div>
    );
};

export default ProjectChatPage;
