import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/api';
import { motion } from 'framer-motion';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Download, Award, Target, AlertCircle, CheckCircle, Briefcase, BookOpen, Map, Cpu, ChevronRight } from 'lucide-react';

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
    <div className="max-w-5xl mx-auto space-y-6 pb-12 print:text-black">
      <div className="flex justify-between items-end mb-8 print:mb-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Interview Report</h1>
          <p className="text-slate-500 mt-1">Session ID: {report.session_id} • Questions: {report.questions_answered}</p>
        </div>
        <button onClick={() => window.print()} className="print:hidden flex items-center px-4 py-2 bg-white border border-slate-200 shadow-sm rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors">
          <Download className="w-4 h-4 mr-2" /> Export PDF
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 print:block print:space-y-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="lg:col-span-1 bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex flex-col items-center justify-center text-center print:border-none print:shadow-none print:p-0">
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
          
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${(report.recommendation || '').toLowerCase().includes('recommended') ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
            {(report.recommendation || '').toLowerCase().includes('recommended') ? <CheckCircle className="w-4 h-4 mr-1.5" /> : <AlertCircle className="w-4 h-4 mr-1.5" />}
            {report.recommendation || 'No Recommendation'}
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-100 p-6 h-80 print:h-64 print:break-inside-avoid print:border-none print:shadow-none print:p-0">
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

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl border border-indigo-100 p-6 print:break-inside-avoid">
        <h3 className="text-lg font-semibold text-indigo-900 mb-3 flex items-center"><Award className="w-5 h-5 mr-2 text-indigo-500" /> AI Executive Summary</h3>
        <p className="text-indigo-800 leading-relaxed text-sm md:text-base">{report.overall_feedback}</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 print:block print:space-y-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 print:break-inside-avoid print:border-none print:shadow-none print:p-0">
          <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center"><Target className="w-5 h-5 mr-2 text-green-500" /> Key Strengths</h3>
          <ul className="space-y-3">
            {report.strengths?.slice(0, 5).map((s, i) => (
              <li key={i} className="flex items-start text-sm text-slate-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 shrink-0" /> {s}
              </li>
            ))}
          </ul>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 print:break-inside-avoid print:border-none print:shadow-none print:p-0">
          <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center"><AlertCircle className="w-5 h-5 mr-2 text-orange-500" /> Areas for Improvement</h3>
          <ul className="space-y-3">
            {report.weaknesses?.slice(0, 5).map((w, i) => (
              <li key={i} className="flex items-start text-sm text-slate-700">
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500 mr-3 mt-1.5 shrink-0" /> {w}
              </li>
            ))}
          </ul>
        </motion.div>
      </div>

      {report.coach && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 mt-8 print:break-inside-avoid print:mt-4 print:border-none print:shadow-none print:p-0">
          <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center border-b pb-4"><Award className="w-6 h-6 mr-2 text-primary-500" /> AI Career Coach Recommendations</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-3 flex items-center"><Map className="w-4 h-4 mr-2" /> Learning Roadmap</h3>
              <ul className="space-y-2">
                {report.coach?.learning_roadmap?.map((item, idx) => (
                  <li key={idx} className="flex items-start text-sm text-slate-700"><span className="text-primary-500 font-bold mr-2">{idx + 1}.</span> {item}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-3 flex items-center"><Cpu className="w-4 h-4 mr-2" /> Key Technologies</h3>
              <div className="flex flex-wrap gap-2">
                {report.coach?.technologies?.map((tech, idx) => (
                  <span key={idx} className="px-3 py-1 bg-slate-100 text-slate-700 rounded-lg text-sm">{tech}</span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-3 flex items-center"><BookOpen className="w-4 h-4 mr-2" /> Certifications</h3>
              <ul className="space-y-2">
                {report.coach?.certifications?.map((cert, idx) => (
                  <li key={idx} className="flex items-center text-sm text-slate-700"><CheckCircle className="w-4 h-4 text-blue-400 mr-2 shrink-0" /> {cert}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-3 flex items-center"><Briefcase className="w-4 h-4 mr-2" /> Target Roles & Companies</h3>
              <div className="mb-3 flex flex-wrap gap-2">
                {report.coach?.job_roles?.map((role, idx) => (
                  <span key={idx} className="px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-xs font-medium">{role}</span>
                ))}
              </div>
              <div className="text-sm text-slate-600">
                <span className="font-medium text-slate-700">Top Matches:</span> {report.coach?.companies?.join(', ')}
              </div>
            </div>
          </div>
          
          <div className="mt-8 pt-6 border-t border-slate-100">
             <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-3">Immediate Next Steps</h3>
             <ul className="space-y-2">
                {report.coach?.next_steps?.map((step, idx) => (
                  <li key={idx} className="flex items-center text-sm text-slate-700"><ChevronRight className="w-4 h-4 text-green-500 mr-2 shrink-0" /> {step}</li>
                ))}
              </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Report;
