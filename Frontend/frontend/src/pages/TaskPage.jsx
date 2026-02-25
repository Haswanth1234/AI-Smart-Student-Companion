import React, { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getTasks, createTask, updateTask, deleteTask } from '../services/taskService';
import { Loader2, Plus, Calendar, CheckCircle, Circle, Trash2, Bot } from 'lucide-react';

export default function TaskPage() {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [newTask, setNewTask] = useState({ title: '', due_date: '', priority: 'medium' });

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const data = await getTasks();
            setTasks(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTask = async (e) => {
        e.preventDefault();
        try {
            await createTask(newTask);
            setShowModal(false);
            setNewTask({ title: '', due_date: '', priority: 'medium' });
            fetchTasks();
        } catch (err) {
            alert("Failed to create task");
        }
    };

    const handleToggleStatus = async (task) => {
        try {
            const newStatus = task.status === 'completed' ? 'pending' : 'completed';
            await updateTask(task._id, { status: newStatus });
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Delete this task?")) return;
        try {
            await deleteTask(id);
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <DashboardLayout title="Tasks">
            <div className="flex-between" style={{ marginBottom: '2rem' }}>
                <p style={{ color: 'var(--text-secondary)' }}>Manage your academic tasks and deadlines.</p>
                <button className="neon-btn" onClick={() => setShowModal(true)} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Plus size={18} /> New Task
                </button>
            </div>

            {loading ? (
                <div className="flex-center" style={{ height: '50vh' }}><Loader2 className="spinner" /></div>
            ) : tasks.length > 0 ? (
                <div className="grid-cols-2">
                    {tasks.map(task => (
                        <div key={task._id} className="glass-card" style={{ borderLeft: `4px solid ${task.priority === 'high' ? 'var(--danger-color)' : task.priority === 'medium' ? 'var(--warning-color)' : 'var(--success-color)'}` }}>
                            <div className="flex-between mb-4">
                                <h3 className="heading-md" style={{ margin: 0, textDecoration: task.status === 'completed' ? 'line-through' : 'none', color: task.status === 'completed' ? 'var(--text-secondary)' : 'white' }}>
                                    {task.title}
                                </h3>
                                {task.is_ai_generated && <Bot size={18} color="var(--primary-color)" title="AI Generated" />}
                            </div>

                            <div className="flex-between text-secondary text-sm mb-4">
                                <div className="flex-center gap-2">
                                    <Calendar size={16} />
                                    {new Date(task.due_date).toLocaleDateString()}
                                </div>
                                <span className={`badge badge-${task.priority === 'high' ? 'danger' : task.priority === 'medium' ? 'warning' : 'success'}`}>
                                    {task.priority}
                                </span>
                            </div>

                            <div className="flex-between mt-auto pt-4" style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
                                <button onClick={() => handleToggleStatus(task)} style={{ background: 'transparent', padding: 0, color: task.status === 'completed' ? 'var(--success-color)' : 'var(--text-secondary)' }}>
                                    {task.status === 'completed' ? <CheckCircle /> : <Circle />}
                                </button>
                                <button onClick={() => handleDelete(task._id)} style={{ background: 'transparent', padding: 0, color: 'var(--danger-color)' }}>
                                    <Trash2 size={18} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="flex-center flex-col text-secondary" style={{ height: '40vh', gap: '1rem' }}>
                    <div style={{ padding: '2rem', background: 'var(--glass-bg)', borderRadius: '50%' }}>
                        <CheckCircle size={48} style={{ opacity: 0.5 }} />
                    </div>
                    <p>No pending tasks. Great job!</p>
                </div>
            )}

            {/* Simple Modal */}
            {showModal && (
                <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
                    <div className="glass-panel" style={{ padding: '2rem', width: '400px', maxWidth: '90%' }}>
                        <h3 className="heading-md">Add New Task</h3>
                        <form onSubmit={handleCreateTask} className="modern-form">
                            <div className="input-group">
                                <input placeholder="Task Title" value={newTask.title} onChange={e => setNewTask({ ...newTask, title: e.target.value })} required />
                            </div>
                            <div className="input-group">
                                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Due Date</label>
                                <input type="date" value={newTask.due_date} onChange={e => setNewTask({ ...newTask, due_date: e.target.value })} required />
                            </div>
                            <div className="input-group">
                                <select value={newTask.priority} onChange={e => setNewTask({ ...newTask, priority: e.target.value })} style={{ width: '100%', padding: '1rem', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', color: 'white', borderRadius: '8px' }}>
                                    <option value="low">Low Priority</option>
                                    <option value="medium">Medium Priority</option>
                                    <option value="high">High Priority</option>
                                </select>
                            </div>
                            <div className="flex-between" style={{ marginTop: '1rem' }}>
                                <button type="button" onClick={() => setShowModal(false)} style={{ background: 'transparent', color: 'var(--text-secondary)' }}>Cancel</button>
                                <button type="submit" className="neon-btn">Create</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}
