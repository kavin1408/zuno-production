import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { supabase } from '../../../lib/supabase';

export function Signup() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    console.log('Attempting signup with:', { email });

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      });

      console.log('Signup response:', { data, error });

      if (error) {
        console.error('Signup error:', error);
        setError(error.message || 'Failed to create account. Please try again.');
      } else {
        console.log('Signup successful');
        // Check if email confirmation is required
        if (data.user && !data.session) {
          setSuccess('Account created! Please check your email to confirm your account.');
        } else {
          setSuccess('Account created successfully!');
          setTimeout(() => navigate('/onboarding'), 2000);
        }
      }
    } catch (err) {
      console.error('Signup exception:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Brand */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-medium text-white mb-3">Zuno</h1>
          <p className="text-gray-400">Let's build momentum together.</p>
        </div>

        {/* Signup Card */}
        <div className="bg-[#25252a] rounded-2xl p-8 border border-[#35353a]">
          <h2 className="text-2xl font-medium text-white mb-6">Create your account</h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-500/10 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg text-sm">
                {success}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-300">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
                className="bg-[#1a1a1e] border-[#35353a] text-white placeholder:text-gray-500 focus:border-indigo-500 focus:ring-indigo-500/20"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-gray-300">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                minLength={6}
                className="bg-[#1a1a1e] border-[#35353a] text-white placeholder:text-gray-500 focus:border-indigo-500 focus:ring-indigo-500/20"
              />
              <p className="text-xs text-gray-500">Password must be at least 6 characters</p>
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white h-11 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <Link
              to="/login"
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Already have an account?
            </Link>
          </div>
        </div>

        {/* Footer Quote */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500 italic">
            "Your future self will thank you."
          </p>
        </div>
      </div>
    </div>
  );
}
