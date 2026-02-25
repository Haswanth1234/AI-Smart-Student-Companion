import React, { useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { sendMessage } from '../services/aiChatService';
import { Send, Bot, User } from 'lucide-react';

export default function AIChatPage() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    // Get user ID for unique storage key
    const getUserKey = () => {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                return `ai_chat_history_${user.id}`;
            } catch (e) {
                return 'ai_chat_history_guest';
            }
        }
        return 'ai_chat_history_guest';
    };

    const STORAGE_KEY = getUserKey();

    // Load messages on mount
    React.useEffect(() => {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            try {
                setMessages(JSON.parse(saved));
            } catch (e) {
                console.error("Failed to parse chat history");
            }
        } else {
            // Default welcome message
            setMessages([
                { sender: 'ai', text: 'Hello! I am your AI academic companion. How can I help you today?' }
            ]);
        }
    }, []);

    // Save messages on update
    React.useEffect(() => {
        if (messages.length > 0) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
        }
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = { sender: 'user', text: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const response = await sendMessage(userMsg.text);
            setMessages(prev => [...prev, { sender: 'ai', text: response.reply || "I'm processing that..." }]);
        } catch (err) {
            setMessages(prev => [...prev, { sender: 'ai', text: "Sorry, I'm having trouble connecting right now." }]);
        } finally {
            setLoading(false);
        }
    };

    const clearChat = () => {
        if (window.confirm("Are you sure you want to clear the chat history?")) {
            const initialMsg = [{ sender: 'ai', text: 'Hello! I am your AI academic companion. How can I help you today?' }];
            setMessages(initialMsg);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(initialMsg));
        }
    };

    return (
        <DashboardLayout title="AI Companion">
            <div className="flex-center h-full">
                <div className="glass-panel w-full" style={{ maxWidth: '800px', height: '80vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
                    {/* Chat Header */}
                    <div className="flex-between p-4" style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--glass-border)' }}>
                        <div className="flex-center gap-2">
                            <div className="flex-center" style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--primary-color)' }}>
                                <Bot size={24} color="white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg">AI Assistant</h3>
                                <p className="text-secondary text-xs">Always here to help</p>
                            </div>
                        </div>
                        <button
                            onClick={clearChat}
                            className="text-xs text-secondary hover:text-white transition-colors"
                            style={{ background: 'transparent', border: '1px solid var(--glass-border)', padding: '0.4rem 0.8rem', borderRadius: '8px', cursor: 'pointer' }}
                        >
                            Clear Chat
                        </button>
                    </div>

                    {/* Messages Area */}
                    <div style={{ flex: 1, padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        {messages.map((msg, idx) => (
                            <div key={idx} style={{
                                display: 'flex', gap: '1rem',
                                flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                                alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                                maxWidth: '85%'
                            }}>
                                <div style={{
                                    width: 36, height: 36, borderRadius: '50%', flexShrink: 0,
                                    background: msg.sender === 'user' ? 'var(--glass-border)' : 'var(--primary-color)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center'
                                }}>
                                    {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
                                </div>

                                <div style={{
                                    padding: '1rem 1.25rem',
                                    borderRadius: '18px',
                                    background: msg.sender === 'user' ? 'var(--primary-color)' : 'rgba(255,255,255,0.05)',
                                    border: msg.sender === 'ai' ? '1px solid var(--glass-border)' : 'none',
                                    borderTopRightRadius: msg.sender === 'user' ? '4px' : '18px',
                                    borderTopLeftRadius: msg.sender === 'ai' ? '4px' : '18px',
                                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                                }}>
                                    <p style={{ lineHeight: '1.6', fontSize: '0.95rem' }}>{msg.text}</p>
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex-center gap-2" style={{ alignSelf: 'flex-start', marginLeft: '3.5rem' }}>
                                <div className="typing-dot" style={{ animationDelay: '0s' }}></div>
                                <div className="typing-dot" style={{ animationDelay: '0.2s' }}></div>
                                <div className="typing-dot" style={{ animationDelay: '0.4s' }}></div>
                            </div>
                        )}
                    </div>

                    {/* Fixed Input Area */}
                    <div style={{ padding: '1.5rem', background: 'rgba(15, 23, 42, 0.4)', backdropFilter: 'blur(10px)', borderTop: '1px solid var(--glass-border)', borderBottomLeftRadius: '24px', borderBottomRightRadius: '24px' }}>
                        <form onSubmit={handleSend} className="relative flex-center gap-2">
                            <input
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                placeholder="Type your question..."
                                style={{
                                    flex: 1,
                                    background: 'rgba(0,0,0,0.3)',
                                    border: '1px solid var(--glass-border)',
                                    padding: '1rem 1.25rem',
                                    borderRadius: '12px',
                                    color: 'white',
                                    outline: 'none',
                                    transition: 'all 0.3s'
                                }}
                                onFocus={(e) => e.target.style.borderColor = 'var(--primary-color)'}
                                onBlur={(e) => e.target.style.borderColor = 'var(--glass-border)'}
                            />
                            <button type="submit" className="neon-btn" disabled={loading} style={{ padding: '1rem', borderRadius: '12px' }}>
                                <Send size={20} />
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
