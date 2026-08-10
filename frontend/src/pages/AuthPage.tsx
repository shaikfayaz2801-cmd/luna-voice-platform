import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';
import { Input } from '../components/common/Input';
import { Button } from '../components/common/Button';
import { Sparkles } from 'lucide-react';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();
  const { login, register, isLoggingIn, isRegistering } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        await login({ email: formData.email, password: formData.password });
        toast.success('Welcome back!');
      } else {
        await register(formData);
        toast.success('Account created successfully!');
      }
      navigate('/');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="flex min-h-screen w-full bg-background overflow-hidden relative">
      {/* Background decorations */}
      <div className="absolute top-0 -left-1/4 w-1/2 h-1/2 bg-primary-DEFAULT/20 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-0 -right-1/4 w-1/2 h-1/2 bg-accent/10 rounded-full blur-[150px] pointer-events-none" />

      {/* Left side - Intro */}
      <div className="hidden lg:flex flex-1 flex-col justify-center items-center relative z-10 p-12">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <div className="relative inline-block mb-8">
            <motion.div 
              animate={{ 
                boxShadow: ['0 0 20px rgba(139,92,246,0.3)', '0 0 60px rgba(139,92,246,0.6)', '0 0 20px rgba(139,92,246,0.3)'] 
              }}
              transition={{ duration: 4, repeat: Infinity }}
              className="w-32 h-32 rounded-full bg-gradient-to-tr from-primary-DEFAULT to-accent flex items-center justify-center border-4 border-background"
            >
              <span className="text-white font-bold text-6xl">L</span>
            </motion.div>
            <Sparkles className="absolute -top-4 -right-4 w-8 h-8 text-accent animate-pulse-slow" />
          </div>
          <h1 className="text-5xl font-bold mb-6 tracking-tight text-white">Meet <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-DEFAULT to-accent text-glow">Luna</span></h1>
          <p className="text-xl text-slate-400 max-w-md mx-auto leading-relaxed">
            Your personal, intelligent voice companion. Ready to chat, remember, and assist.
          </p>
        </motion.div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex flex-col justify-center items-center z-10 p-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-md glass p-8 rounded-3xl shadow-2xl relative overflow-hidden"
        >
          {/* Form Tabs */}
          <div className="flex p-1 bg-white/5 rounded-xl mb-8 relative">
            <div className="flex-1 text-center relative z-10">
              <button 
                type="button"
                onClick={() => setIsLogin(true)}
                className={`w-full py-2 text-sm font-medium transition-colors ${isLogin ? 'text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Login
              </button>
            </div>
            <div className="flex-1 text-center relative z-10">
              <button 
                type="button"
                onClick={() => setIsLogin(false)}
                className={`w-full py-2 text-sm font-medium transition-colors ${!isLogin ? 'text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Register
              </button>
            </div>
            <motion.div 
              className="absolute top-1 bottom-1 w-[calc(50%-4px)] bg-primary-DEFAULT/40 rounded-lg backdrop-blur-md shadow-[0_0_10px_rgba(139,92,246,0.3)] z-0"
              animate={{ left: isLogin ? '4px' : 'calc(50% + 2px)' }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
            />
          </div>

          <AnimatePresence mode="wait">
            <motion.form
              key={isLogin ? 'login' : 'register'}
              initial={{ opacity: 0, x: isLogin ? -20 : 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: isLogin ? 20 : -20 }}
              transition={{ duration: 0.2 }}
              onSubmit={handleSubmit}
              className="space-y-4"
            >
              {!isLogin && (
                <div className="flex gap-4">
                  <Input 
                    label="First Name" 
                    name="first_name" 
                    value={formData.first_name} 
                    onChange={handleChange}
                    required={!isLogin}
                  />
                  <Input 
                    label="Last Name" 
                    name="last_name" 
                    value={formData.last_name} 
                    onChange={handleChange}
                    required={!isLogin}
                  />
                </div>
              )}
              <Input 
                type="email" 
                label="Email Address" 
                name="email" 
                value={formData.email} 
                onChange={handleChange}
                required
              />
              <Input 
                type="password" 
                label="Password" 
                name="password" 
                value={formData.password} 
                onChange={handleChange}
                required
              />
              
              {isLogin && (
                <div className="flex justify-end mt-2">
                  <Link to="/auth/reset-password" className="text-sm text-primary-DEFAULT hover:text-primary-DEFAULT/80 hover:underline transition-all">
                    Forgot password?
                  </Link>
                </div>
              )}

              <Button 
                type="submit" 
                className="w-full mt-6" 
                size="lg"
                isLoading={isLogin ? isLoggingIn : isRegistering}
              >
                {isLogin ? 'Sign In to Luna' : 'Create Account'}
              </Button>
            </motion.form>
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
};

export default AuthPage;
