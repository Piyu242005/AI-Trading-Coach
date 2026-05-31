import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { BookOpen } from 'lucide-react';

export default function Journal() {
  const userId = useAuthStore(state => state.userId);

  const { data, isLoading, error } = useQuery({
    queryKey: ['trades', userId],
    queryFn: async () => {
      const res = await api.get('/api/trades');
      return res.data;
    },
    enabled: !!userId,
  });

  if (isLoading) return <div className="p-8 text-center text-gray-500">Loading journal...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Error loading journal data</div>;

  const traders = data?.traders || [];
  const currentUser = traders.find((t: any) => t.userId === userId);
  
  if (!currentUser) return <div className="p-8 text-red-500">User not found in dataset.</div>;

  let allTrades: any[] = [];
  currentUser.sessions.forEach((s: any) => allTrades.push(...s.trades));
  allTrades.sort((a, b) => new Date(b.entryAt).getTime() - new Date(a.entryAt).getTime()); // Newest first

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
            <BookOpen className="w-7 h-7 mr-3 text-blue-500" />
            Trade Journal
          </h2>
          <p className="text-gray-500 mt-1">Review your psychological state and rationale for each trade.</p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-900/50">
              <tr>
                <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Date & Time</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Asset</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">P&L</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Emotion</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Rationale & Notes</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {allTrades.map((trade, idx) => (
                <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {new Date(trade.entryAt).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${trade.direction === 'LONG' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'}`}>
                        {trade.direction}
                      </span>
                      <span className="ml-2 text-sm font-medium text-gray-900 dark:text-white">{trade.asset}</span>
                    </div>
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm font-bold ${trade.pnl >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                    ${trade.pnl.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                      {trade.emotionalState || 'Neutral'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 max-w-xs truncate">
                    {trade.entryRationale || <span className="text-gray-400 italic">No notes provided</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
