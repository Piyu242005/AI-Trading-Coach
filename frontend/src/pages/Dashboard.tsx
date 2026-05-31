import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { Activity, Zap, TrendingUp, TrendingDown, Lightbulb } from 'lucide-react';

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

  // Risk Distribution Data
  const riskData = [
    { name: 'Winning Trades', value: winningTrades },
    { name: 'Losing Trades', value: losingTrades },
  ];
  const RISK_COLORS = ['#10B981', '#EF4444'];

  // Mock Weekly Progress
  const weeklyProgressData = [
    { week: 'Week 1', score: 68 },
    { week: 'Week 2', score: 72 },
    { week: 'Week 3', score: disciplineData?.score || 79 },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header row with Insights & AI Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* User Insights Panel */}
        <div className="lg:col-span-2 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl p-8 text-white shadow-lg flex flex-col justify-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          <h2 className="text-3xl font-extrabold mb-2 z-10 flex items-center">
            <Lightbulb className="w-8 h-8 mr-3 text-yellow-300" />
            Today's Insight
          </h2>
          <p className="text-blue-100 text-lg z-10 mb-6">
            Your discipline score improved by <strong className="text-white">11 points</strong> this month!
          </p>
          <div className="flex gap-6 z-10">
            <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20 flex-1">
              <span className="text-blue-200 text-sm font-semibold uppercase tracking-wider block mb-1">Main Strength</span>
              <span className="font-bold text-lg">Profit Factor ({profitFactor})</span>
            </div>
            <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20 flex-1">
              <span className="text-blue-200 text-sm font-semibold uppercase tracking-wider block mb-1">Main Weakness</span>
              <span className="font-bold text-lg">
                {disciplineData?.contributors?.overtrading_penalty < 0 ? 'Overtrading' : 'Drawdown Management'}
              </span>
            </div>
          </div>
        </div>

        {/* Circular Discipline Gauge */}
        {disciplineData && (
          <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 flex flex-col items-center justify-center relative">
            <h3 className="text-gray-500 dark:text-gray-400 font-semibold uppercase tracking-wider text-sm mb-4">Trader Discipline</h3>
            <div className="relative w-48 h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={[{ value: disciplineData.score }, { value: 100 - disciplineData.score }]}
                    cx="50%"
                    cy="50%"
                    startAngle={225}
                    endAngle={-45}
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={0}
                    dataKey="value"
                    stroke="none"
                  >
                    <Cell fill={disciplineData.score > 80 ? '#10B981' : disciplineData.score > 60 ? '#F59E0B' : '#EF4444'} />
                    <Cell fill="#E5E7EB" />
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-extrabold text-gray-900 dark:text-white">{disciplineData.score}</span>
                <span className="text-gray-400 text-sm font-medium">/ 100</span>
              </div>
            </div>
            
            {/* Confidence Tooltip */}
            <div className="absolute bottom-6 right-6 group cursor-help">
              <div className="flex items-center text-gray-400 hover:text-blue-500 transition-colors bg-gray-50 dark:bg-gray-900 px-3 py-1.5 rounded-full border border-gray-200 dark:border-gray-700">
                <Zap className="w-4 h-4 mr-1 text-yellow-500" />
                <span className="text-xs font-bold">{disciplineData.confidence}%</span>
              </div>
              <div className="absolute bottom-full right-0 mb-2 w-48 p-3 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all shadow-xl z-50">
                <p className="font-bold mb-1">AI Confidence</p>
                <p className="text-gray-300">Confidence in behavioral pattern detection based on available trade history volume.</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stats Grid with Trend Indicators */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Win Rate" value={`${winRate}%`} trend="↓ 3% vs last week" isNegative />
        <StatCard title="Profit Factor" value={profitFactor} trend="↑ 0.4 improvement" />
        <StatCard title="Total P&L" value={`₹${currentPnl.toFixed(2)}`} valueColor={currentPnl >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'} trend="↑ 12% vs last week" />
        <div className="flex flex-col justify-between bg-white dark:bg-gray-800 p-5 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div className="flex justify-between w-full mb-2">
            <span className="text-gray-500 dark:text-gray-400 text-sm font-medium">Avg Win</span>
            <span className="text-green-600 dark:text-green-400 font-bold">₹{avgWin}</span>
          </div>
          <div className="flex justify-between w-full">
            <span className="text-gray-500 dark:text-gray-400 text-sm font-medium">Avg Loss</span>
            <span className="text-red-600 dark:text-red-400 font-bold">-₹{avgLoss}</span>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Advanced Equity Curve */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700">
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
                  contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '12px', color: '#fff', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' }}
                  itemStyle={{ color: '#E5E7EB' }}
                />
                <Area type="monotone" dataKey="pnl" name="Equity (₹)" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorPnl)" />
                <Area type="monotone" dataKey="drawdown" name="Drawdown (₹)" stroke="#EF4444" strokeWidth={1} fillOpacity={1} fill="url(#colorDrawdown)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sidebar Charts */}
        <div className="flex flex-col gap-6">
          
          {/* Risk Distribution */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 flex-1">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-4">Risk Exposure</h3>
            <div className="h-40 w-full relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={60}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {riskData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={RISK_COLORS[index % RISK_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                    itemStyle={{ color: '#fff' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center gap-4 mt-2">
              <div className="flex items-center text-xs font-medium text-gray-500">
                <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div> Wins
              </div>
              <div className="flex items-center text-xs font-medium text-gray-500">
                <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div> Losses
              </div>
            </div>
          </div>

          {/* Weekly Progress */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 flex-1">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-4">Weekly Progress</h3>
            <div className="h-32 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={weeklyProgressData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                  <XAxis dataKey="week" stroke="#9CA3AF" tick={{fontSize: 10}} />
                  <YAxis domain={['dataMin - 10', 'dataMax + 10']} hide />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                  />
                  <Line type="monotone" dataKey="score" stroke="#8B5CF6" strokeWidth={3} dot={{ r: 4, fill: '#8B5CF6', strokeWidth: 2, stroke: '#fff' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, valueColor = 'text-gray-900 dark:text-white', trend, isNegative }: any) {
  return (
    <div className="bg-white dark:bg-gray-800 p-5 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
      <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <p className={`text-3xl font-extrabold ${valueColor}`}>{value}</p>
      {trend && (
        <div className={`mt-2 flex items-center text-xs font-semibold ${isNegative ? 'text-red-500' : 'text-green-500'}`}>
          {isNegative ? <TrendingDown className="w-3 h-3 mr-1" /> : <TrendingUp className="w-3 h-3 mr-1" />}
          {trend}
        </div>
      )}
    </div>
  );
}
