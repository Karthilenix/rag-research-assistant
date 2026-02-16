
import React from 'react';
import { User, Bot, FileText } from 'lucide-react';
import type { Message } from '../types';

interface MessageBubbleProps {
    message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';

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
                        className={`px-6 py-4 rounded-2xl shadow-sm text-sm leading-relaxed whitespace-pre-wrap
              ${isUser
                                ? 'bg-blue-600 text-white rounded-tr-none'
                                : 'bg-white border border-gray-100 text-gray-800 rounded-tl-none'}`}
                    >
                        {message.content}
                    </div>

                    {!isUser && message.citations && message.citations.length > 0 && (
                        <div className="mt-2 text-xs text-gray-500 pl-2">
                            <div className="font-semibold mb-1 flex items-center gap-1">
                                <FileText size={12} />
                                Sources:
                            </div>
                            <ul className="list-disc list-inside space-y-1">
                                {message.citations.map((citation, idx) => (
                                    <li key={idx} className="truncate max-w-xs opacity-80 hover:opacity-100 transition-opacity">
                                        {citation.trim()}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <span className={`text-[10px] mt-1 px-1 ${isUser ? 'text-right text-gray-400' : 'text-left text-gray-400'}`}>
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default MessageBubble;
