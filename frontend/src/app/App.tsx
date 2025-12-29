import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './components/auth/Login';
import { Signup } from './components/auth/Signup';
import { Onboarding } from './components/onboarding/Onboarding';
import { Dashboard } from './components/dashboard/Dashboard';
import { TaskExecution } from './components/task/TaskExecution';
import { Feedback } from './components/feedback/Feedback';
import { Progress } from './components/progress/Progress';
import { WeeklySummary } from './components/weekly/WeeklySummary';
import { ProtectedRoute } from './components/auth/ProtectedRoute';

export default function App() {
  return (
    <div className="min-h-screen bg-[#1a1a1e] dark">
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/onboarding" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/task/:taskId" element={<ProtectedRoute><TaskExecution /></ProtectedRoute>} />
          <Route path="/feedback/:taskId" element={<ProtectedRoute><Feedback /></ProtectedRoute>} />
          <Route path="/progress" element={<ProtectedRoute><Progress /></ProtectedRoute>} />
          <Route path="/weekly-summary" element={<ProtectedRoute><WeeklySummary /></ProtectedRoute>} />
        </Routes>
      </Router>
    </div>
  );
}
