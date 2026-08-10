import React from 'react';
import { Link } from 'react-router-dom';

const ResetPasswordPage = () => {
  return (
    <div className="flex min-h-screen w-full bg-background items-center justify-center p-6">
      <div className="max-w-md w-full glass p-8 rounded-3xl shadow-2xl text-center">
        <h2 className="text-2xl font-bold text-white mb-4">Reset Password</h2>
        <p className="text-slate-400 mb-6">Enter your email and we'll send you a link to reset your password.</p>
        <form className="space-y-4">
          <input 
            type="email" 
            placeholder="Email Address" 
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-primary-DEFAULT transition-all"
          />
          <button type="submit" className="w-full bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white font-medium rounded-xl py-3 transition-colors shadow-[0_0_15px_rgba(139,92,246,0.3)]">
            Send Reset Link
          </button>
        </form>
        <div className="mt-6">
          <Link to="/auth" className="text-sm text-slate-400 hover:text-white transition-colors">Back to Login</Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage;
