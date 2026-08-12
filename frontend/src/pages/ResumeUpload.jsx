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
