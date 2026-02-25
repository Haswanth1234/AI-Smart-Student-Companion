import React, { useEffect, useState } from 'react';
import { Calendar, CheckCircle, AlertCircle } from 'lucide-react';
import { markAttendance } from '../../services/adminAttendanceService';
import { getStudentsList } from '../../services/adminStudentService';
import Loader from '../../components/Loader';

const Attendance = () => {
    // Removed activeTab state as there's only one view now
    // Removed summary state as it was used for Overview/Defaulters
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [markingDate, setMarkingDate] = useState(new Date().toISOString().split('T')[0]);
    const [attendanceStatus, setAttendanceStatus] = useState({}); // { studentId: 'present' | 'absent' }
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState(null);
    const [apiError, setApiError] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        setApiError(null);
        try {
            const studentsData = await getStudentsList();

            if (studentsData && studentsData.students) {
                setStudents(studentsData.students);
                // Initialize status
                const initialStatus = {};
                studentsData.students.forEach(s => {
                    initialStatus[s.id] = 'present';
                });
                setAttendanceStatus(initialStatus);
            } else {
                console.warn('Students data format unexpected:', studentsData);
            }
        } catch (err) {
            console.error('Failed to fetch students:', err);
            setApiError(`Failed to load student list: ${err.message || err}`);
        } finally {
            setLoading(false);
        }
    };

    const handleStatusChange = (studentId, status) => {
        setAttendanceStatus(prev => ({
            ...prev,
            [studentId]: status
        }));
    };

    const handleBulkSubmit = async () => {
        setSubmitting(true);
        setMessage(null);
        let successCount = 0;
        let errors = [];

        try {
            for (const student of students) {
                const status = attendanceStatus[student.id];
                try {
                    await markAttendance(student.id, markingDate, status);
                    successCount++;
                } catch (err) {
                    if (typeof err === 'string' && !err.includes('already exists')) {
                        errors.push(err);
                    }
                }
            }

            if (errors.length > 0) {
                setMessage({ type: 'warning', text: `Marked ${successCount} students. Some failed.` });
            } else {
                setMessage({ type: 'success', text: `Successfully marked attendance for ${successCount} students.` });
            }
        } catch (err) {
            setMessage({ type: 'error', text: 'Failed to submit attendance.' });
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="flex-center" style={{ height: '80vh' }}><Loader /></div>;

    return (
        <div className="main-content fade-in">
            <header className="mb-8">
                <h1 className="heading-lg mb-4">Mark Attendance</h1>

                {/* Error Banner */}
                {apiError && (
                    <div className="glass-card mb-4 border-l-4 border-l-red-500 flex items-center gap-2 text-danger">
                        <AlertCircle size={20} />
                        <strong>Error:</strong> {apiError}
                    </div>
                )}
            </header>

            {message && (
                <div className={`glass-card mb-6 text-${message.type} border-l-4 border-l-${message.type === 'success' ? 'green' : message.type === 'warning' ? 'yellow' : 'red'}-500`}>
                    {message.text}
                </div>
            )}

            <div className="glass-card">
                <div className="flex-between mb-6" style={{ flexWrap: 'wrap', gap: '1rem' }}>
                    <div className="flex items-center gap-4 modern-form">
                        <Calendar size={20} className="text-secondary" />
                        <input
                            type="date"
                            value={markingDate}
                            onChange={(e) => setMarkingDate(e.target.value)}
                            style={{ width: 'auto' }}
                        />
                    </div>
                    <button
                        className="neon-btn"
                        onClick={handleBulkSubmit}
                        disabled={submitting || students.length === 0}
                    >
                        {submitting ? 'Submitting...' : 'Submit Attendance'}
                    </button>
                </div>

                <div style={{ maxHeight: '60vh', overflowY: 'auto' }}>
                    <table className="glass-table glass-table-attendance">
                        <thead style={{ position: 'sticky', top: 0, background: 'var(--bg-card)', zIndex: 1, backdropFilter: 'blur(10px)' }}>
                            <tr>
                                <th>Student</th>
                                <th>Roll No</th>
                                <th className="text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {students.length === 0 && (
                                <tr>
                                    <td colSpan="3" className="text-center p-8 text-secondary">
                                        {apiError ? 'Could not load students.' : 'No students found in your department.'}
                                        <br />
                                        <small onClick={fetchData} className="cursor-pointer underline">Try Refreshing</small>
                                    </td>
                                </tr>
                            )}
                            {students.map(student => (
                                <tr key={student.id}>
                                    <td>
                                        <div className="font-medium text-primary">{student.name}</div>
                                    </td>
                                    <td className="text-secondary">{student.roll_number}</td>
                                    <td className="text-center">
                                        <div className="flex-center gap-2">
                                            <button
                                                onClick={() => handleStatusChange(student.id, 'present')}
                                                className={`px-4 py-1 rounded transition-all ${attendanceStatus[student.id] === 'present' ? 'bg-green-500 text-white shadow-lg' : 'bg-white/10 text-secondary'}`}
                                                style={{
                                                    background: attendanceStatus[student.id] === 'present' ? 'var(--success-color)' : 'rgba(255,255,255,0.1)',
                                                    opacity: attendanceStatus[student.id] === 'present' ? 1 : 0.6
                                                }}
                                            >
                                                P
                                            </button>
                                            <button
                                                onClick={() => handleStatusChange(student.id, 'absent')}
                                                className={`px-4 py-1 rounded transition-all ${attendanceStatus[student.id] === 'absent' ? 'bg-red-500 text-white shadow-lg' : 'bg-white/10 text-secondary'}`}
                                                style={{
                                                    background: attendanceStatus[student.id] === 'absent' ? 'var(--danger-color)' : 'rgba(255,255,255,0.1)',
                                                    opacity: attendanceStatus[student.id] === 'absent' ? 1 : 0.6
                                                }}
                                            >
                                                A
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Attendance;
