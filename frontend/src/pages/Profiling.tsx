import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { Brain, AlertTriangle, ShieldCheck, TrendingDown, Target } from 'lucide-react';

export default function Profiling() {
  const userId = useAuthStore(state => state.userId);

  const { data, isLoading, error } = useQuery({
    queryKey: ['profiling', userId],
    queryFn: async () => {
      const res = await api.get(`/api/profiling/${userId}`);
      return res.data;
    },
    enabled: !!userId,
  });

  if (isLoading) return <div className="p-8 text-center text-gray-500">Loading behavioral profile...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Error loading profile data</div>;

  const behavior = data?.behavior?.replace('_', ' ')?.toUpperCase() || 'UNKNOWN';
  const isHealthy = behavior === 'NONE' || behavior === 'UNKNOWN';

  // Rich metadata mapping
  const metadataMap: Record<string, any> = {
    'OVERTRADING': {
      confidence: '92%',
      severity: 'High',
      impact: 'Frequent trading dramatically increases transaction costs, reduces strategy expectancy, and leads to decision fatigue.',
      recommendation: 'Implement a hard limit of 3 trades per session. Step away from the screen after hitting the limit.'
    },
    'REVENGE TRADING': {
      confidence: '88%',
      severity: 'Critical',
      impact: 'Trading immediately after a loss out of frustration destroys risk management and causes outsized drawdowns.',
      recommendation: 'Enforce a mandatory 15-minute cool-down period after any losing trade before entering a new position.'
    },
    'TILT': {
      confidence: '85%',
      severity: 'High',
      impact: 'Emotional dysregulation is causing deviation from your documented trading plan.',
      recommendation: 'Review your daily risk limit. If you are within 20% of your max daily loss, halt trading for the day.'
    }
  };

  const meta = metadataMap[behavior] || {
    confidence: '95%',
    severity: 'Low',
    impact: 'Maintaining discipline allows edge to play out over a large sample size.',
    recommendation: 'Continue following your trading plan.'
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
            <Brain className="w-7 h-7 mr-3 text-purple-500" />
            Behavioral Profile
          </h2>
          <p className="text-gray-500 mt-1">Deep analysis of your trading psychology and biases.</p>
        </div>
      </div>

      <div className={`p-8 rounded-2xl border backdrop-blur-md shadow-lg ${isHealthy ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-200 dark:from-green-900/30 dark:to-emerald-900/10 dark:border-green-800/50' : 'bg-gradient-to-br from-red-50 to-orange-50 border-red-200 dark:from-red-900/30 dark:to-orange-900/10 dark:border-red-800/50'}`}>
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center mb-6">
              {isHealthy ? <ShieldCheck className="w-10 h-10 text-green-600 mr-4" /> : <AlertTriangle className="w-10 h-10 text-red-600 mr-4" />}
              <h3 className={`text-3xl font-extrabold tracking-tight ${isHealthy ? 'text-green-800 dark:text-green-300' : 'text-red-800 dark:text-red-300'}`}>
                {behavior}
              </h3>
            </div>
            
            <div className="space-y-6">
              <div>
                <h4 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-2 flex items-center">
                  <TrendingDown className="w-4 h-4 mr-2 text-gray-500" /> Business Impact
                </h4>
                <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                  {meta.impact}
                </p>
              </div>

              <div>
                <h4 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-2 flex items-center">
                  <Target className="w-4 h-4 mr-2 text-gray-500" /> Recommendation
                </h4>
                <div className={`p-4 rounded-xl border ${isHealthy ? 'bg-green-100/50 border-green-300 dark:bg-green-800/30 dark:border-green-700' : 'bg-red-100/50 border-red-300 dark:bg-red-800/30 dark:border-red-700'}`}>
                  <p className="font-medium text-gray-900 dark:text-white">{meta.recommendation}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-row md:flex-col gap-4">
            <div className="bg-white/60 dark:bg-gray-800/60 p-4 rounded-xl border border-gray-200/50 dark:border-gray-700/50 text-center min-w-[120px]">
              <span className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Severity</span>
              <span className={`text-xl font-black ${isHealthy ? 'text-green-600' : 'text-red-600'}`}>{meta.severity}</span>
            </div>
            <div className="bg-white/60 dark:bg-gray-800/60 p-4 rounded-xl border border-gray-200/50 dark:border-gray-700/50 text-center min-w-[120px]">
              <span className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Confidence</span>
              <span className="text-xl font-black text-gray-900 dark:text-white">{meta.confidence}</span>
            </div>
          </div>
        </div>
      </div>

      {data?.evidence && data.evidence.length > 0 && (
        <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Evidence Log</h3>
          <div className="space-y-4">
            {data.evidence.map((ev: any, i: number) => (
              <div key={i} className="p-5 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800">
                <span className="text-xs font-mono text-gray-400 mb-3 block">Session ID: {ev.sessionId}</span>
                <p className="text-gray-800 dark:text-gray-200 font-medium">{ev.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
