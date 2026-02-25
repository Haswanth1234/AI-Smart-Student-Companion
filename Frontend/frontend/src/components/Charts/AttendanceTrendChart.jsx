import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const AttendanceTrendChart = ({ data }) => {
    // data is array of percentages [82, 78, 80...]
    // convert to object array for Recharts
    const chartData = data.map((val, index) => ({
        day: `Day ${index + 1}`,
        attendance: val
    }));

    return (
        <div className="glass-card" style={{ height: '400px', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ marginBottom: '24px' }}>Attendance Trend (Weekly)</h3>
            <div style={{ flex: 1, width: '100%', position: 'relative', minHeight: 0, minWidth: 0 }}>
                <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', minWidth: 0, minHeight: 0 }}>
                    <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                        <LineChart
                            data={chartData}
                            margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis dataKey="day" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" domain={[0, 100]} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: '8px',
                                    color: '#fff'
                                }}
                            />
                            <Line
                                type="monotone"
                                dataKey="attendance"
                                stroke="#38bdf8"
                                strokeWidth={3}
                                dot={{ fill: '#38bdf8', strokeWidth: 2 }}
                                activeDot={{ r: 8 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default AttendanceTrendChart;
