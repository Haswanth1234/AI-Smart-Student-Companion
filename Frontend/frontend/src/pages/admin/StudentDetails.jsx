import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    User, Mail, Phone, Calendar, BookOpen, Award,
    CheckCircle, XCircle, ArrowLeft, Clock, AlertTriangle
} from 'lucide-react';
import { getStudentDetails } from '../../services/adminStudentService';
import Loader from '../../components/Loader';
import StatCard from '../../components/StatCard';
import ChartSection from '../../components/ChartSection'; // We might reuse this or create a simple one here

const StudentDetails = () => {
    const { studentId } = useParams();
    const navigate = useNavigate();
    const [student, setStudent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const data = await getStudentDetails(studentId);
                setStudent(data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        if (studentId) {
            fetchDetails();
        }
    }, [studentId]);

    if (loading) return <div className="flex-center" style={{ height: '80vh' }}><Loader /></div>;

    if (error) return (
        <div className="fade-in">
            <button onClick={() => navigate(-1)} className="btn glass-card" style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ArrowLeft size={16} /> Back
            </button>
            <div className="glass-card text-danger">
                <h3>Error loading student details</h3>
                <p>{error.message || String(error)}</p>
            </div>
        </div>
    );

    if (!student) return null;

    const { student_info, profile, attendance_summary, tasks_summary } = student;

    // Helper for safe access
    const getVal = (val, suffix = '') => val ? `${val}${suffix}` : 'N/A';

    return (
        <div className="fade-in">
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
                <button onClick={() => navigate(-1)} className="btn-icon" style={{ background: 'rgba(255,255,255,0.1)', border: 'none', color: 'white', borderRadius: '50%', width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
                    <ArrowLeft size={20} />
                </button>
                <div>
                    <h1 style={{ fontSize: '1.75rem', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        {student_info.name}
                        {student_info.profile_completed && <CheckCircle size={20} className="text-success" title="Profile Completed" />}
                    </h1>
                    <p className="text-secondary">{student_info.roll_number} • {student_info.department}</p>
                </div>
            </div>

            {/* Top Stats */}
            <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', marginBottom: '24px' }}>
                <StatCard
                    label="Attendance"
                    value={getVal(profile.attendance_percentage, '%')}
                    icon={CheckCircle}
                    color={profile.attendance_percentage >= 75 ? 'success' : 'danger'}
                />
                <StatCard
                    label="CGPA"
                    value={getVal(profile.cgpa)}
                    icon={Award}
                    color="accent"
                />
                <StatCard
                    label="Pending Tasks"
                    value={tasks_summary?.pending || 0}
                    icon={Clock}
                    color={tasks_summary?.pending > 0 ? 'warning' : 'success'}
                />
                <StatCard
                    label="Year / Sem"
                    value={`${getVal(profile.studying_year)} / ${getVal(profile.current_semester)}`}
                    icon={BookOpen}
                    color="primary"
                />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>

                {/* Left Column: Personal Info & Academic */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                    {/* Contact Info */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <User size={18} /> Personal Details
                        </h3>
                        <div style={{ display: 'grid', gap: '16px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <Mail size={16} className="text-secondary" />
                                <div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Email</div>
                                    <div>{getVal(student_info.email)}</div>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <Phone size={16} className="text-secondary" />
                                <div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Phone</div>
                                    <div>{getVal(student_info.phone)}</div>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <Calendar size={16} className="text-secondary" />
                                <div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Skills</div>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                                        {profile.skills && profile.skills.length > 0 ? (
                                            profile.skills.map((skill, i) => (
                                                <span key={i} style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '12px' }}>
                                                    {skill}
                                                </span>
                                            ))
                                        ) : <span className="text-secondary">No skills listed</span>}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Academic Performance (Simple Table for now) */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Award size={18} /> Performance
                        </h3>
                        {/* Placeholder for marks - user service returns sem_1_marks etc. */}
                        <div className="dashboard-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '8px' }}>
                                <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Sem 1 GPA</div>
                                <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{getVal(profile.sem_1_marks)}</div>
                            </div>
                            {/* Add more semesters if available in data */}
                        </div>
                    </div>

                </div>

                {/* Right Column: Attendance & Tasks */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                    {/* Recent Attendance */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Calendar size={18} /> Recent Attendance
                        </h3>
                        {attendance_summary?.recent && attendance_summary.recent.length > 0 ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {attendance_summary.recent.map((record, index) => (
                                    <div key={index} style={{
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                        padding: '10px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px'
                                    }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <div style={{
                                                width: '8px', height: '8px', borderRadius: '50%',
                                                background: record.status === 'present' ? 'var(--success-color)' : 'var(--danger-color)'
                                            }} />
                                            <span>{new Date(record.date).toLocaleDateString()}</span>
                                        </div>
                                        <span style={{
                                            textTransform: 'capitalize',
                                            color: record.status === 'present' ? 'var(--success-color)' : 'var(--danger-color)',
                                            fontWeight: '500', fontSize: '0.9rem'
                                        }}>
                                            {record.status}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-secondary">No recent attendance records.</p>
                        )}
                    </div>

                    {/* Task Summary */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <CheckCircle size={18} /> Task Overview
                        </h3>
                        <div style={{ display: 'flex', gap: '16px' }}>
                            <div style={{ flex: 1, background: 'rgba(16, 185, 129, 0.1)', padding: '16px', borderRadius: '12px', textAlign: 'center' }}>
                                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--success-color)' }}>
                                    {tasks_summary?.total ? tasks_summary.total - (tasks_summary.pending || 0) : 0}
                                </div>
                                <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Completed</div>
                            </div>
                            <div style={{ flex: 1, background: 'rgba(245, 158, 11, 0.1)', padding: '16px', borderRadius: '12px', textAlign: 'center' }}>
                                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--warning-color)' }}>
                                    {tasks_summary?.pending || 0}
                                </div>
                                <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Pending</div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default StudentDetails;
