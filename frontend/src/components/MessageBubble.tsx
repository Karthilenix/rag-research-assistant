import React, { useState } from 'react';
import { User, Bot, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import type { Message } from '../types';
import ReactMarkdown from 'react-markdown';

interface MessageBubbleProps {
    message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';
    const [isSourcesOpen, setIsSourcesOpen] = useState(false);

    return (
        <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`flex max-w-[80%] md:max-w-[70%] ${isUser ? 'flex-row-reverse' : 'flex-row'
                    } items-start gap-4`}
            >
                <div
                    className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center 
            ${isUser ? 'bg-blue-600 text-white' : 'bg-gray-100 text-blue-600 border border-gray-200'}`}
                >
                    {isUser ? <User size={20} /> : <Bot size={20} />}
                </div>

                <div className="flex flex-col">
                    <div
                        className={`px-6 py-4 rounded-2xl shadow-sm text-sm leading-relaxed
              ${isUser
                                ? 'bg-blue-600 text-white rounded-tr-none'
                                : 'bg-white border border-gray-100 text-gray-800 rounded-tl-none prose prose-sm max-w-none'}`}
                    >
                        {isUser ? (
                            <span className="whitespace-pre-wrap">{message.content}</span>
                        ) : (
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                        )}
                    </div>

                    {!isUser && message.citations && message.citations.length > 0 && (
                        <div className="mt-2 text-xs text-gray-500 pl-2">
                            <button
                                onClick={() => setIsSourcesOpen(!isSourcesOpen)}
                                className="flex items-center gap-1 font-semibold text-blue-600 hover:text-blue-700 transition-colors mb-2"
                            >
                                {isSourcesOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                                {isSourcesOpen ? 'Hide Sources' : 'Show Sources'} ({(message.citations || []).length})
                            </button>

                            {isSourcesOpen && (
                                <div className="p-3 bg-gray-50 rounded-lg border border-gray-100 animate-in fade-in slide-in-from-top-1 duration-200">
                                    <div className="font-semibold mb-2 flex items-center gap-1 text-gray-700">
                                        <FileText size={12} />
                                        Reference Context:
                                    </div>
                                    <ul className="list-disc list-inside space-y-2">
                                        {message.citations.map((citation, idx) => (
                                            <li key={idx} className="text-[11px] leading-relaxed opacity-80 bg-white p-2 rounded border border-gray-100">
                                                {citation.trim().slice(0, 300)}...
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    <span className={`text-[10px] mt-1 px-1 ${isUser ? 'text-right text-gray-400' : 'text-left text-gray-400'}`}>
                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default MessageBubble;
