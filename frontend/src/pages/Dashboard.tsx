import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Activity, ShieldCheck, Zap } from 'lucide-react';

export default function Dashboard() {
  const userId = useAuthStore(state => state.userId);

  const { data: tradesData, isLoading: tradesLoading } = useQuery({
    queryKey: ['trades'],
    queryFn: async () => {
      const res = await api.get('/api/trades');
      return res.data;
    }
  });

  const { data: disciplineData, isLoading: disciplineLoading } = useQuery({
    queryKey: ['discipline', userId],
    queryFn: async () => {
      const res = await api.get(`/api/discipline-score/${userId}`);
      return res.data;
    },
    enabled: !!userId,
  });

  if (tradesLoading || disciplineLoading) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>;

  const traders = tradesData?.traders || [];
  const currentUser = traders.find((t: any) => t.userId === userId);
  
  if (!currentUser) return <div className="p-8 text-red-500">User not found in dataset. Make sure you used a valid User ID.</div>;

  let allTrades: any[] = [];
  currentUser.sessions.forEach((s: any) => allTrades.push(...s.trades));
  allTrades.sort((a, b) => new Date(a.entryAt).getTime() - new Date(b.entryAt).getTime());

  let currentPnl = 0;
  let peakPnl = 0;
  let grossProfit = 0;
  let grossLoss = 0;
  let winningTrades = 0;
  let losingTrades = 0;
  
  const chartData = allTrades.map(t => {
    currentPnl += t.pnl;
    if (currentPnl > peakPnl) peakPnl = currentPnl;
    const drawdown = currentPnl - peakPnl;

    if (t.pnl > 0) {
      grossProfit += t.pnl;
      winningTrades++;
    } else if (t.pnl < 0) {
      grossLoss += Math.abs(t.pnl);
      losingTrades++;
    }

    return { 
      time: new Date(t.entryAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), 
      pnl: currentPnl, 
      drawdown: drawdown,
      trade: t 
    };
  });

  const totalTrades = allTrades.length;
  const winRate = totalTrades ? ((winningTrades / totalTrades) * 100).toFixed(1) : '0.0';
  const profitFactor = grossLoss > 0 ? (grossProfit / grossLoss).toFixed(2) : '1.00';
  const avgWin = winningTrades > 0 ? (grossProfit / winningTrades).toFixed(2) : '0.00';
  const avgLoss = losingTrades > 0 ? (grossLoss / losingTrades).toFixed(2) : '0.00';

  return (
    <div className="space-y-6">
      {/* Header row with AI Score */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white/50 dark:bg-gray-800/50 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Portfolio Overview</h2>
          <p className="text-gray-500 dark:text-gray-400">Welcome back! Here's your real-time trading performance.</p>
        </div>
        
        {disciplineData && (
          <div className="mt-4 md:mt-0 flex gap-4">
            <div className="flex flex-col items-end bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-800/50">
              <div className="flex items-center text-blue-600 dark:text-blue-400 font-medium text-sm mb-1">
                <ShieldCheck className="w-4 h-4 mr-1" /> Trader Discipline
              </div>
              <div className="flex items-baseline">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">{disciplineData.score}</span>
                <span className="text-gray-500 dark:text-gray-400 ml-1">/100</span>
              </div>
            </div>
            
            <div className="flex flex-col items-end bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-purple-100 dark:border-purple-800/50">
              <div className="flex items-center text-purple-600 dark:text-purple-400 font-medium text-sm mb-1">
                <Zap className="w-4 h-4 mr-1" /> AI Confidence
              </div>
              <div className="flex items-baseline">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">{disciplineData.confidence}</span>
                <span className="text-gray-500 dark:text-gray-400 ml-1">%</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <StatCard title="Total Trades" value={totalTrades} />
        <StatCard title="Win Rate" value={`${winRate}%`} />
        <StatCard title="Total P&L" value={`$${currentPnl.toFixed(2)}`} valueColor={currentPnl >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'} />
        <StatCard title="Profit Factor" value={profitFactor} />
        <div className="flex flex-col justify-between bg-white dark:bg-gray-800 p-5 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div className="flex justify-between w-full mb-2">
            <span className="text-gray-500 dark:text-gray-400 text-sm font-medium">Avg Win</span>
            <span className="text-green-600 dark:text-green-400 font-bold">${avgWin}</span>
          </div>
          <div className="flex justify-between w-full">
            <span className="text-gray-500 dark:text-gray-400 text-sm font-medium">Avg Loss</span>
            <span className="text-red-600 dark:text-red-400 font-bold">-${avgLoss}</span>
          </div>
        </div>
      </div>

      {/* Advanced Equity Curve */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
            <Activity className="w-5 h-5 mr-2 text-blue-500" />
            Equity Curve & Drawdown
          </h3>
        </div>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorPnl" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorDrawdown" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#EF4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
              <XAxis dataKey="time" stroke="#9CA3AF" tick={{fontSize: 12}} />
              <YAxis stroke="#9CA3AF" tick={{fontSize: 12}} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px', color: '#fff' }}
                itemStyle={{ color: '#E5E7EB' }}
              />
              <Area type="monotone" dataKey="pnl" name="Equity ($)" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorPnl)" />
              <Area type="monotone" dataKey="drawdown" name="Drawdown ($)" stroke="#EF4444" strokeWidth={1} fillOpacity={1} fill="url(#colorDrawdown)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, valueColor = 'text-gray-900 dark:text-white' }: any) {
  return (
    <div className="bg-white dark:bg-gray-800 p-5 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
      <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <p className={`text-2xl font-extrabold ${valueColor}`}>{value}</p>
    </div>
  );
}
