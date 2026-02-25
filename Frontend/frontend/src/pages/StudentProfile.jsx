import React, { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getProfile, updateProfile } from '../services/profileService';
import { Loader2, Save, BarChart as BarChartIcon } from 'lucide-react';
import {
    ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
    CartesianGrid, Tooltip as RechartsTooltip, Cell
} from 'recharts';

export default function StudentProfile() {
    const [profile, setProfile] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const data = await getProfile();
            // Flatten the response structure
            setProfile({
                name: data.user_info?.name,
                email: data.user_info?.email,
                phone: data.user_info?.phone || '',
                department: data.user_info?.department || '',
                year: data.profile?.studying_year ? `${data.profile.studying_year}rd Year` : '', // Visual format
                semester: data.profile?.semester ? `${data.profile.semester}th Sem` : '',
                studying_year: data.profile?.studying_year, // Store raw value
                raw_semester: data.profile?.semester, // Store raw value
                semester_marks: data.profile?.semester_marks || [],
                passout_year: data.profile?.passout_year || '',
                attendance_percentage: data.profile?.attendance_percentage || 0,
                interested_domain: data.profile?.interested_domain || '',
                skills: data.profile?.skills || []
            });
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);

        // Helper to extract number from string
        const extractNumber = (str) => {
            if (!str) return null;
            if (typeof str === 'number') return str;
            const match = str.toString().match(/\d+/);
            return match ? parseInt(match[0], 10) : null;
        };

        const payload = {
            name: profile.name,
            email: profile.email,
            phone: profile.phone,
            department: profile.department,
            studying_year: extractNumber(profile.year),
            semester: extractNumber(profile.semester),
            semester_marks: profile.semester_marks, // Already in [{subject, marks}] format
            passout_year: Number(profile.passout_year),
            interested_domain: profile.interested_domain,
            skills: profile.skills
        };

        try {
            await updateProfile(payload);
            // Refresh to get confirmed data
            const data = await getProfile();
            setProfile({
                name: data.user_info?.name,
                email: data.user_info?.email,
                department: data.user_info?.department || 'Computer Science',
                year: data.profile?.studying_year ? `${data.profile.studying_year}rd Year` : '',
                semester: data.profile?.semester ? `${data.profile.semester}th Sem` : '',
                studying_year: data.profile?.studying_year,
                raw_semester: data.profile?.semester,
                semester_marks: data.profile?.semester_marks || [],
                passout_year: data.profile?.passout_year || '',
                attendance_percentage: data.profile?.attendance_percentage || 0,
                interested_domain: data.profile?.interested_domain || '',
                skills: data.profile?.skills || []
            });
            alert("Profile updated successfully!");
        } catch (err) {
            console.error(err);
            alert("Failed to update profile: " + (typeof err === 'string' ? err : 'Validation failed'));
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="flex-center" style={{ height: '100vh' }}><Loader2 className="spinner" /></div>;

    // Filter out empty subjects for the chart
    const chartData = (profile.semester_marks || [])
        .filter(item => item.subject && item.marks !== '')
        .map(item => ({
            name: item.subject,
            marks: Number(item.marks)
        }));

    return (
        <DashboardLayout title="My Profile">
            {/* PERFORMANCE CHART SECTION */}
            <div className="glass-panel" style={{
                padding: '1.5rem',
                maxWidth: '800px',
                margin: '0 auto 2rem auto',
                background: 'linear-gradient(135deg, rgba(100, 108, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)'
            }}>
                <div className="flex-center mb-6" style={{ justifyContent: 'flex-start', gap: '0.75rem' }}>
                    <BarChartIcon size={22} color="var(--primary-color)" />
                    <h3 className="heading-md" style={{ margin: 0 }}>Academic Performance</h3>
                </div>

                <div style={{ width: '100%', height: '250px', minWidth: 0, minHeight: 0 }}>
                    {chartData.length > 0 ? (
                        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                                <XAxis
                                    dataKey="name"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                                    domain={[0, 100]}
                                />
                                <RechartsTooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                                    contentStyle={{
                                        background: 'rgba(15, 23, 42, 0.95)',
                                        border: '1px solid var(--glass-border)',
                                        borderRadius: '12px',
                                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                                    }}
                                    itemStyle={{ color: 'var(--primary-color)', fontWeight: 'bold' }}
                                />
                                <Bar
                                    dataKey="marks"
                                    radius={[6, 6, 0, 0]}
                                    animationDuration={1500}
                                    barSize={40}
                                >
                                    {chartData.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={entry.marks >= 80 ? '#4ade80' : entry.marks >= 60 ? '#646cff' : '#f87171'}
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    ) : (
                        <div className="flex-center flex-col text-secondary" style={{ height: '100%' }}>
                            <p>Add subjects and marks below to see your performance graph.</p>
                        </div>
                    )}
                </div>
            </div>

            {/* PROFILE FORM SECTION */}
            <div className="glass-panel" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
                <form onSubmit={handleSubmit} className="modern-form grid-cols-2">
                    {/* Row 1 */}
                    <div className="input-group">
                        <label>Full Name</label>
                        <input
                            value={profile.name || ''}
                            onChange={e => setProfile({ ...profile, name: e.target.value })}
                            placeholder="Your Full Name"
                        />
                    </div>
                    <div className="input-group">
                        <label>Email</label>
                        <input
                            value={profile.email || ''}
                            onChange={e => setProfile({ ...profile, email: e.target.value })}
                            placeholder="your.email@example.com"
                        />
                    </div>

                    {/* Row 2 */}
                    <div className="input-group">
                        <label>Phone Number</label>
                        <input
                            value={profile.phone || ''}
                            onChange={e => setProfile({ ...profile, phone: e.target.value })}
                            placeholder="Enter phone number"
                        />
                    </div>
                    <div className="input-group">
                        <label>Department</label>
                        <input
                            value={profile.department || ''}
                            onChange={e => setProfile({ ...profile, department: e.target.value })}
                            placeholder="e.g. Computer Science"
                        />
                    </div>

                    {/* Row 3 */}
                    <div className="input-group">
                        <label>Year</label>
                        <input
                            type="number"
                            value={profile.studying_year || ''}
                            onChange={e => setProfile({ ...profile, studying_year: e.target.value, year: e.target.value })}
                            placeholder="e.g. 3"
                        />
                    </div>
                    <div className="input-group">
                        <label>Semester</label>
                        <input
                            type="number"
                            value={profile.raw_semester || ''}
                            onChange={e => setProfile({ ...profile, raw_semester: e.target.value, semester: e.target.value })}
                            placeholder="e.g. 5"
                        />
                    </div>

                    {/* Row 4 */}
                    <div className="input-group">
                        <label>Passout Year</label>
                        <input
                            type="number"
                            value={profile.passout_year || ''}
                            onChange={e => setProfile({ ...profile, passout_year: e.target.value })}
                            placeholder="e.g. 2026"
                        />
                    </div>
                    <div className="input-group">
                        <label>Attendance (%)</label>
                        <input
                            type="text"
                            value={profile.attendance_percentage ? profile.attendance_percentage + '%' : '0%'}
                            disabled
                            style={{ opacity: 0.7, fontWeight: 'bold', color: 'var(--primary-color)' }}
                        />
                    </div>

                    {/* Row 5 */}
                    <div className="input-group">
                        <label>Interested Domain</label>
                        <input
                            value={profile.interested_domain || ''}
                            onChange={e => setProfile({ ...profile, interested_domain: e.target.value })}
                            placeholder="e.g. AI/ML"
                        />
                    </div>
                    <div className="input-group">
                        <label>Skills (comma separated)</label>
                        <input
                            value={profile.skills ? (Array.isArray(profile.skills) ? profile.skills.join(', ') : profile.skills) : ''}
                            onChange={e => setProfile({ ...profile, skills: e.target.value.split(',').map(s => s.trim()) })}
                            placeholder="Python, React, Java..."
                        />
                    </div>

                    {/* Row 6: Semester Marks (Full Width) */}
                    <div className="input-group" style={{ gridColumn: '1 / -1' }}>
                        <label className="heading-md" style={{ fontSize: '1.1rem', marginBottom: '0.5rem', color: 'var(--primary-color)' }}>
                            Semester Marks & Subjects
                        </label>
                        <div className="marks-container" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {Array.isArray(profile.semester_marks) && profile.semester_marks.map((item, index) => (
                                <div key={index} style={{ display: 'grid', gridTemplateColumns: '1fr 120px auto', gap: '1rem', alignItems: 'center' }}>
                                    <input
                                        placeholder="Subject Name"
                                        value={item.subject || ''}
                                        onChange={e => {
                                            const newMarks = [...profile.semester_marks];
                                            newMarks[index] = { ...newMarks[index], subject: e.target.value };
                                            setProfile({ ...profile, semester_marks: newMarks });
                                        }}
                                    />
                                    <input
                                        type="number"
                                        placeholder="Marks"
                                        value={item.marks || ''}
                                        onChange={e => {
                                            const newMarks = [...profile.semester_marks];
                                            newMarks[index] = { ...newMarks[index], marks: Number(e.target.value) };
                                            setProfile({ ...profile, semester_marks: newMarks });
                                        }}
                                    />
                                    <button
                                        type="button"
                                        onClick={() => {
                                            const newMarks = profile.semester_marks.filter((_, i) => i !== index);
                                            setProfile({ ...profile, semester_marks: newMarks });
                                        }}
                                        className="btn-danger"
                                        style={{
                                            padding: '0.6rem',
                                            borderRadius: '12px',
                                            background: 'rgba(239, 68, 68, 0.1)',
                                            color: '#ef4444',
                                            border: '1px solid rgba(239, 68, 68, 0.2)',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            height: '42px',
                                            width: '42px'
                                        }}
                                    >
                                        ✕
                                    </button>
                                </div>
                            ))}
                            <button
                                type="button"
                                onClick={() => setProfile({ ...profile, semester_marks: [...(profile.semester_marks || []), { subject: '', marks: '' }] })}
                                className="btn-secondary"
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    borderRadius: '12px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    color: 'var(--text-secondary)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    cursor: 'pointer',
                                    width: 'fit-content',
                                    fontWeight: 500
                                }}
                            >
                                + Add Subject
                            </button>
                        </div>
                    </div>

                    <div style={{ gridColumn: '1 / -1', marginTop: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
                        <button type="submit" className="neon-btn" disabled={saving}>
                            {saving ? <Loader2 className="spinner" /> : <><Save size={18} style={{ marginRight: '0.5rem' }} /> Save Changes</>}
                        </button>
                    </div>
                </form>
            </div>
        </DashboardLayout>
    );
}
