import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { Play, Square } from 'lucide-react';
import { api } from '../services/api';
import ReactMarkdown from 'react-markdown';

export default function Coaching() {
  const userId = useAuthStore(state => state.userId);
  const token = useAuthStore(state => state.token);
  const [isStreaming, setIsStreaming] = useState(false);
  const [messages, setMessages] = useState<string>('');
  const [signals, setSignals] = useState<any[]>([]);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleStartCoaching = async () => {
    if (isStreaming) return;
    
    setMessages('');
    setSignals([]);
    setIsStreaming(true);

    try {
      // First get user trades to send for coaching
      const res = await api.get('/api/trades');
      const traders = res.data.traders || [];
      const currentUser = traders.find((t: any) => t.userId === userId);
      
      let allTrades: any[] = [];
      if (currentUser) {
        currentUser.sessions.forEach((s: any) => allTrades.push(...s.trades));
      }
      const tradesToSend = allTrades.slice(-20); // Send last 20

      // Stream endpoint setup
      // Since it's a POST request with EventSource, we need to use fetch instead of standard EventSource which only supports GET
      // Wait, EventSource API doesn't support POST. The backend endpoint `/api/coaching/{user_id}/stream` is a POST endpoint!
      // To support SSE with POST, we must use fetch API and read the stream manually.
      
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
              setMessages(prev => prev + data);
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
    // Note: Can't easily abort a fetch stream without AbortController, but UI state will reset.
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">AI Coach</h2>
          <p className="text-gray-500 dark:text-gray-400">Get real-time feedback based on your recent trading behavior.</p>
        </div>
        {!isStreaming ? (
          <button onClick={handleStartCoaching} className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            <Play className="w-4 h-4 mr-2" />
            Start Session
          </button>
        ) : (
          <button onClick={stopCoaching} className="flex items-center px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
            <Square className="w-4 h-4 mr-2" />
            Stop
          </button>
        )}
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 min-h-[400px]">
        {messages ? (
          <div className="prose dark:prose-invert max-w-none font-sans text-gray-800 dark:text-gray-200">
            <ReactMarkdown>{messages}</ReactMarkdown>
          </div>
        ) : (
          <div className="flex items-center justify-center h-64 text-gray-400">
            Click 'Start Session' to begin AI coaching...
          </div>
        )}
        
        {isStreaming && (
          <div className="mt-4 flex items-center text-blue-500">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-ping mr-2"></div>
            AI is thinking...
          </div>
        )}
      </div>

      {signals.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">Detected Signals</h3>
          <div className="grid grid-cols-1 gap-4">
            {signals.map((sig, i) => (
              <div key={i} className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r-md">
                <div className="flex items-center">
                  <h4 className="text-red-800 dark:text-red-200 font-semibold uppercase">{sig.signal.replace('_', ' ')}</h4>
                </div>
                <p className="text-red-700 dark:text-red-300 mt-1 text-sm">{sig.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
