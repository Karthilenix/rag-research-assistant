
export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    citations?: string[];
    timestamp: Date;
}

export interface QueryResponse {
    answer: string;
    context: string[];
}
