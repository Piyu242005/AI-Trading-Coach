import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { Play, Square, Bot, User, RefreshCcw } from 'lucide-react';
import { api } from '../services/api';
import ReactMarkdown from 'react-markdown';

export default function Coaching() {
  const userId = useAuthStore(state => state.userId);
  const token = useAuthStore(state => state.token);
  const [isStreaming, setIsStreaming] = useState(false);
  const [messages, setMessages] = useState<{role: 'user'|'assistant', content: string}[]>([]);
  const [signals, setSignals] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isStreaming]);

  const handleStartCoaching = async () => {
    if (isStreaming) return;
    
    // Initial Request
    setMessages([{ role: 'user', content: 'Please analyze my most recent trading session and identify any behavioral biases.' }]);
    setSignals([]);
    setIsStreaming(true);

    try {
      const res = await api.get('/api/trades');
      const traders = res.data.traders || [];
      const currentUser = traders.find((t: any) => t.userId === userId);
      
      let allTrades: any[] = [];
      if (currentUser) {
        currentUser.sessions.forEach((s: any) => allTrades.push(...s.trades));
      }
      const tradesToSend = allTrades.slice(-20); 

      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/coaching/${userId}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ trades: tradesToSend })
      });

      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      let buffer = '';
      
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          setIsStreaming(false);
          break;
        }
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        let currentEvent = '';
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.substring(7);
          } else if (line.startsWith('data: ')) {
            const data = line.substring(6);
            if (currentEvent === 'token') {
              setMessages(prev => {
                const newMsgs = [...prev];
                const last = newMsgs[newMsgs.length - 1];
                if (last.role === 'assistant') {
                  last.content += data;
                }
                return newMsgs;
              });
            } else if (currentEvent === 'summary') {
              setSignals(JSON.parse(data).signals || []);
            } else if (currentEvent === 'done') {
              setIsStreaming(false);
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setIsStreaming(false);
    }
  };

  const stopCoaching = () => {
    setIsStreaming(false);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 flex flex-col h-[calc(100vh-8rem)]">
      <div className="flex justify-between items-center bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-4">
          <div className="bg-blue-100 dark:bg-blue-900/30 p-3 rounded-xl">
            <Bot className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">AI Coach Chat</h2>
            <p className="text-gray-500 dark:text-gray-400">ChatGPT-powered behavioral analysis</p>
          </div>
        </div>
        <div className="flex gap-3">
          {messages.length > 0 && !isStreaming && (
            <button onClick={() => {setMessages([]); setSignals([])}} className="flex items-center px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 dark:text-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors font-semibold">
              <RefreshCcw className="w-4 h-4 mr-2" /> Reset
            </button>
          )}
          {!isStreaming ? (
            <button onClick={handleStartCoaching} className="flex items-center px-6 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 shadow-md transition-all">
              <Play className="w-4 h-4 mr-2 fill-current" />
              {messages.length === 0 ? "Start Session" : "Analyze Again"}
            </button>
          ) : (
            <button onClick={stopCoaching} className="flex items-center px-6 py-2 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700 shadow-md transition-all">
              <Square className="w-4 h-4 mr-2 fill-current" />
              Stop Analysis
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900/50 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-inner relative">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-400 space-y-4">
            <Bot className="w-16 h-16 opacity-20" />
            <p className="text-lg">Click 'Start Session' to generate an analysis of your recent trades.</p>
          </div>
        ) : (
          <div className="space-y-6 pb-20">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'assistant' && (
                  <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-md">
                    <Bot className="w-6 h-6 text-white" />
                  </div>
                )}
                
                <div className={`max-w-[80%] rounded-2xl px-6 py-4 shadow-sm ${msg.role === 'user' ? 'bg-gray-900 text-white dark:bg-gray-100 dark:text-gray-900 rounded-tr-sm' : 'bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-tl-sm text-gray-800 dark:text-gray-200'}`}>
                  {msg.role === 'user' ? (
                    <p className="text-sm sm:text-base font-medium">{msg.content}</p>
                  ) : (
                    <div className="prose dark:prose-invert max-w-none text-sm sm:text-base">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  )}
                </div>

                {msg.role === 'user' && (
                  <div className="w-10 h-10 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center flex-shrink-0 shadow-md">
                    <User className="w-6 h-6 text-gray-600 dark:text-gray-300" />
                  </div>
                )}
              </div>
            ))}
            
            {isStreaming && (
              <div className="flex gap-4 justify-start">
                <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-md">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div className="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl rounded-tl-sm px-6 py-4 flex items-center gap-2 shadow-sm">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {signals.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Detected Bias Signals</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {signals.map((sig, i) => (
              <div key={i} className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r-xl">
                <h4 className="text-red-800 dark:text-red-200 font-bold uppercase mb-1">{sig.signal.replace('_', ' ')}</h4>
                <p className="text-red-700 dark:text-red-300 text-sm leading-relaxed">{sig.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
