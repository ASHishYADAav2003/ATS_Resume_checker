export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-4">
      <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
        ATS Compatibility Analyzer
      </h1>
      <p className="text-xl text-slate-300 mb-8 max-w-2xl text-center">
        Optimize your resume for any job description using advanced AI and NLP technology. 
        Get actionable feedback and beat the Applicant Tracking Systems.
      </p>
      <div className="flex gap-4">
        <a href="/login" className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors">
          Get Started
        </a>
      </div>
    </div>
  )
}
