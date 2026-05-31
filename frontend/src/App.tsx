import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './store/authStore';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Coaching from './pages/Coaching';
import Profiling from './pages/Profiling';
import Journal from './pages/Journal';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

const queryClient = new QueryClient();

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = useAuthStore(state => state.token);
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 dark:bg-gray-900 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/coaching" element={
            <ProtectedRoute>
              <Layout>
                <Coaching />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/profiling" element={
            <ProtectedRoute>
              <Layout>
                <Profiling />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/journal" element={
            <ProtectedRoute>
              <Layout>
                <Journal />
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}
