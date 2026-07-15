import { Doughnut, Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js';
import { BarChart2, TrendingUp, Users, Percent } from 'lucide-react';
import GlassCard from './GlassCard';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
);

export default function PageStats() {
  
  // Set global Chart.js configuration overrides
  ChartJS.defaults.color = '#a1a1aa'; // gray-400
  ChartJS.defaults.font.family = 'Inter, sans-serif';

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          font: { family: 'Inter', size: 11 },
          color: '#a1a1aa',
          usePointStyle: true,
          boxWidth: 6,
        }
      },
      tooltip: {
        backgroundColor: '#0a0a0c',
        titleColor: '#fff',
        bodyColor: '#e4e4e7',
        borderColor: 'rgba(255,255,255,0.06)',
        borderWidth: 1,
        padding: 12,
        boxPadding: 6,
        usePointStyle: true,
        cornerRadius: 8,
      }
    }
  };

  const gridDefaults = {
    color: 'rgba(255, 255, 255, 0.02)',
    drawBorder: false,
  };

  // 1. Doughnut: Outcome Distribution
  const doughnutData = {
    labels: ['Conviction', 'Acquittal'],
    datasets: [{
      data: [50, 16],
      backgroundColor: ['#ef4444', '#10b981'],
      borderWidth: 2,
      borderColor: '#030303',
      hoverOffset: 8
    }]
  };

  const doughnutOptions = {
    ...chartOptions,
    cutout: '72%',
    plugins: {
      ...chartOptions.plugins,
      legend: {
        position: 'bottom' as const,
        labels: {
          ...chartOptions.plugins.legend.labels,
          padding: 20
        }
      }
    }
  };

  // 2. Bar: Cases by IPC Section
  const barData = {
    labels: ['IPC 379', 'IPC 420', 'IPC 323', 'IPC 380', 'IPC 468', 'IPC 392', 'Other'],
    datasets: [{
      label: 'Number of Cases',
      data: [10, 10, 8, 6, 6, 4, 56],
      backgroundColor: '#3b82f6',
      borderRadius: 8,
      hoverBackgroundColor: '#60a5fa',
      borderWidth: 0,
      barPercentage: 0.55
    }]
  };

  const barOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      legend: { display: false }
    },
    scales: {
      x: { grid: { display: false }, ticks: { color: '#a1a1aa' } },
      y: { grid: gridDefaults, beginAtZero: true, ticks: { color: '#a1a1aa' } }
    }
  };

  // 3. Line: Cross-Validation Accuracy
  const lineData = {
    labels: ['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5'],
    datasets: [{
      label: 'Accuracy %',
      data: [95, 100, 90, 100, 85],
      borderColor: '#8b5cf6',
      backgroundColor: (context: any) => {
        const ctx = context.chart.ctx;
        const gradient = ctx.createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.25)');
        gradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');
        return gradient;
      },
      pointBackgroundColor: '#030303',
      pointBorderColor: '#8b5cf6',
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 7,
      fill: true,
      tension: 0.38
    }]
  };

  const lineOptions = {
    ...chartOptions,
    scales: {
      y: { min: 80, max: 105, grid: gridDefaults, ticks: { color: '#a1a1aa' } },
      x: { grid: { display: false }, ticks: { color: '#a1a1aa' } }
    }
  };

  const statCards = [
    { title: 'Model Accuracy', value: '94.0%', change: 'Cross Validated', icon: Percent, color: 'var(--accent-blue)' },
    { title: 'Model Precision', value: '94.6%', change: 'IPC Evaluation', icon: TrendingUp, color: 'var(--accent-purple)' },
    { title: 'Model Recall', value: '94.0%', change: 'True Positive', icon: BarChart2, color: 'var(--accent-blue)' },
    { title: 'Trained Cases', value: '4.5k+', change: 'Curated Database', icon: Users, color: 'var(--accent-purple)' },
  ];

  return (
    <div style={{ padding: '40px 0' }}>
      
      {/* Title */}
      <div style={{ marginBottom: '36px', textAlign: 'center' }}>
        <h2 className="glow-gradient-text" style={{ fontSize: '28px', fontWeight: 700, margin: 0 }}>
          Model Statistics
        </h2>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: '8px 0 0' }}>
          Real-time metrics, classifier evaluations, and structural data allocations.
        </p>
      </div>

      {/* Grid of Stat Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '36px' }}>
        {statCards.map((sc, index) => {
          const Icon = sc.icon;
          return (
            <GlassCard key={index} delay={index * 0.05} hoverEffect={true} style={{ padding: '24px', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '4px',
                background: `linear-gradient(90deg, ${sc.color}, transparent)`
              }} />
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '14px', color: sc.color }}>
                <Icon size={18} />
              </div>
              <div style={{ fontSize: '28px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)', margin: '0 0 4px' }}>
                {sc.value}
              </div>
              <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '4px' }}>
                {sc.title}
              </div>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                {sc.change}
              </div>
            </GlassCard>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        
        {/* Doughnut Chart */}
        <GlassCard hoverEffect={false} style={{ padding: '28px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', marginBottom: '20px' }}>
            Outcome Distribution
          </h3>
          <div style={{ height: '240px', position: 'relative' }}>
            <Doughnut data={doughnutData} options={doughnutOptions} />
          </div>
        </GlassCard>

        {/* Bar Chart */}
        <GlassCard hoverEffect={false} style={{ padding: '28px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', marginBottom: '20px' }}>
            Cases by IPC Section
          </h3>
          <div style={{ height: '240px', position: 'relative' }}>
            <Bar data={barData} options={barOptions} />
          </div>
        </GlassCard>

        {/* Line Chart spanning full width */}
        <GlassCard hoverEffect={false} style={{ padding: '28px', gridColumn: '1 / -1' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', marginBottom: '20px' }}>
            Cross-Validation Accuracy (5-Fold)
          </h3>
          <div style={{ height: '220px', position: 'relative' }}>
            <Line data={lineData} options={lineOptions} />
          </div>
        </GlassCard>

      </div>

    </div>
  );
}
