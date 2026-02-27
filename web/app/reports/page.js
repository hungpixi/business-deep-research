'use client';

import { useState, useEffect } from 'react';
import { listReports, getReport, deleteReport } from '../lib/api';

export default function ReportsPage() {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeReport, setActiveReport] = useState(null);
    const [content, setContent] = useState('');
    const [toast, setToast] = useState(null);

    useEffect(() => {
        loadReports();
    }, []);

    const loadReports = async () => {
        setLoading(true);
        try {
            const data = await listReports();
            setReports(data.reports || []);
        } catch (err) {
            console.error('Failed to load reports:', err);
        }
        setLoading(false);
    };

    const openReport = async (filename) => {
        try {
            const data = await getReport(filename);
            setActiveReport(filename);
            setContent(data.content);
        } catch (err) {
            showToast('❌ Không thể mở report', 'error');
        }
    };

    const handleDelete = async (filename, e) => {
        e.stopPropagation();
        if (!confirm(`Xoá report "${filename}"?`)) return;
        try {
            await deleteReport(filename);
            showToast('🗑️ Đã xoá', 'success');
            if (activeReport === filename) {
                setActiveReport(null);
                setContent('');
            }
            loadReports();
        } catch (err) {
            showToast('❌ ' + err.message, 'error');
        }
    };

    const downloadReport = (filename) => {
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    };

    const showToast = (message, type) => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    const formatDate = (iso) => {
        try {
            return new Date(iso).toLocaleString('vi-VN');
        } catch { return iso; }
    };

    const formatSize = (bytes) => {
        if (bytes < 1024) return `${bytes} B`;
        return `${(bytes / 1024).toFixed(1)} KB`;
    };

    return (
        <>
            <div className="page-header">
                <div className="flex-between">
                    <div>
                        <h2 className="page-title">📊 Reports</h2>
                        <p className="page-subtitle">{reports.length} business plan đã tạo</p>
                    </div>
                    <button className="btn btn-secondary btn-sm" onClick={loadReports}>
                        🔄 Refresh
                    </button>
                </div>
            </div>

            <div className="page-body">
                {activeReport ? (
                    /* Report Viewer */
                    <div className="fade-in">
                        <div className="flex-between" style={{ marginBottom: '16px' }}>
                            <div>
                                <button className="btn btn-secondary btn-sm" onClick={() => { setActiveReport(null); setContent(''); }}>
                                    ← Quay lại
                                </button>
                                <span style={{ marginLeft: '12px', fontWeight: 600 }}>{activeReport}</span>
                            </div>
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <button className="btn btn-primary btn-sm" onClick={() => downloadReport(activeReport)}>
                                    ⬇️ Download
                                </button>
                                <button className="btn btn-secondary btn-sm" onClick={() => navigator.clipboard.writeText(content)}>
                                    📋 Copy
                                </button>
                            </div>
                        </div>
                        <div className="card">
                            <div className="markdown-content" style={{ maxHeight: 'calc(100vh - 250px)', overflowY: 'auto' }}>
                                <ReportMarkdown content={content} />
                            </div>
                        </div>
                    </div>
                ) : (
                    /* Reports List */
                    <>
                        {loading ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="skeleton" style={{ height: '72px', borderRadius: 'var(--radius-md)' }} />
                                ))}
                            </div>
                        ) : reports.length === 0 ? (
                            <div className="card">
                                <div className="empty-state">
                                    <div className="empty-state-icon">📭</div>
                                    <h3 style={{ marginBottom: '8px' }}>Chưa có report nào</h3>
                                    <p>Vào tab Pipeline Runner để tạo business plan đầu tiên.</p>
                                </div>
                            </div>
                        ) : (
                            <div className="fade-in">
                                {reports.map(report => (
                                    <div key={report.filename} className="report-item" onClick={() => openReport(report.filename)}>
                                        <div>
                                            <div style={{ fontWeight: 600, fontSize: '14px' }}>
                                                📄 {report.title || report.filename}
                                            </div>
                                            <div className="report-meta">
                                                {report.industry && <span className="badge badge-info">{report.industry}</span>}
                                                {report.market && <span className="badge badge-info">{report.market}</span>}
                                                <span>📅 {formatDate(report.modified)}</span>
                                                <span>📏 {formatSize(report.size)}</span>
                                            </div>
                                        </div>
                                        <div style={{ display: 'flex', gap: '8px' }}>
                                            <button
                                                className="btn btn-danger btn-sm btn-icon"
                                                onClick={(e) => handleDelete(report.filename, e)}
                                                title="Xoá"
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </div>

            {toast && (
                <div className="toast-container">
                    <div className={`toast toast-${toast.type}`}>{toast.message}</div>
                </div>
            )}
        </>
    );
}

function ReportMarkdown({ content }) {
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
