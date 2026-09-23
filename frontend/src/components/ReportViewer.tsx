import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { useAuth } from '../context/AuthContext';

interface ReportData {
  ats_score: number;
  keyword_score: number;
  semantic_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  extra_keywords: string[];
  risks: string[];
  ai_feedback: {
    strengths: string[];
    weaknesses: string[];
    suggestions: string[];
  };
}

export default function ReportViewer({ data }: { data: ReportData }) {
  const { token } = useAuth();
  
  const handleDownload = async () => {
    // Assuming report ID is in the data object; if not, we can pass it as a prop
    if (!data.id) {
        alert("Report ID is required to download.");
        return;
    }
    
    try {
      const response = await fetch(`/api/analysis/report/${data.id}/download`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error("Download failed");
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ATS_Report_${data.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err) {
      console.error(err);
      alert("Failed to download PDF.");
    }
  };

  const pieData = [
    { name: 'Match', value: data.ats_score },
    { name: 'Gap', value: 100 - data.ats_score }
  ];
  const COLORS = ['#10B981', '#1E293B'];

  return (
    <div className="space-y-8 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-end">
        <button 
          onClick={handleDownload}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Download PDF Report
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Score Card */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex flex-col items-center justify-center">
          <h3 className="text-lg font-medium text-slate-300 mb-4">Overall ATS Match</h3>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="text-4xl font-bold text-emerald-400 mt-[-100px] mb-[60px]">
            {data.ats_score}%
          </div>
        </div>

        {/* Breakdown */}
        <div className="col-span-2 bg-slate-800 p-6 rounded-xl border border-slate-700 flex flex-col justify-center">
          <h3 className="text-lg font-medium text-slate-300 mb-6">Score Breakdown</h3>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Keyword Match</span>
                <span className="text-sm font-medium text-blue-400">{data.keyword_score}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2.5">
                <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: `${data.keyword_score}%` }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Semantic Similarity</span>
                <span className="text-sm font-medium text-purple-400">{data.semantic_score}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2.5">
                <div className="bg-purple-500 h-2.5 rounded-full" style={{ width: `${data.semantic_score}%` }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Keywords */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h3 className="text-lg font-medium text-emerald-400 mb-4">Matched Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {data.matched_keywords.length > 0 ? data.matched_keywords.map((kw, i) => (
              <span key={i} className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-sm border border-emerald-500/20">
                {kw}
              </span>
            )) : <span className="text-slate-500 text-sm">None detected</span>}
          </div>
        </div>
        
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h3 className="text-lg font-medium text-red-400 mb-4">Missing Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {data.missing_keywords.length > 0 ? data.missing_keywords.map((kw, i) => (
              <span key={i} className="px-3 py-1 bg-red-500/10 text-red-400 rounded-full text-sm border border-red-500/20">
                {kw}
              </span>
            )) : <span className="text-slate-500 text-sm">None detected</span>}
          </div>
        </div>
      </div>

      {/* AI Feedback */}
      <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h3 className="text-xl font-semibold mb-6 border-b border-slate-700 pb-2">AI Resume Review</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="text-emerald-400 font-medium mb-3 flex items-center gap-2">
              <span className="text-xl">✓</span> Strengths
            </h4>
            <ul className="space-y-2 text-sm text-slate-300">
              {data.ai_feedback.strengths.map((item, i) => <li key={i}>• {item}</li>)}
            </ul>
          </div>
          
          <div>
            <h4 className="text-red-400 font-medium mb-3 flex items-center gap-2">
              <span className="text-xl">✗</span> Weaknesses
            </h4>
            <ul className="space-y-2 text-sm text-slate-300">
              {data.ai_feedback.weaknesses.map((item, i) => <li key={i}>• {item}</li>)}
            </ul>
          </div>
          
          <div>
            <h4 className="text-blue-400 font-medium mb-3 flex items-center gap-2">
              <span className="text-xl">💡</span> Suggestions
            </h4>
            <ul className="space-y-2 text-sm text-slate-300">
              {data.ai_feedback.suggestions.map((item, i) => <li key={i}>• {item}</li>)}
            </ul>
          </div>
        </div>
      </div>
      
      {/* Risks */}
      {data.risks && data.risks.length > 0 && (
        <div className="bg-amber-500/10 border border-amber-500/20 p-6 rounded-xl">
          <h3 className="text-amber-400 font-medium mb-3 flex items-center gap-2">
            ⚠️ ATS Risks Detected
          </h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-amber-200">
            {data.risks.map((risk, i) => <li key={i}>{risk}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
