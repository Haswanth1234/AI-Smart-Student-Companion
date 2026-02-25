import React, { useState, useEffect } from 'react';
import {
    Settings as SettingsIcon,
    User,
    Lock,
    Shield,
    Mail,
    Briefcase,
    Save,
    AlertCircle,
    CheckCircle
} from 'lucide-react';
import { getAdminProfile, changeAdminPassword } from '../../services/adminSettingsService';

const Settings = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    // Password Change State
    const [passwords, setPasswords] = useState({
        current: '',
        new: '',
        confirm: ''
    });
    const [passLoading, setPassLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            setLoading(true);
            const data = await getAdminProfile();
            setProfile(data);
        } catch (err) {
            console.error("Failed to load profile:", err);
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordChange = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });

        if (passwords.new !== passwords.confirm) {
            setMessage({ type: 'error', text: 'New passwords do not match' });
            return;
        }

        if (passwords.new.length < 6) {
            setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
            return;
        }

        try {
            setPassLoading(true);
            await changeAdminPassword(passwords.current, passwords.new);
            setMessage({ type: 'success', text: 'Password updated successfully' });
            setPasswords({ current: '', new: '', confirm: '' });
        } catch (err) {
            setMessage({ type: 'error', text: err });
        } finally {
            setPassLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex-center" style={{ height: '400px', color: 'var(--text-secondary)' }}>
                <div className="animate-spin" style={{ marginRight: '10px' }}>⌛</div> Loading settings...
            </div>
        );
    }

    return (
        <div className="main-content fade-in">
            {/* Header */}
            <div className="mb-8">
                <h1 className="heading-lg flex-center gap-2" style={{ justifyContent: 'flex-start', marginBottom: '8px' }}>
                    <SettingsIcon size={32} color="var(--primary-color)" />
                    Settings
                </h1>
                <p className="text-secondary">
                    Manage your account settings and security preferences.
                </p>
            </div>

            <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>

                {/* Profile Card */}
                <div className="glass-card" style={{ height: 'fit-content' }}>
                    <div className="flex-center-col mb-6">
                        <div style={{
                            width: '100px', height: '100px',
                            background: 'linear-gradient(135deg, #06b6d4, #3b82f6)',
                            borderRadius: '50%',
                            marginBottom: '1rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '2.5rem',
                            fontWeight: '700',
                            color: 'white',
                            boxShadow: 'var(--shadow-glow)'
                        }}>
                            {profile?.name?.charAt(0).toUpperCase()}
                        </div>
                        <h2 className="heading-md" style={{ marginBottom: '4px' }}>
                            {profile?.name}
                        </h2>
                        <span className="badge badge-info">
                            {profile?.role?.toUpperCase()}
                        </span>
                    </div>

                    <div className="flex-col gap-4">
                        <div className="user-badge mb-0">
                            <Mail size={20} className="text-secondary" />
                            <div>
                                <div className="text-secondary text-xs">Email</div>
                                <div className="font-medium">{profile?.email}</div>
                            </div>
                        </div>

                        <div className="user-badge mb-0">
                            <Briefcase size={20} className="text-secondary" />
                            <div>
                                <div className="text-secondary text-xs">Department</div>
                                <div className="font-medium">{profile?.department}</div>
                            </div>
                        </div>

                        <div className="user-badge mb-0">
                            <Shield size={20} className="text-secondary" />
                            <div>
                                <div className="text-secondary text-xs">College</div>
                                <div className="font-medium">{profile?.college_name}</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Security / Password Card */}
                <div className="glass-card">
                    <h3 className="heading-md flex-center gap-2 mb-6" style={{ justifyContent: 'flex-start' }}>
                        <Lock size={22} color="var(--warning-color)" />
                        Security Settings
                    </h3>

                    {message.text && (
                        <div className={`badge ${message.type === 'error' ? 'badge-danger' : 'badge-success'} w-full mb-6 p-3`}>
                            {message.type === 'error' ? <AlertCircle size={18} /> : <CheckCircle size={18} />}
                            {message.text}
                        </div>
                    )}

                    <form onSubmit={handlePasswordChange} className="modern-form">
                        <div className="mb-6">
                            <label>Current Password</label>
                            <input
                                type="password"
                                value={passwords.current}
                                onChange={(e) => setPasswords({ ...passwords, current: e.target.value })}
                                placeholder="Enter current password"
                                required
                            />
                        </div>

                        <div className="grid-cols-2">
                            <div>
                                <label>New Password</label>
                                <input
                                    type="password"
                                    value={passwords.new}
                                    onChange={(e) => setPasswords({ ...passwords, new: e.target.value })}
                                    placeholder="Enter new password"
                                    required
                                />
                            </div>
                            <div>
                                <label>Confirm Password</label>
                                <input
                                    type="password"
                                    value={passwords.confirm}
                                    onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })}
                                    placeholder="Confirm new password"
                                    required
                                />
                            </div>
                        </div>

                        <div className="flex justify-end mt-4">
                            <button
                                type="submit"
                                disabled={passLoading}
                                className="neon-btn"
                            >
                                {passLoading ? (
                                    <>
                                        <div className="animate-spin" style={{ width: '16px', height: '16px', border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%' }}></div>
                                        Updating...
                                    </>
                                ) : (
                                    <>
                                        <Save size={18} />
                                        Update Password
                                    </>
                                )}
                            </button>
                        </div>
                    </form>
                </div>

            </div>
        </div>
    );
};

export default Settings;
