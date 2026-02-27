'use client';

import { useState, useEffect } from 'react';
import { listKnowledge, getKnowledge, updateKnowledge, createKnowledge, deleteKnowledge } from '../lib/api';

const CATEGORIES = [
    { key: 'frameworks', label: '📐 MBA Frameworks', icon: '📐' },
    { key: 'industries', label: '🏢 Industries', icon: '🏢' },
    { key: 'markets', label: '🌍 Markets', icon: '🌍' },
];

export default function EditorPage() {
    const [files, setFiles] = useState({});
    const [activeCategory, setActiveCategory] = useState('frameworks');
    const [activeFile, setActiveFile] = useState(null);
    const [content, setContent] = useState('');
    const [originalContent, setOriginalContent] = useState('');
    const [saving, setSaving] = useState(false);
    const [showNewModal, setShowNewModal] = useState(false);
    const [newFileName, setNewFileName] = useState('');
    const [toast, setToast] = useState(null);

    // Load files for all categories
    useEffect(() => {
        CATEGORIES.forEach(cat => {
            listKnowledge(cat.key)
                .then(data => setFiles(prev => ({ ...prev, [cat.key]: data.files })))
                .catch(err => console.error(`Failed to load ${cat.key}:`, err));
        });
    }, []);

    const loadFile = async (category, name) => {
        try {
            const data = await getKnowledge(category, name);
            setActiveCategory(category);
            setActiveFile(name);
            setContent(data.content);
            setOriginalContent(data.content);
        } catch (err) {
            showToast('Không thể đọc file: ' + err.message, 'error');
        }
    };

    const handleSave = async () => {
        if (!activeFile) return;
        setSaving(true);
        try {
            await updateKnowledge(activeCategory, activeFile, content);
            setOriginalContent(content);
            showToast(`✅ Đã lưu ${activeFile}.md`, 'success');
        } catch (err) {
            showToast('❌ Lỗi lưu: ' + err.message, 'error');
        }
        setSaving(false);
    };

    const handleCreate = async () => {
        if (!newFileName.trim()) return;
        try {
            const name = newFileName.trim().replace(/\.md$/, '').replace(/\s+/g, '_').toLowerCase();
            await createKnowledge(activeCategory, name, `# ${name}\n\nNội dung framework mới.\n`);
            showToast(`✅ Đã tạo ${name}.md`, 'success');
            setShowNewModal(false);
            setNewFileName('');
            // Reload
            const data = await listKnowledge(activeCategory);
            setFiles(prev => ({ ...prev, [activeCategory]: data.files }));
            loadFile(activeCategory, name);
        } catch (err) {
            showToast('❌ ' + err.message, 'error');
        }
    };

    const handleDelete = async () => {
        if (!activeFile || !confirm(`Xoá ${activeFile}.md?`)) return;
        try {
            await deleteKnowledge(activeCategory, activeFile);
            showToast(`🗑️ Đã xoá ${activeFile}.md`, 'success');
            setActiveFile(null);
            setContent('');
            const data = await listKnowledge(activeCategory);
            setFiles(prev => ({ ...prev, [activeCategory]: data.files }));
        } catch (err) {
            showToast('❌ ' + err.message, 'error');
        }
    };

    const showToast = (message, type) => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    const hasChanges = content !== originalContent;

    return (
        <>
            <div className="page-header">
                <div className="flex-between">
                    <div>
                        <h2 className="page-title">📚 Knowledge Editor</h2>
                        <p className="page-subtitle">Chỉnh sửa framework, industry và market knowledge files</p>
                    </div>
                    <button className="btn btn-primary btn-sm" onClick={() => setShowNewModal(true)}>
                        ➕ Tạo mới
                    </button>
                </div>
            </div>

            <div className="editor-container">
                {/* File Tree */}
                <div className="editor-sidebar">
                    {CATEGORIES.map(cat => (
                        <div key={cat.key}>
                            <div className="editor-category">{cat.label}</div>
                            {(files[cat.key] || []).map(file => (
                                <div
                                    key={file.name}
                                    className={`editor-file-item ${activeCategory === cat.key && activeFile === file.name ? 'active' : ''}`}
                                    onClick={() => loadFile(cat.key, file.name)}
                                >
                                    <span>📄</span>
                                    <span>{file.name}</span>
                                </div>
                            ))}
                            {(!files[cat.key] || files[cat.key].length === 0) && (
                                <div className="editor-file-item" style={{ opacity: 0.5, cursor: 'default' }}>
                                    <span>📭</span>
                                    <span>Trống</span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* Editor */}
                <div className="editor-main">
                    {activeFile ? (
                        <>
                            <div className="editor-toolbar">
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                    <span style={{ fontSize: '14px', fontWeight: 600 }}>
                                        {activeCategory}/{activeFile}.md
                                    </span>
                                    {hasChanges && <span className="badge badge-warning">Chưa lưu</span>}
                                </div>
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button
                                        className="btn btn-primary btn-sm"
                                        onClick={handleSave}
                                        disabled={saving || !hasChanges}
                                    >
                                        {saving ? '⏳ Saving...' : '💾 Save'}
                                    </button>
                                    <button className="btn btn-danger btn-sm" onClick={handleDelete}>
                                        🗑️ Xoá
                                    </button>
                                </div>
                            </div>
                            <div className="editor-content">
                                <textarea
                                    className="editor-textarea"
                                    value={content}
                                    onChange={e => setContent(e.target.value)}
                                    spellCheck={false}
                                />
                                <div className="editor-preview markdown-content">
                                    <SimpleMarkdown content={content} />
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="empty-state" style={{ marginTop: '100px' }}>
                            <div className="empty-state-icon">📝</div>
                            <h3 style={{ marginBottom: '8px' }}>Chọn file để chỉnh sửa</h3>
                            <p>
                                Click vào file trong danh sách bên trái để mở editor.<br />
                                Bạn có thể chỉnh sửa framework, thêm industry mới, hoặc cập nhật market data.
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {/* New File Modal */}
            {showNewModal && (
                <div className="modal-overlay" onClick={() => setShowNewModal(false)}>
                    <div className="modal" onClick={e => e.stopPropagation()}>
                        <h3 className="modal-title">➕ Tạo Knowledge File Mới</h3>
                        <div className="form-group">
                            <label className="form-label">Category</label>
                            <select className="form-select" value={activeCategory} onChange={e => setActiveCategory(e.target.value)}>
                                {CATEGORIES.map(cat => (
                                    <option key={cat.key} value={cat.key}>{cat.label}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Tên file (không cần .md)</label>
                            <input
                                className="form-input"
                                placeholder="VD: customer_journey, growth_hacking"
                                value={newFileName}
                                onChange={e => setNewFileName(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleCreate()}
                                autoFocus
                            />
                        </div>
                        <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                            <button className="btn btn-secondary" onClick={() => setShowNewModal(false)}>Huỷ</button>
                            <button className="btn btn-primary" onClick={handleCreate} disabled={!newFileName.trim()}>Tạo</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Toast */}
            {toast && (
                <div className="toast-container">
                    <div className={`toast toast-${toast.type}`}>{toast.message}</div>
                </div>
            )}
        </>
    );
}

function SimpleMarkdown({ content }) {
    const html = content
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/^- (.*$)/gm, '<li>$1</li>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        .replace(/^---$/gm, '<hr/>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br/>');
    return <div dangerouslySetInnerHTML={{ __html: `<p>${html}</p>` }} />;
}
