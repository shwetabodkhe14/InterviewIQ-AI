import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def generate_frontend():
    files = {
        'src/App.jsx': """
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ResumeUpload from './pages/ResumeUpload';
import Interview from './pages/Interview';
import Report from './pages/Report';
import History from './pages/History';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster position="top-right" />
        <Routes>
          {/* Auth Routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Route>

          {/* Protected Routes */}
          <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/resume" element={<ResumeUpload />} />
            <Route path="/interview" element={<Interview />} />
            <Route path="/report/:id" element={<Report />} />
            <Route path="/history" element={<History />} />
            <Route path="/profile" element={<Profile />} />
          </Route>

          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
        """,
        'src/main.jsx': """
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
        """,
        'src/components/ProtectedRoute.jsx': """
import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useContext(AuthContext);
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
        """,
        'src/layouts/AuthLayout.jsx': """
import React, { useContext } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';

const AuthLayout = () => {
  const { isAuthenticated } = useContext(AuthContext);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-white p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 border border-slate-100"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900">InterviewIQ AI</h1>
          <p className="text-slate-500 mt-2">Master your next tech interview</p>
        </div>
        <Outlet />
      </motion.div>
    </div>
  );
};

export default AuthLayout;
        """,
        'src/layouts/MainLayout.jsx': """
import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="h-screen flex overflow-hidden bg-slate-50">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      <div className="flex-1 flex flex-col w-0 overflow-hidden">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
        """,
        'src/components/Navbar.jsx': """
import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Bell, Menu, UserCircle, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Navbar = ({ onMenuClick }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8 shrink-0">
      <div className="flex items-center">
        <button onClick={onMenuClick} className="text-slate-500 hover:text-slate-700 md:hidden p-2 -ml-2">
          <Menu className="w-6 h-6" />
        </button>
        <div className="hidden md:flex font-bold text-xl text-primary-600">
          InterviewIQ
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <button className="text-slate-400 hover:text-slate-500 p-1 rounded-full relative">
          <Bell className="w-6 h-6" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <div className="flex items-center space-x-3 border-l pl-4">
          <div className="hidden sm:block text-sm text-right">
            <p className="font-medium text-slate-700">{user?.full_name}</p>
            <p className="text-xs text-slate-500">{user?.email}</p>
          </div>
          <UserCircle className="w-8 h-8 text-slate-400" />
          <button onClick={handleLogout} className="text-slate-400 hover:text-red-500 p-1">
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
        """,
        'src/components/Sidebar.jsx': """
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, PlayCircle, History, User, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Upload Resume', href: '/resume', icon: FileText },
  { name: 'Interview', href: '/interview', icon: PlayCircle },
  { name: 'History', href: '/history', icon: History },
  { name: 'Profile', href: '/profile', icon: User },
];

const SidebarContent = () => (
  <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
    <div className="flex items-center flex-shrink-0 px-4 md:hidden">
      <span className="font-bold text-2xl text-primary-600">InterviewIQ</span>
    </div>
    <nav className="mt-5 px-2 space-y-1">
      {navigation.map((item) => (
        <NavLink
          key={item.name}
          to={item.href}
          className={({ isActive }) =>
            `group flex items-center px-2 py-3 text-sm font-medium rounded-lg transition-colors duration-150 ${
              isActive
                ? 'bg-primary-50 text-primary-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`
          }
        >
          {({ isActive }) => (
            <>
              <item.icon
                className={`mr-3 flex-shrink-0 h-6 w-6 ${
                  isActive ? 'text-primary-600' : 'text-slate-400 group-hover:text-slate-500'
                }`}
              />
              {item.name}
            </>
          )}
        </NavLink>
      ))}
    </nav>
  </div>
);

const Sidebar = ({ open, setOpen }) => {
  return (
    <>
      {/* Mobile Sidebar */}
      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 flex z-40 md:hidden">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-slate-600 bg-opacity-75"
              onClick={() => setOpen(false)}
            />
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', bounce: 0, duration: 0.3 }}
              className="relative flex-1 flex flex-col max-w-xs w-full bg-white"
            >
              <div className="absolute top-0 right-0 -mr-12 pt-2">
                <button
                  className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                  onClick={() => setOpen(false)}
                >
                  <X className="h-6 w-6 text-white" />
                </button>
              </div>
              <SidebarContent />
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64 bg-white border-r border-slate-200">
          <SidebarContent />
        </div>
      </div>
    </>
  );
};

export default Sidebar;
        """,
        'src/pages/Login.jsx': """
import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { Loader2 } from 'lucide-react';

const Login = () => {
  const { login } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      await login(data.email, data.password);
      toast.success('Successfully logged in!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-slate-700">Email Address</label>
        <input
          type="email"
          {...register('email', { required: 'Email is required' })}
          className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700">Password</label>
        <input
          type="password"
          {...register('password', { required: 'Password is required' })}
          className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
        {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
      >
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Sign In'}
      </button>

      <div className="text-sm text-center">
        <span className="text-slate-500">Don't have an account? </span>
        <Link to="/register" className="font-medium text-primary-600 hover:text-primary-500">
          Sign up
        </Link>
      </div>
    </form>
  );
};

export default Login;
        """,
        'src/pages/Register.jsx': """
import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { Loader2 } from 'lucide-react';

const Register = () => {
  const { register: registerUser } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  
  const password = watch("password");

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      await registerUser(data.full_name, data.email, data.password);
      toast.success('Registration successful!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700">Full Name</label>
        <input
          type="text"
          {...register('full_name', { required: 'Full name is required' })}
          className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
        {errors.full_name && <p className="mt-1 text-sm text-red-600">{errors.full_name.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700">Email Address</label>
        <input
          type="email"
          {...register('email', { required: 'Email is required' })}
          className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700">Password</label>
        <input
          type="password"
          {...register('password', { required: 'Password is required', minLength: { value: 6, message: 'Minimum 6 characters' } })}
          className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
        {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
      >
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create Account'}
      </button>

      <div className="text-sm text-center">
        <span className="text-slate-500">Already have an account? </span>
        <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
          Sign in
        </Link>
      </div>
    </form>
  );
};

export default Register;
        """,
        'src/pages/Dashboard.jsx': """
import React, { useEffect, useState } from 'react';
import api from '../api/api';
import { motion } from 'framer-motion';
import { Activity, Star, Calendar, FileText, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get('/dashboard/');
        setData(response.data);
      } catch (error) {
        console.error("Dashboard fetch error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <div className="p-8 animate-pulse flex space-x-4"><div className="flex-1 space-y-4 py-1"><div className="h-4 bg-slate-200 rounded w-3/4"></div><div className="space-y-2"><div className="h-4 bg-slate-200 rounded"></div><div className="h-4 bg-slate-200 rounded w-5/6"></div></div></div></div>;

  const stats = [
    { name: 'Total Interviews', value: data?.total_interviews || 0, icon: Activity, color: 'bg-blue-500' },
    { name: 'Average Score', value: data?.average_overall_score ? `${data.average_overall_score}%` : 'N/A', icon: Star, color: 'bg-yellow-500' },
    { name: 'Resume Uploaded', value: data?.has_resume ? 'Yes' : 'No', icon: FileText, color: data?.has_resume ? 'bg-green-500' : 'bg-red-500' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Welcome Back!</h2>
        <p className="mt-1 text-sm text-slate-500">Here's a summary of your interview progress.</p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        {stats.map((item, index) => (
          <motion.div
            key={item.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white overflow-hidden shadow rounded-2xl p-5 border border-slate-100 flex items-center"
          >
            <div className={`p-3 rounded-xl ${item.color} text-white`}>
              <item.icon className="w-6 h-6" />
            </div>
            <div className="ml-5">
              <p className="text-sm font-medium text-slate-500 truncate">{item.name}</p>
              <p className="mt-1 text-2xl font-semibold text-slate-900">{item.value}</p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl shadow border border-slate-100 p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Quick Actions</h3>
          <div className="space-y-4">
            <Link to="/resume" className="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors">
              <div className="flex items-center">
                <FileText className="w-5 h-5 text-primary-500 mr-3" />
                <span className="font-medium text-slate-700">Upload New Resume</span>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </Link>
            <Link to="/interview" className="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors">
              <div className="flex items-center">
                <Activity className="w-5 h-5 text-primary-500 mr-3" />
                <span className="font-medium text-slate-700">Start Mock Interview</span>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow border border-slate-100 p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Recent Activity</h3>
          {data?.recent_activity && data.recent_activity.length > 0 ? (
            <div className="space-y-4">
              {data.recent_activity.map((activity, idx) => (
                <div key={idx} className="flex items-start">
                  <div className="flex-shrink-0 h-2 w-2 mt-2 rounded-full bg-primary-500"></div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-slate-900">{activity.description}</p>
                    <p className="text-xs text-slate-500">{new Date(activity.date).toLocaleDateString()}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-sm italic">No recent activity found. Start an interview!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
        """,
        'src/pages/ResumeUpload.jsx': """
import React, { useState, useRef } from 'react';
import api from '../api/api';
import toast from 'react-hot-toast';
import { UploadCloud, File, CheckCircle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleDragOver = (e) => e.preventDefault();
  
  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      toast.error('Only PDF files are allowed!');
      return;
    }
    setFile(selectedFile);
    setSuccess(false);
  };

  const uploadResume = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSuccess(true);
      toast.success('Resume parsed successfully!');
      setTimeout(() => navigate('/interview'), 2000);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upload resume.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-slate-900">Upload Your Resume</h2>
        <p className="text-slate-500 mt-2">We'll use Gemini AI to parse your resume and generate tailored interview questions.</p>
      </div>

      <motion.div 
        className={`border-2 border-dashed rounded-2xl p-12 text-center transition-colors ${file ? 'border-primary-400 bg-primary-50' : 'border-slate-300 hover:border-slate-400 bg-white'}`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input type="file" ref={fileInputRef} className="hidden" accept=".pdf" onChange={handleFileChange} />
        
        {success ? (
          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="flex flex-col items-center">
            <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
            <h3 className="text-lg font-medium text-slate-900">Resume parsed successfully!</h3>
            <p className="text-slate-500">Redirecting to interview setup...</p>
          </motion.div>
        ) : file ? (
          <div className="flex flex-col items-center">
            <File className="w-12 h-12 text-primary-500 mb-4" />
            <p className="text-sm font-medium text-slate-900">{file.name}</p>
            <p className="text-xs text-slate-500 mb-6">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            
            <div className="flex space-x-4">
              <button onClick={() => setFile(null)} className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-md hover:bg-slate-50">
                Cancel
              </button>
              <button onClick={uploadResume} disabled={loading} className="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 flex items-center">
                {loading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Parsing...</> : 'Upload & Proceed'}
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center cursor-pointer" onClick={() => fileInputRef.current?.click()}>
            <UploadCloud className="w-12 h-12 text-slate-400 mb-4" />
            <p className="text-sm font-medium text-slate-900">Click to upload or drag and drop</p>
            <p className="text-xs text-slate-500 mt-1">PDF only (Max 5MB)</p>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default ResumeUpload;
        """,
        'src/pages/Interview.jsx': """
import React, { useState } from 'react';
import api from '../api/api';
import toast from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, Play, ChevronRight, CheckCircle, BarChart } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Interview = () => {
  const [sessionStarted, setSessionStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  
  const [sessionId, setSessionId] = useState(null);
  const [totalQs, setTotalQs] = useState(0);
  const [currentQNum, setCurrentQNum] = useState(0);
  const [questionText, setQuestionText] = useState('');
  
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [completed, setCompleted] = useState(false);

  const navigate = useNavigate();

  const startInterview = async () => {
    setLoading(true);
    try {
      const res = await api.post('/session/start');
      setSessionId(res.data.session_id);
      setTotalQs(res.data.total_questions);
      setCurrentQNum(res.data.question_number);
      setQuestionText(res.data.question);
      setSessionStarted(true);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Make sure you have uploaded a resume first.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) return toast.error("Please provide an answer.");
    setEvaluating(true);
    try {
      const res = await api.post('/session/answer', {
        session_id: sessionId,
        answer: answer
      });

      if (res.data.completed) {
        setCompleted(true);
      } else {
        setEvaluation(res.data.evaluation);
        // Wait for user to click next
        setTimeout(() => {
          setAnswer('');
          setCurrentQNum(res.data.question_number);
          setQuestionText(res.data.question);
          setEvaluation(null);
        }, 5000); // Auto next after 5 seconds of showing feedback
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to submit answer.");
    } finally {
      setEvaluating(false);
    }
  };

  if (completed) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <CheckCircle className="w-20 h-20 text-green-500 mb-6" />
        <h2 className="text-3xl font-bold text-slate-900 mb-4">Interview Completed!</h2>
        <p className="text-slate-500 mb-8 max-w-md">Great job! You have answered all questions. Our AI has generated a comprehensive performance report.</p>
        <button onClick={() => navigate(`/report/${sessionId}`)} className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 flex items-center">
          <BarChart className="w-5 h-5 mr-2" /> View Final Report
        </button>
      </div>
    );
  }

  if (!sessionStarted) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 max-w-lg w-full text-center">
          <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Play className="w-8 h-8 ml-1" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Ready to start?</h2>
          <p className="text-slate-500 mb-8">We will generate questions based on your resume. Treat this like a real interview.</p>
          <button onClick={startInterview} disabled={loading} className="w-full py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 flex justify-center items-center">
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Start Interview'}
          </button>
        </div>
      </div>
    );
  }

  const progress = (currentQNum / totalQs) * 100;

  return (
    <div className="max-w-4xl mx-auto py-6">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-slate-500">Question {currentQNum} of {totalQs}</span>
          <span className="text-sm font-medium text-primary-600">{Math.round(progress)}% Completed</span>
        </div>
        <div className="w-full bg-slate-200 rounded-full h-2">
          <motion.div className="bg-primary-500 h-2 rounded-full" initial={{ width: 0 }} animate={{ width: `${progress}%` }} />
        </div>
      </div>

      <AnimatePresence mode="wait">
        {!evaluation ? (
          <motion.div key="question" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 mb-6">
              <h3 className="text-xl font-medium text-slate-900 mb-6 leading-relaxed">{questionText}</h3>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={6}
                placeholder="Type your detailed answer here..."
                className="w-full p-4 border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              />
              <div className="mt-6 flex justify-end">
                <button 
                  onClick={submitAnswer} 
                  disabled={evaluating || !answer.trim()} 
                  className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 flex items-center disabled:opacity-50"
                >
                  {evaluating ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Evaluating...</> : <>Submit Answer <ChevronRight className="w-4 h-4 ml-2" /></>}
                </button>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div key="feedback" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
            <div className="flex items-center text-green-600 mb-6">
              <CheckCircle className="w-6 h-6 mr-2" />
              <h3 className="text-lg font-medium">Answer Evaluated</h3>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {[
                { label: 'Technical', val: evaluation.technical_score },
                { label: 'Communication', val: evaluation.communication_score },
                { label: 'Confidence', val: evaluation.confidence_score },
                { label: 'Grammar', val: evaluation.grammar_score }
              ].map(s => (
                <div key={s.label} className="bg-slate-50 rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold text-slate-900">{s.val}/10</p>
                  <p className="text-xs font-medium text-slate-500 uppercase mt-1">{s.label}</p>
                </div>
              ))}
            </div>

            <div className="bg-blue-50 text-blue-900 p-4 rounded-xl border border-blue-100 text-sm mb-6">
              <span className="font-semibold block mb-1">Feedback:</span>
              {evaluation.feedback}
            </div>

            <p className="text-center text-sm text-slate-500 flex items-center justify-center animate-pulse">
              <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Moving to next question...
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Interview;
        """,
        'src/pages/Report.jsx': """
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/api';
import { motion } from 'framer-motion';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Download, Award, Target, AlertCircle, CheckCircle } from 'lucide-react';

const Report = () => {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await api.get(`/session/report/${id}`);
        setReport(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [id]);

  if (loading) return <div className="p-8 text-center text-slate-500">Loading AI Analysis...</div>;
  if (!report) return <div className="p-8 text-center text-red-500">Failed to load report.</div>;

  const chartData = [
    { subject: 'Technical', A: report.average_scores.technical, fullMark: 100 },
    { subject: 'Communication', A: report.average_scores.communication, fullMark: 100 },
    { subject: 'Confidence', A: report.average_scores.confidence, fullMark: 100 },
    { subject: 'Grammar', A: report.average_scores.grammar, fullMark: 100 },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Interview Report</h1>
          <p className="text-slate-500 mt-1">Session ID: {report.session_id} • Questions: {report.questions_answered}</p>
        </div>
        <button className="flex items-center px-4 py-2 bg-white border border-slate-200 shadow-sm rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors">
          <Download className="w-4 h-4 mr-2" /> Export PDF
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="lg:col-span-1 bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex flex-col items-center justify-center text-center">
          <div className="relative mb-4">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-slate-100" />
              <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" strokeDasharray="377" strokeDashoffset={377 - (377 * report.average_scores.overall) / 100} className="text-primary-500 transition-all duration-1000 ease-out" />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center flex-col">
              <span className="text-3xl font-bold text-slate-900">{report.average_scores.overall}</span>
              <span className="text-xs font-medium text-slate-500 uppercase">Score</span>
            </div>
          </div>
          
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${report.recommendation.toLowerCase().includes('recommended') ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
            {report.recommendation.toLowerCase().includes('recommended') ? <CheckCircle className="w-4 h-4 mr-1.5" /> : <AlertCircle className="w-4 h-4 mr-1.5" />}
            {report.recommendation}
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-100 p-6 h-80">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Skills Radar</h3>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
              <Radar name="Candidate" dataKey="A" stroke="#22c55e" fill="#22c55e" fillOpacity={0.5} />
            </RadarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl border border-indigo-100 p-6">
        <h3 className="text-lg font-semibold text-indigo-900 mb-3 flex items-center"><Award className="w-5 h-5 mr-2 text-indigo-500" /> AI Executive Summary</h3>
        <p className="text-indigo-800 leading-relaxed text-sm md:text-base">{report.overall_feedback}</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center"><Target className="w-5 h-5 mr-2 text-green-500" /> Key Strengths</h3>
          <ul className="space-y-3">
            {report.strengths.slice(0, 5).map((s, i) => (
              <li key={i} className="flex items-start text-sm text-slate-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 shrink-0" /> {s}
              </li>
            ))}
          </ul>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center"><AlertCircle className="w-5 h-5 mr-2 text-orange-500" /> Areas for Improvement</h3>
          <ul className="space-y-3">
            {report.weaknesses.slice(0, 5).map((w, i) => (
              <li key={i} className="flex items-start text-sm text-slate-700">
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500 mr-3 mt-1.5 shrink-0" /> {w}
              </li>
            ))}
          </ul>
        </motion.div>
      </div>
    </div>
  );
};

export default Report;
        """,
        'src/pages/History.jsx': """
import React, { useEffect, useState } from 'react';
import api from '../api/api';
import { Link } from 'react-router-dom';
import { Eye } from 'lucide-react';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/history/');
        setHistory(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-900">Interview History</h2>
      
      <div className="bg-white shadow-sm rounded-2xl border border-slate-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Session ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Questions</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {loading ? (
                <tr><td colSpan="5" className="px-6 py-4 text-center text-slate-500">Loading...</td></tr>
              ) : history.length === 0 ? (
                <tr><td colSpan="5" className="px-6 py-4 text-center text-slate-500">No interviews found.</td></tr>
              ) : (
                history.map((session) => (
                  <tr key={session.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{new Date(session.created_at).toLocaleDateString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">#{session.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-primary-100 text-primary-800">
                        {session.overall_score}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{session.completed_questions} / {session.total_questions}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Link to={`/report/${session.id}`} className="text-primary-600 hover:text-primary-900 inline-flex items-center">
                        <Eye className="w-4 h-4 mr-1" /> View Report
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default History;
        """,
        'src/pages/Profile.jsx': """
import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { UserCircle, Mail, Key } from 'lucide-react';

const Profile = () => {
  const { user } = useContext(AuthContext);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-slate-900">Profile Settings</h2>
      
      <div className="bg-white shadow-sm rounded-2xl border border-slate-100 p-6">
        <div className="flex items-center space-x-5">
          <div className="h-24 w-24 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
            <span className="text-4xl font-bold">{user?.full_name?.charAt(0) || 'U'}</span>
          </div>
          <div>
            <h3 className="text-2xl font-bold text-slate-900">{user?.full_name}</h3>
            <p className="text-sm text-slate-500">Candidate Account</p>
          </div>
        </div>
      </div>

      <div className="bg-white shadow-sm rounded-2xl border border-slate-100 overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-200">
          <h3 className="text-lg font-medium leading-6 text-slate-900">Account Information</h3>
        </div>
        <div className="px-6 py-5 space-y-6">
          <div className="flex items-center">
            <UserCircle className="w-5 h-5 text-slate-400 mr-3" />
            <div>
              <p className="text-sm font-medium text-slate-500">Full Name</p>
              <p className="text-base text-slate-900">{user?.full_name}</p>
            </div>
          </div>
          <div className="flex items-center">
            <Mail className="w-5 h-5 text-slate-400 mr-3" />
            <div>
              <p className="text-sm font-medium text-slate-500">Email Address</p>
              <p className="text-base text-slate-900">{user?.email}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
        """,
        'src/pages/NotFound.jsx': """
import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-4">
      <h1 className="text-6xl font-bold text-primary-600 mb-4">404</h1>
      <h2 className="text-2xl font-semibold text-slate-900 mb-2">Page Not Found</h2>
      <p className="text-slate-500 mb-8 text-center max-w-md">The page you are looking for doesn't exist or has been moved.</p>
      <Link to="/" className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700">
        Back to Home
      </Link>
    </div>
  );
};

export default NotFound;
        """
    }

    for path, content in files.items():
        create_file(path, content)
    
    print("All frontend files generated successfully.")

if __name__ == "__main__":
    generate_frontend()
