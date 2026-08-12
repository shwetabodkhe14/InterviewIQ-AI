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
