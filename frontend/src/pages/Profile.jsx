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
