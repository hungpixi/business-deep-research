'use client';

import { useState, useEffect } from 'react';
import { getSettings, updateSettings } from '../lib/api';

export default function SettingsPage() {
    const [settings, setSettings] = useState({
        api_provider: 'gemini_direct',
        gemini_api_key: '',
        antigravity_proxy_url: 'http://localhost:8045/v1',
        antigravity_api_key: '',
        model_fast: 'gemini-2.0-flash',
        model_pro: 'gemini-2.5-pro',
        tavily_api_key: '',
    });
    const [saving, setSaving] = useState(false);
    const [toast, setToast] = useState(null);
    const [editingKeys, setEditingKeys] = useState({});

    useEffect(() => {
        getSettings()
            .then(data => setSettings(prev => ({ ...prev, ...data })))
            .catch(err => console.error('Settings load failed:', err));
    }, []);

    const handleSave = async () => {
        setSaving(true);
        try {
            await updateSettings(settings);
            showToast('✅ Settings saved!', 'success');
        } catch (err) {
            showToast('❌ ' + err.message, 'error');
        }
        setSaving(false);
    };

    const showToast = (message, type) => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    const updateField = (key, value) => {
        setSettings(prev => ({ ...prev, [key]: value }));
    };

    return (
        <>
            <div className="page-header">
                <h2 className="page-title">⚙️ Cài đặt API</h2>
                <p className="page-subtitle">Cấu hình API provider — hỗ trợ Gemini trực tiếp hoặc qua Antigravity Tools proxy</p>
            </div>

            <div className="page-body" style={{ maxWidth: '700px' }}>

                {/* API Provider */}
                <div className="card fade-in" style={{ marginBottom: '16px' }}>
                    <div className="card-title">🔌 API Provider</div>

                    <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
                        <label
                            style={{
                                flex: 1, padding: '16px', borderRadius: 'var(--radius-md)',
                                border: `2px solid ${settings.api_provider === 'gemini_direct' ? 'var(--accent-primary)' : 'var(--border)'}`,
                                background: settings.api_provider === 'gemini_direct' ? 'var(--accent-glow)' : 'var(--bg-tertiary)',
                                cursor: 'pointer', transition: 'var(--transition)',
                            }}
                        >
                            <input
                                type="radio" name="provider" value="gemini_direct"
                                checked={settings.api_provider === 'gemini_direct'}
                                onChange={e => updateField('api_provider', e.target.value)}
                                style={{ display: 'none' }}
                            />
                            <div style={{ fontWeight: 600, marginBottom: '4px' }}>🔑 Gemini Direct</div>
                            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                                Kết nối trực tiếp Google Gemini API với API key
                            </div>
                        </label>

                        <label
                            style={{
                                flex: 1, padding: '16px', borderRadius: 'var(--radius-md)',
                                border: `2px solid ${settings.api_provider === 'antigravity_proxy' ? 'var(--accent-primary)' : 'var(--border)'}`,
                                background: settings.api_provider === 'antigravity_proxy' ? 'var(--accent-glow)' : 'var(--bg-tertiary)',
                                cursor: 'pointer', transition: 'var(--transition)',
                            }}
                        >
                            <input
                                type="radio" name="provider" value="antigravity_proxy"
                                checked={settings.api_provider === 'antigravity_proxy'}
                                onChange={e => updateField('api_provider', e.target.value)}
                                style={{ display: 'none' }}
                            />
                            <div style={{ fontWeight: 600, marginBottom: '4px' }}>🔀 Antigravity Tools</div>
                            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                                Kết nối qua Antigravity Tools proxy (localhost:8045)
                            </div>
                        </label>
                    </div>

                    {/* Gemini Direct Settings */}
                    {settings.api_provider === 'gemini_direct' && (
                        <div className="fade-in">
                            <div className="form-group">
                                <label className="form-label">Gemini API Key</label>
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <input
                                        className="form-input"
                                        type={editingKeys.gemini ? 'text' : 'password'}
                                        value={settings.gemini_api_key}
                                        onChange={e => updateField('gemini_api_key', e.target.value)}
                                        placeholder="AIza..."
                                    />
                                    <button
                                        className="btn btn-secondary btn-icon"
                                        onClick={() => setEditingKeys(prev => ({ ...prev, gemini: !prev.gemini }))}
                                        title={editingKeys.gemini ? 'Ẩn' : 'Hiện'}
                                    >
                                        {editingKeys.gemini ? '🙈' : '👁️'}
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Antigravity Proxy Settings */}
                    {settings.api_provider === 'antigravity_proxy' && (
                        <div className="fade-in">
                            <div className="form-group">
                                <label className="form-label">Proxy URL</label>
                                <input
                                    className="form-input"
                                    value={settings.antigravity_proxy_url}
                                    onChange={e => updateField('antigravity_proxy_url', e.target.value)}
                                    placeholder="http://localhost:8045/v1"
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">API Key (từ Antigravity Tools)</label>
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <input
                                        className="form-input"
                                        type={editingKeys.antigravity ? 'text' : 'password'}
                                        value={settings.antigravity_api_key}
                                        onChange={e => updateField('antigravity_api_key', e.target.value)}
                                        placeholder="sk-..."
                                    />
                                    <button
                                        className="btn btn-secondary btn-icon"
                                        onClick={() => setEditingKeys(prev => ({ ...prev, antigravity: !prev.antigravity }))}
                                    >
                                        {editingKeys.antigravity ? '🙈' : '👁️'}
                                    </button>
                                </div>
                            </div>
                            <div style={{
                                padding: '12px', borderRadius: 'var(--radius-md)',
                                background: 'rgba(59, 130, 246, 0.05)', border: '1px solid rgba(59, 130, 246, 0.1)',
                                fontSize: '12px', color: 'var(--text-muted)',
                            }}>
                                💡 Mở Antigravity Tools → tab "API Proxy" → copy API Key và Port
                            </div>
                        </div>
                    )}
                </div>

                {/* Model Settings */}
                <div className="card fade-in" style={{ marginBottom: '16px' }}>
                    <div className="card-title">🤖 Model Configuration</div>
                    <div className="grid-2">
                        <div className="form-group">
                            <label className="form-label">Fast Model (Search)</label>
                            <input
                                className="form-input"
                                value={settings.model_fast}
                                onChange={e => updateField('model_fast', e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Pro Model (Analysis)</label>
                            <input
                                className="form-input"
                                value={settings.model_pro}
                                onChange={e => updateField('model_pro', e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                {/* Tavily */}
                <div className="card fade-in" style={{ marginBottom: '16px' }}>
                    <div className="card-title">🔍 Search API (Optional)</div>
                    <div className="form-group">
                        <label className="form-label">Tavily API Key</label>
                        <div style={{ display: 'flex', gap: '8px' }}>
                            <input
                                className="form-input"
                                type={editingKeys.tavily ? 'text' : 'password'}
                                value={settings.tavily_api_key}
                                onChange={e => updateField('tavily_api_key', e.target.value)}
                                placeholder="tvly-..."
                            />
                            <button
                                className="btn btn-secondary btn-icon"
                                onClick={() => setEditingKeys(prev => ({ ...prev, tavily: !prev.tavily }))}
                            >
                                {editingKeys.tavily ? '🙈' : '👁️'}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Save Button */}
                <button
                    className="btn btn-primary"
                    style={{ width: '100%', justifyContent: 'center' }}
                    onClick={handleSave}
                    disabled={saving}
                >
                    {saving ? '⏳ Đang lưu...' : '💾 Lưu cài đặt'}
                </button>

                {/* About */}
                <div className="card" style={{ marginTop: '24px', opacity: 0.7 }}>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: 1.6 }}>
                        <strong>Business Deep Research</strong> by{' '}
                        <a href="https://comarai.com" target="_blank">Comarai</a>
                        <br />
                        Built with 🧠 AI tạo sản phẩm. Con người vận hành dịch vụ.
                        <br />
                        <a href="https://github.com/hungpixi" target="_blank">GitHub</a>
                        {' • '}
                        <a href="https://zalo.me/0834422439" target="_blank">Zalo</a>
                        {' • '}
                        <a href="mailto:hungphamphunguyen@gmail.com">Email</a>
                    </div>
                </div>
            </div>

            {toast && (
                <div className="toast-container">
                    <div className={`toast toast-${toast.type}`}>{toast.message}</div>
                </div>
            )}
        </>
    );
}
