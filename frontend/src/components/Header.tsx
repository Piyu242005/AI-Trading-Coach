import { useAuthStore } from '../store/authStore';
import { LogOut, User } from 'lucide-react';

export default function Header() {
  const { userId, logout } = useAuthStore();

  return (
    <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">
      <h1 className="text-lg font-semibold text-gray-900 dark:text-white">Overview</h1>
      <div className="flex items-center space-x-4">
        <div className="flex items-center text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-md">
          <User className="w-4 h-4 mr-2" />
          <span className="text-sm font-medium">{userId?.slice(0, 8)}...</span>
        </div>
        <button
          onClick={logout}
          className="p-2 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
          title="Logout"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
}
