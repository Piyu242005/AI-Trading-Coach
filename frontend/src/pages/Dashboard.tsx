import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const userId = useAuthStore(state => state.userId);

  const { data, isLoading, error } = useQuery({
    queryKey: ['trades'],
    queryFn: async () => {
      const res = await api.get('/api/trades');
      return res.data;
    }
  });

  if (isLoading) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Error loading dashboard</div>;

  const traders = data?.traders || [];
  const currentUser = traders.find((t: any) => t.userId === userId);
  
  if (!currentUser) return <div className="p-8 text-red-500">User not found in dataset. Make sure you used a valid User ID from the dataset.</div>;

  let allTrades: any[] = [];
  currentUser.sessions.forEach((s: any) => allTrades.push(...s.trades));
  allTrades.sort((a, b) => new Date(a.entryAt).getTime() - new Date(b.entryAt).getTime());

  let currentPnl = 0;
  const chartData = allTrades.map(t => {
    currentPnl += t.pnl;
    return { time: new Date(t.entryAt).toLocaleTimeString(), pnl: currentPnl, trade: t };
  });

  const totalTrades = allTrades.length;
  const wins = allTrades.filter(t => t.outcome === 'win').length;
  const winRate = totalTrades ? ((wins / totalTrades) * 100).toFixed(1) : '0.0';

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Total Trades</h3>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{totalTrades}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Win Rate</h3>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400 mt-2">{winRate}%</p>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Total P&L</h3>
          <p className={`text-3xl font-bold mt-2 ${currentPnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${currentPnl.toFixed(2)}
          </p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6">Equity Curve</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1F2937', border: 'none', color: '#fff' }}
                itemStyle={{ color: '#60A5FA' }}
              />
              <Line type="monotone" dataKey="pnl" stroke="#3B82F6" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
