import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Brain, Activity } from 'lucide-react';
import clsx from 'clsx';

export default function Sidebar() {
  const links = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Behavioral Profile', path: '/profiling', icon: Brain },
    { name: 'Real-time Coaching', path: '/coaching', icon: MessageSquare },
  ];

  return (
    <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 h-full">
      <div className="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-700">
        <Activity className="w-6 h-6 text-blue-600 mr-2" />
        <span className="text-xl font-bold text-gray-900 dark:text-white">AI Coach</span>
      </div>
      <nav className="p-4 space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.name}
              to={link.path}
              className={({ isActive }) =>
                clsx(
                  'flex items-center px-4 py-3 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-200'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
                )
              }
            >
              <Icon className="w-5 h-5 mr-3" />
              {link.name}
            </NavLink>
          );
        })}
      </nav>
    </div>
  );
}
