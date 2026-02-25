import React, { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getAttendance } from '../services/attendanceService';
import { Loader2, XCircle, CheckCircle } from 'lucide-react';

export default function AttendancePage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAttendance = async () => {
            try {
                const result = await getAttendance();
                if (result) {
                    // Backend returns: { statistics: { attendance_percentage: ... }, history: [...] }
                    // Map it to component state structure
                    setData({
                        attendance_percentage: result.statistics?.attendance_percentage || 0,
                        history: result.history?.map(record => ({
                            date: record.date,
                            status: record.status.charAt(0).toUpperCase() + record.status.slice(1) // Capitalize
                        })) || []
                    });
                } else {
                    // Fallback for empty state but NO MOCK DATA
                    setData({ attendance_percentage: 0, history: [] });
                }
            } catch (error) {
                console.error("Failed to fetch attendance:", error);
                setData({ attendance_percentage: 0, history: [] });
            } finally {
                setLoading(false);
            }
        };
        fetchAttendance();
    }, []);

    if (loading) return <div className="flex-center" style={{ height: '100vh' }}><Loader2 className="spinner" /></div>;

    return (
        <DashboardLayout title="Attendance">
            <div className="flex-center mb-6 flex-col">
                <div style={{
                    width: '150px', height: '150px', borderRadius: '50%',
                    background: `conic-gradient(var(--primary-color) ${data.attendance_percentage}%, transparent 0)`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    boxShadow: '0 0 30px rgba(100, 108, 255, 0.3)'
                }}>
                    <div className="flex-col flex-center" style={{
                        width: '130px', height: '130px', borderRadius: '50%', background: '#0f0f13',
                    }}>
                        <span className="text-3xl font-bold">{data.attendance_percentage}%</span>
                        <span className="text-secondary">Present</span>
                    </div>
                </div>
            </div>

            <h3 className="heading-md mb-4">History</h3>
            <div className="glass-panel">
                {data.history.length > 0 ? (
                    data.history.map((record, idx) => (
                        <div key={idx} className="flex-between" style={{ padding: '1rem', borderBottom: idx !== data.history.length - 1 ? '1px solid var(--glass-border)' : 'none' }}>
                            <span className="font-semibold">{record.date}</span>
                            <span className={`badge badge-${record.status === 'Present' ? 'success' : 'danger'} flex-center gap-2`}>
                                {record.status === 'Present' ? <CheckCircle size={14} /> : <XCircle size={14} />}
                                {record.status}
                            </span>
                        </div>
                    ))
                ) : (
                    <div className="p-4 text-center text-secondary">No attendance records found.</div>
                )}
            </div>
        </DashboardLayout>
    );
}
