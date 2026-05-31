import { Link } from 'react-router-dom';
import { Brain, Activity, MessageSquare, ArrowRight } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 overflow-hidden font-sans">
      {/* Navbar */}
      <nav className="absolute top-0 w-full px-6 py-6 flex justify-between items-center z-10">
        <div className="flex items-center text-xl font-bold text-gray-900 dark:text-white">
          <Brain className="w-8 h-8 text-blue-600 mr-2" />
          AI Trading Coach
        </div>
        <Link 
          to="/login" 
          className="px-6 py-2.5 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-full shadow-lg transition-all"
        >
          Sign In
        </Link>
      </nav>

      {/* Hero Section */}
      <div className="relative pt-40 pb-20 sm:pt-48 sm:pb-32 overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-gradient-to-b from-blue-100/50 to-transparent dark:from-blue-900/20 pointer-events-none rounded-full blur-3xl"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl sm:text-7xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-8 drop-shadow-sm">
            Master your psychology.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-500">Elevate your trading.</span>
          </h1>
          <p className="mt-4 text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto font-light leading-relaxed mb-12">
            Real-time behavioral analytics, ChatGPT-powered coaching, and automated trade journaling built specifically for professional traders.
          </p>
          <div className="flex justify-center gap-4">
            <Link 
              to="/login"
              className="inline-flex items-center px-10 py-5 text-lg font-bold text-white bg-gray-900 dark:bg-white dark:text-gray-900 hover:scale-105 rounded-full shadow-2xl transition-transform"
            >
              Start Analysis <ArrowRight className="ml-3 w-6 h-6" />
            </Link>
          </div>
        </div>
      </div>

      {/* Feature Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard 
            icon={<Brain className="w-8 h-8 text-purple-500" />}
            title="Behavioral Analytics"
            desc="Automatically detect tilt, overtrading, and revenge trading before they drain your account."
          />
          <FeatureCard 
            icon={<MessageSquare className="w-8 h-8 text-blue-500" />}
            title="AI Coaching"
            desc="Get real-time, ChatGPT-style personalized feedback tailored to your exact trading sessions."
          />
          <FeatureCard 
            icon={<Activity className="w-8 h-8 text-green-500" />}
            title="Advanced Metrics"
            desc="Track your actual Discipline Score, Profit Factor, and Risk Distribution in a glassmorphic dashboard."
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: any) {
  return (
    <div className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl p-8 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 hover:-translate-y-2 transition-transform duration-300">
      <div className="bg-gray-50 dark:bg-gray-900/50 w-16 h-16 rounded-2xl flex items-center justify-center mb-6 shadow-inner">
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 leading-relaxed text-lg">{desc}</p>
    </div>
  );
}
