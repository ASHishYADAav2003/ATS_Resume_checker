import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

export default function FileUpload({ onSuccess }: { onSuccess: (resumeId: number, jobId: number) => void }) {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [jobTitle, setJobTitle] = useState('Software Engineer');
  const [jobCompany, setJobCompany] = useState('Tech Corp');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const { token } = useAuth();

  const handleUpload = async () => {
    if (!resumeFile || !jobDescription) {
      setError('Please provide both a resume file and a job description.');
      return;
    }
    
    setIsUploading(true);
    setError('');

    try {
      // 1. Upload Resume
      const resumeFormData = new FormData();
      resumeFormData.append('file', resumeFile);
      
      const resumeRes = await axios.post('/api/upload/resume', resumeFormData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });
      const resumeId = resumeRes.data.resume_id;

      // 2. Upload Job Description
      const jobRes = await axios.post(
        `/api/upload/job-description?title=${encodeURIComponent(jobTitle)}&company=${encodeURIComponent(jobCompany)}&text_content=${encodeURIComponent(jobDescription)}`, 
        null, 
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const jobId = jobRes.data.job_id;

      onSuccess(resumeId, jobId);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'An error occurred during upload.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {error && <div className="bg-red-500/10 border border-red-500 text-red-500 p-3 rounded">{error}</div>}
      
      <div>
        <label className="block text-sm font-medium mb-2 text-slate-300">Upload Resume (PDF/DOCX)</label>
        <input 
          type="file" 
          accept=".pdf,.docx"
          onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
          className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2 text-slate-300">Paste Job Description</label>
        <textarea
          rows={6}
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the full job description here..."
          className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
        />
      </div>
      
      <button 
        onClick={handleUpload}
        disabled={isUploading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-3 rounded-lg transition-colors"
      >
        {isUploading ? 'Uploading & Analyzing...' : 'Analyze Resume'}
      </button>
    </div>
  );
}
