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
    { name: 'Average Score', value: data?.average_score !== undefined && data?.average_score !== null ? `${data.average_score}%` : 'N/A', icon: Star, color: 'bg-yellow-500' },
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
