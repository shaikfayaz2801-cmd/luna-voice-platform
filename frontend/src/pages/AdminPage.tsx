import React from 'react';
import { Users, Activity, Server, Database, ShieldCheck } from 'lucide-react';

const AdminPage = () => {
  const stats = [
    { label: 'Total Users', value: '1,248', icon: Users, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Active Sessions', value: '142', icon: Activity, color: 'text-green-400', bg: 'bg-green-400/10' },
    { label: 'System Health', value: '99.9%', icon: ShieldCheck, color: 'text-primary-DEFAULT', bg: 'bg-primary-DEFAULT/10' },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-white mb-8">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className="glass p-6 rounded-2xl flex items-center gap-4 border border-white/5">
            <div className={`p-4 rounded-xl ${stat.bg} ${stat.color}`}>
              <stat.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400 font-medium uppercase tracking-wider">{stat.label}</p>
              <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass rounded-3xl p-6 border border-white/5">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <Server className="w-5 h-5 text-slate-400" /> Infrastructure Status
          </h2>
          <div className="space-y-4">
            {['API Server', 'Websocket Server', 'Redis Cache', 'Celery Workers'].map((service) => (
              <div key={service} className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                <span className="text-white font-medium">{service}</span>
                <span className="flex items-center gap-2 text-sm text-green-400 bg-green-400/10 px-3 py-1 rounded-full">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  Operational
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-3xl p-6 border border-white/5">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <Database className="w-5 h-5 text-slate-400" /> Recent Users
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-400">
              <thead className="text-xs uppercase bg-white/5 text-slate-300">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">User</th>
                  <th className="px-4 py-3">Role</th>
                  <th className="px-4 py-3 rounded-tr-lg">Status</th>
                </tr>
              </thead>
              <tbody>
                {[1, 2, 3, 4].map((i) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="px-4 py-4 text-white font-medium">user{i}@example.com</td>
                    <td className="px-4 py-4">User</td>
                    <td className="px-4 py-4"><span className="text-green-400">Active</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
