import React, { useState, useEffect, useRef } from 'react';
import api from '../api/api';
import toast from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, Play, ChevronRight, CheckCircle, BarChart, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const COMPANIES = ['Generic', 'Google', 'Microsoft', 'Amazon', 'NVIDIA', 'Meta', 'TCS', 'Infosys', 'Wipro', 'Capgemini', 'Accenture', 'Deloitte', 'Cognizant'];
const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
const DOMAINS = ['General', 'Data Science', 'Machine Learning', 'AI', 'Python', 'SQL', 'React', 'FastAPI', 'Java', 'C++', 'Web Development'];

const Interview = () => {
  const [sessionStarted, setSessionStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  
  const [company, setCompany] = useState('Generic');
  const [difficulty, setDifficulty] = useState('Medium');
  const [domain, setDomain] = useState('General');

  const [sessionId, setSessionId] = useState(null);
  const [totalQs, setTotalQs] = useState(0);
  const [currentQNum, setCurrentQNum] = useState(0);
  const [questionText, setQuestionText] = useState('');
  
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [completed, setCompleted] = useState(false);

  // Timer state
  const [timeLeft, setTimeLeft] = useState(120);
  

  const navigate = useNavigate();

  // Auto-submit timer
  useEffect(() => {
    let timer;
    if (sessionStarted && !evaluation && !completed && !evaluating) {
      timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            submitAnswer(true); // pass true for auto-submit
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [sessionStarted, evaluation, completed, evaluating, answer]); // Include answer in dep array to pass latest to submit

  const startInterview = async () => {
    setLoading(true);
    try {
      const res = await api.post('/session/start', {
        company: company === 'Generic' ? null : company,
        difficulty,
        domain: domain === 'General' ? null : domain
      });
      setSessionId(res.data.session_id);
      setTotalQs(res.data.total_questions);
      setCurrentQNum(res.data.question_number);
      setQuestionText(res.data.question);
      setSessionStarted(true);
      setTimeLeft(120);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Make sure you have uploaded a resume first.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async (isAutoSubmit = false) => {
    const finalAnswer = answer.trim() || (isAutoSubmit ? "No answer provided within the time limit." : "");
    if (!finalAnswer && !isAutoSubmit) return toast.error("Please provide an answer.");
    
    setEvaluating(true);
    try {
      const res = await api.post('/session/answer', {
        session_id: sessionId,
        answer: finalAnswer
      });

      if (res.data.completed) {
        setCompleted(true);
      } else {
        setEvaluation(res.data.evaluation);
        setTimeout(() => {
          setAnswer('');
          setCurrentQNum(res.data.question_number);
          setQuestionText(res.data.question);
          setEvaluation(null);
          setTimeLeft(120);
        }, 5000);
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to submit answer.");
    } finally {
      setEvaluating(false);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
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
      <div className="flex flex-col items-center justify-center py-10">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 max-w-lg w-full">
          <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Play className="w-8 h-8 ml-1" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-2 text-center">Interview Settings</h2>
          <p className="text-slate-500 mb-6 text-center">Customize your mock interview experience.</p>
          
          <div className="space-y-4 mb-8">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Target Company</label>
              <select value={company} onChange={(e) => setCompany(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
                {COMPANIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Difficulty Level</label>
              <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
                {DIFFICULTIES.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Target Domain</label>
              <select value={domain} onChange={(e) => setDomain(e.target.value)} className="w-full p-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
                {DOMAINS.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
          </div>

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
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 mb-6 relative">
              <div className="absolute top-6 right-8 flex items-center text-slate-500 font-mono">
                <Clock className="w-4 h-4 mr-2" />
                <span className={timeLeft < 30 ? 'text-red-500 font-bold' : ''}>{formatTime(timeLeft)}</span>
              </div>
              
              <h3 className="text-xl font-medium text-slate-900 mb-6 mt-4 leading-relaxed pr-16">{questionText}</h3>
              
              <div className="relative">
                <textarea
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  rows={8}
                  placeholder="Type your detailed answer here..."
                  className="w-full p-4 border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
              </div>
              
              <div className="mt-6 flex justify-end">
                <button 
                  onClick={() => submitAnswer(false)} 
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
