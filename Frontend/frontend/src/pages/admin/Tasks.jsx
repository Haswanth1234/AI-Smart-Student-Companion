import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle, Clock, AlertCircle, Search, Filter, Plus, X, Trash2, Edit } from 'lucide-react';
import { getTasks, createTask, updateTask, deleteTask } from '../../services/adminTaskService';
import Loader from '../../components/Loader';
import { getStudentsList } from '../../services/adminStudentService';

const Tasks = () => {
    const [tasks, setTasks] = useState([]);
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filterStatus, setFilterStatus] = useState('all'); // all, pending, completed
    const [searchTerm, setSearchTerm] = useState('');

    // Modal State
    const [showModal, setShowModal] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentTask, setCurrentTask] = useState(null);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        student_id: '',
        priority: 'medium',
        due_date: '',
        status: 'pending'
    });
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [tasksData, studentsData] = await Promise.all([
                getTasks(),
                getStudentsList()
            ]);
            setTasks(tasksData);
            setStudents(studentsData.students || []);
            setError(null);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleOpenModal = (task = null) => {
        if (task) {
            setIsEditing(true);
            setCurrentTask(task);
            setFormData({
                title: task.title,
                description: task.description || '',
                student_id: task.student_id,
                priority: task.priority,
                due_date: task.due_date ? new Date(task.due_date).toISOString().split('T')[0] : '',
                status: task.status
            });
        } else {
            setIsEditing(false);
            setCurrentTask(null);
            setFormData({
                title: '',
                description: '',
                student_id: '',
                priority: 'medium',
                due_date: '',
                status: 'pending'
            });
        }
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSubmitting(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            if (isEditing) {
                await updateTask(currentTask._id, formData);
            } else {
                await createTask(formData);
            }
            fetchData(); // Refresh list
            handleCloseModal();
        } catch (err) {
            setError(err);
        } finally {
            setSubmitting(false);
        }
    };

    const handleDelete = async (taskId) => {
        if (window.confirm('Are you sure you want to delete this task?')) {
            try {
                await deleteTask(taskId);
                setTasks(prev => prev.filter(t => t._id !== taskId));
            } catch (err) {
                setError(err);
            }
        }
    };

    const getPriorityColor = (p) => {
        switch (p) {
            case 'high': return 'var(--danger-color)';
            case 'medium': return 'var(--warning-color)';
            case 'low': return 'var(--success-color)';
            default: return 'var(--text-secondary)';
        }
    };

    const filteredTasks = tasks.filter(task => {
        const matchesStatus = filterStatus === 'all' || task.status === filterStatus;
        const matchesSearch =
            task.student_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            task.student_roll?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            task.title?.toLowerCase().includes(searchTerm.toLowerCase());

        return matchesStatus && matchesSearch;
    });

    if (loading) return <div className="flex-center" style={{ height: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}><Loader /></div>;

    return (
        <div className="fade-in">
            <header style={{ marginBottom: '32px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <div>
                        <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>Student Tasks</h1>
                        <p className="text-secondary">Manage and assign tasks to students.</p>
                    </div>
                    <button className="btn btn-primary" onClick={() => handleOpenModal()} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Plus size={18} /> Create Task
                    </button>
                </div>

                <div style={{ marginTop: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
                    {/* Search Bar */}
                    <div style={{ position: 'relative', minWidth: '320px', flex: '1 1 auto' }}>
                        <Search size={20} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                        <input
                            type="text"
                            placeholder="Search by student name, roll no, or task..."
                            className="glass-input"
                            style={{ paddingLeft: '48px', width: '100%' }}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    {/* Filter Buttons */}
                    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                        <select
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value)}
                            className="glass-input"
                            style={{ width: 'auto', minWidth: '160px' }}
                        >
                            <option value="all" style={{ background: '#1a1a2e' }}>All Tasks</option>
                            <option value="pending" style={{ background: '#1a1a2e' }}>Pending</option>
                            <option value="completed" style={{ background: '#1a1a2e' }}>Completed</option>
                        </select>
                    </div>
                </div>
            </header>

            {error && (
                <div className="glass-card text-danger" style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <AlertCircle size={20} />
                    Error: {error.message || String(error)}
                </div>
            )}

            <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
                {filteredTasks.length === 0 ? (
                    <div className="text-center" style={{ padding: '4rem 1.5rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
                        <CheckCircle size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                        <p>No {filterStatus !== 'all' ? filterStatus : ''} tasks found matching your search.</p>
                    </div>
                ) : (
                    <div style={{ overflowX: 'auto' }}>
                        <table className="glass-table">
                            <thead>
                                <tr>
                                    <th>Student Details</th>
                                    <th>Task</th>
                                    <th>Due Date</th>
                                    <th className="text-center" style={{ textAlign: 'center' }}>Priority</th>
                                    <th className="text-center" style={{ textAlign: 'center' }}>Status</th>
                                    <th className="text-center" style={{ textAlign: 'center' }}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredTasks.map(task => (
                                    <tr key={task._id}>
                                        <td>
                                            <div style={{ fontWeight: '500', color: 'var(--text-primary)', marginBottom: '4px' }}>{task.student_name}</div>
                                            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{task.student_roll}</div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: '500', marginBottom: '4px' }}>{task.title}</div>
                                            {task.description && (
                                                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                    {task.description}
                                                </div>
                                            )}
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                                                <Calendar size={16} />
                                                {new Date(task.due_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                                            </div>
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            <span style={{
                                                padding: '4px 12px',
                                                borderRadius: '20px',
                                                fontSize: '0.75rem',
                                                fontWeight: '600',
                                                background: getPriorityColor(task.priority),
                                                color: '#fff',
                                                textTransform: 'uppercase',
                                                letterSpacing: '0.05em',
                                                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                                            }}>
                                                {task.priority}
                                            </span>
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            {task.status === 'completed' ? (
                                                <span className="text-success" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontWeight: '500', background: 'rgba(16, 185, 129, 0.1)', padding: '4px 12px', borderRadius: '20px' }}>
                                                    <CheckCircle size={14} /> Completed
                                                </span>
                                            ) : (
                                                <span className="text-warning" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontWeight: '500', background: 'rgba(245, 158, 11, 0.1)', padding: '4px 12px', borderRadius: '20px' }}>
                                                    <Clock size={14} /> Pending
                                                </span>
                                            )}
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                                                <button
                                                    onClick={() => handleOpenModal(task)}
                                                    style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: '4px' }}
                                                    title="Edit Task"
                                                >
                                                    <Edit size={16} />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(task._id)}
                                                    style={{ background: 'transparent', border: 'none', color: 'var(--danger-color)', cursor: 'pointer', padding: '4px' }}
                                                    title="Delete Task"
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <div style={{ marginTop: '20px', textAlign: 'right', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                Showing {filteredTasks.length} tasks
            </div>

            {/* Task Modal */}
            {showModal && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
                    display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
                }}>
                    <div className="glass-card" style={{ width: '90%', maxWidth: '500px', maxHeight: '90vh', overflowY: 'auto', position: 'relative' }}>
                        <button
                            onClick={handleCloseModal}
                            style={{ position: 'absolute', right: '16px', top: '16px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer' }}
                        >
                            <X size={20} />
                        </button>

                        <h2 style={{ marginBottom: '24px', fontSize: '1.5rem' }}>{isEditing ? 'Edit Task' : 'Create Task'}</h2>

                        <form onSubmit={handleSubmit}>
                            <div style={{ marginBottom: '16px' }}>
                                <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Task Title</label>
                                <input
                                    type="text"
                                    name="title"
                                    className="glass-input"
                                    placeholder="e.g. Submit Project Report"
                                    value={formData.title}
                                    onChange={handleChange}
                                    required
                                    style={{ width: '100%' }}
                                />
                            </div>

                            <div style={{ marginBottom: '16px' }}>
                                <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Description</label>
                                <textarea
                                    name="description"
                                    className="glass-input"
                                    rows="3"
                                    placeholder="Task details..."
                                    value={formData.description}
                                    onChange={handleChange}
                                    style={{ width: '100%', resize: 'vertical' }}
                                ></textarea>
                            </div>

                            <div style={{ marginBottom: '16px' }}>
                                <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Assign To (Student)</label>
                                <select
                                    name="student_id"
                                    className="glass-input"
                                    value={formData.student_id}
                                    onChange={handleChange}
                                    required
                                    disabled={isEditing} // Prevent changing student on edit for simplicity, or allow if needed
                                    style={{ width: '100%' }}
                                >
                                    <option value="" style={{ background: '#1a1a2e' }}>Select Student</option>
                                    {students.map(student => (
                                        <option key={student.id} value={student.id} style={{ background: '#1a1a2e' }}>
                                            {student.name} ({student.roll_number})
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                                <div style={{ flex: 1 }}>
                                    <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Priority</label>
                                    <select
                                        name="priority"
                                        className="glass-input"
                                        value={formData.priority}
                                        onChange={handleChange}
                                        style={{ width: '100%' }}
                                    >
                                        <option value="low" style={{ background: '#1a1a2e' }}>Low</option>
                                        <option value="medium" style={{ background: '#1a1a2e' }}>Medium</option>
                                        <option value="high" style={{ background: '#1a1a2e' }}>High</option>
                                    </select>
                                </div>
                                <div style={{ flex: 1 }}>
                                    <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Due Date</label>
                                    <input
                                        type="date"
                                        name="due_date"
                                        className="glass-input"
                                        value={formData.due_date}
                                        onChange={handleChange}
                                        required
                                        style={{ width: '100%' }}
                                    />
                                </div>
                            </div>

                            {isEditing && (
                                <div style={{ marginBottom: '24px' }}>
                                    <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Status</label>
                                    <select
                                        name="status"
                                        className="glass-input"
                                        value={formData.status}
                                        onChange={handleChange}
                                        style={{ width: '100%' }}
                                    >
                                        <option value="pending" style={{ background: '#1a1a2e' }}>Pending</option>
                                        <option value="completed" style={{ background: '#1a1a2e' }}>Completed</option>
                                    </select>
                                </div>
                            )}

                            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '32px' }}>
                                <button type="button" className="btn glass-card" onClick={handleCloseModal}>Cancel</button>
                                <button
                                    type="submit"
                                    className="btn btn-primary"
                                    disabled={submitting}
                                >
                                    {submitting ? 'Saving...' : (isEditing ? 'Update Task' : 'Create Task')}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Tasks;
