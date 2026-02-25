import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#f87171', '#fbbf24', '#34d399']; // Red, Yellow, Green

const LearningLevelChart = ({ data }) => {
    // Transform data object { slow: 25, intermediate: 65, advanced: 30 } into array
    const chartData = [
        { name: 'Slow', value: data.slow || 0 },
        { name: 'Intermediate', value: data.intermediate || 0 },
        { name: 'Advanced', value: data.advanced || 0 },
    ];

    return (
        <div className="glass-card" style={{ height: '400px', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ marginBottom: '24px' }}>Learning Levels</h3>
            <div style={{ flex: 1, width: '100%', position: 'relative', minHeight: 0, minWidth: 0 }}>
                <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', minWidth: 0, minHeight: 0 }}>
                    <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                        <PieChart>
                            <Pie
                                data={chartData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={100}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {chartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: '8px',
                                    color: '#fff'
                                }}
                            />
                            <Legend verticalAlign="bottom" height={36} />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default LearningLevelChart;
