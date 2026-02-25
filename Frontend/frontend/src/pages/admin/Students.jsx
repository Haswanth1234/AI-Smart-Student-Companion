import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Eye, MoreHorizontal, Download } from 'lucide-react';
import { getStudentsList } from '../../services/adminStudentService';
import Loader from '../../components/Loader';

const Students = () => {
    const navigate = useNavigate();
    const [students, setStudents] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filter, setFilter] = useState('all'); // all, low_attendance

    useEffect(() => {
        fetchStudents();
    }, []);

    const fetchStudents = async () => {
        try {
            setLoading(true);
            const data = await getStudentsList();
            setStudents(data.students);
            setStatistics(data.statistics);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const filteredStudents = students.filter(student => {
        const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.roll_number.toLowerCase().includes(searchTerm.toLowerCase());

        if (filter === 'low_attendance') {
            return matchesSearch && student.attendance_percentage < 75;
        }
        return matchesSearch;
    });

    if (loading) return <div className="flex-center" style={{ height: '80vh' }}><Loader /></div>;
    if (error) return <div className="text-danger">Error: {error}</div>;

    return (
        <div className="fade-in">
            <header style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>Students</h1>
                    <p className="text-secondary">Manage and view student performance.</p>
                </div>
            </header>

            {/* Statistics Row */}
            {statistics && (
                <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
                    <div className="glass-card">
                        <p className="text-secondary" style={{ fontSize: '0.875rem', marginBottom: '8px' }}>Total Students</p>
                        <h3 style={{ fontSize: '1.75rem' }}>{statistics.total_students}</h3>
                    </div>
                    <div className="glass-card">
                        <p className="text-secondary" style={{ fontSize: '0.875rem', marginBottom: '8px' }}>Profiles Completed</p>
                        <h3 style={{ fontSize: '1.75rem' }} className="text-success">{statistics.students_with_profile}</h3>
                    </div>
                    <div className="glass-card">
                        <p className="text-secondary" style={{ fontSize: '0.875rem', marginBottom: '8px' }}>Profiles Pending</p>
                        <h3 style={{ fontSize: '1.75rem' }} className="text-warning">{statistics.students_without_profile}</h3>
                    </div>
                </div>
            )}

            {/* Controls */}
            <div className="glass-card" style={{ marginBottom: '24px', padding: '16px' }}>
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                    <div style={{ flex: 1, position: 'relative' }}>
                        <Search size={20} className="text-secondary" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                        <input
                            type="text"
                            placeholder="Search by Name or Roll No..."
                            className="glass-input"
                            style={{ paddingLeft: '40px', width: '100%' }}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <select
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                        className="glass-input"
                        style={{ width: 'auto', minWidth: '200px' }}
                    >
                        <option value="all" style={{ background: '#1a1a2e' }}>All Students</option>
                        <option value="low_attendance" style={{ background: '#1a1a2e' }}>Low Attendance (&lt;75%)</option>
                    </select>

                    <button className="btn btn-secondary glass-input" style={{ width: 'auto', cursor: 'pointer' }}>
                        <Download size={18} /> Export
                    </button>
                </div>
            </div>

            {/* Table */}
            <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
                <div style={{ overflowX: 'auto' }}>
                    <table className="glass-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Roll Number</th>
                                <th>Year/Sem</th>
                                <th>Attendance</th>
                                <th>CGPA</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredStudents.length > 0 ? (
                                filteredStudents.map((student) => (
                                    <tr key={student.id}>
                                        <td>
                                            <div style={{ fontWeight: '500' }}>{student.name}</div>
                                            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{student.email}</div>
                                        </td>
                                        <td>{student.roll_number}</td>
                                        <td>
                                            {student.studying_year !== 'N/A' ? `${student.studying_year} Year / ${student.semester} Sem` : '-'}
                                        </td>
                                        <td>
                                            <span className={student.attendance_percentage < 75 ? 'text-danger' : 'text-success'} style={{ fontWeight: 'bold' }}>
                                                {student.attendance_percentage}%
                                            </span>
                                        </td>
                                        <td>{student.cgpa}</td>
                                        <td>
                                            <button
                                                className="btn-icon"
                                                title="View Details"
                                                style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', cursor: 'pointer', opacity: 0.8 }}
                                                onMouseOver={(e) => e.currentTarget.style.opacity = 1}
                                                onMouseOut={(e) => e.currentTarget.style.opacity = 0.8}
                                                onClick={() => navigate(`/admin/students/${student.id}`)}
                                            >
                                                <Eye size={18} />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                        No students found matching your search.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Students;
