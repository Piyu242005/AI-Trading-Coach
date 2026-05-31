import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuthStore } from '../store/authStore';
import { Brain, AlertTriangle, ShieldCheck } from 'lucide-react';

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

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
            <Brain className="w-6 h-6 mr-2 text-purple-500" />
            Behavioral Profile
          </h2>
          <p className="text-gray-500 mt-1 text-sm">AI analysis of your trading psychology.</p>
        </div>
      </div>

      <div className={`p-6 rounded-xl border ${isHealthy ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800' : 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800'}`}>
        <div className="flex items-center mb-4">
          {isHealthy ? <ShieldCheck className="w-8 h-8 text-green-600 mr-3" /> : <AlertTriangle className="w-8 h-8 text-red-600 mr-3" />}
          <h3 className={`text-2xl font-bold ${isHealthy ? 'text-green-800 dark:text-green-300' : 'text-red-800 dark:text-red-300'}`}>
            Detected Pattern: {behavior}
          </h3>
        </div>
        <p className="text-gray-700 dark:text-gray-300">
          {data?.summary || 'No summary available.'}
        </p>
      </div>

      {data?.evidence && data.evidence.length > 0 && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Evidence Log</h3>
          <div className="space-y-4">
            {data.evidence.map((ev: any, i: number) => (
              <div key={i} className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <span className="text-xs font-mono text-gray-500 mb-2 block">Session: {ev.sessionId}</span>
                <p className="text-gray-800 dark:text-gray-200">{ev.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
