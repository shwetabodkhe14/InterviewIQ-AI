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
