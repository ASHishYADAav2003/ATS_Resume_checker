import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import ReportViewer from '../components/ReportViewer';

export default function Dashboard() {
  const { user, logout, token } = useAuth();
  const navigate = useNavigate();
  const [report, setReport] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleAnalysis = async (resumeId: number, jobId: number) => {
    setIsAnalyzing(true);
    try {
      const res = await axios.post(`/api/analysis/analyze/${resumeId}/${jobId}`, null, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReport(res.data.data);
    } catch (err) {
      console.error("Analysis failed", err);
      alert("Failed to analyze resume. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-slate-300">Welcome, {user?.name || user?.email}</span>
            <button 
              onClick={handleLogout}
              className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg border border-slate-700 transition-colors"
            >
              Sign out
            </button>
          </div>
        </header>

        {!report ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="col-span-1 md:col-span-2 bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h2 className="text-xl font-semibold mb-4">Analyze Resume</h2>
              <p className="text-slate-400 mb-6">Upload your resume and a job description to get an ATS compatibility score.</p>
              {isAnalyzing ? (
                <div className="text-center py-12 text-slate-400 animate-pulse">
                  Analyzing compatibility with AI... This might take a few seconds.
                </div>
              ) : (
                <FileUpload onSuccess={handleAnalysis} />
              )}
            </div>
            
            <div className="col-span-1 space-y-6">
              <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                <h2 className="text-xl font-semibold mb-4">Recent Analyses</h2>
                <p className="text-slate-400 text-sm">No recent analyses found.</p>
              </div>
            </div>
          </div>
        ) : (
          <div>
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">Analysis Results</h2>
              <button 
                onClick={() => setReport(null)}
                className="text-blue-400 hover:text-blue-300 text-sm font-medium"
              >
                ← New Analysis
              </button>
            </div>
            <ReportViewer data={report} />
          </div>
        )}
      </div>
    </div>
  );
}


