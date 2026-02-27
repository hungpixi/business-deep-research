'use client';

import { useState, useEffect, useRef } from 'react';

const API = '';

const EXAMPLES = [
  "AI chatbot CSKH cho SME Việt Nam, vốn 50 triệu",
  "SaaS quản lý đơn hàng cho shop Shopee/TikTok",
  "App học tiếng Anh bằng AI cho trẻ em 6-12 tuổi",
  "Nền tảng kết nối freelancer IT với doanh nghiệp Nhật",
  "Tool AI tự động tạo content marketing cho agency",
];

const PANEL_TABS = [
  { key: 'config', icon: '🎛️', label: 'Pipeline' },
  { key: 'knowledge', icon: '📚', label: 'Knowledge' },
  { key: 'compare', icon: '⚖️', label: 'Compare' },
  { key: 'api', icon: '🔌', label: 'API' },
];

const OUTPUT_MODES = [
  { key: 'full', icon: '📋', label: 'Full Plan', desc: 'Business plan chi tiết 12 frameworks' },
  { key: 'pitch', icon: '🎤', label: 'Pitch Deck', desc: 'Outline slide deck cho investor' },
  { key: 'lean', icon: '⚡', label: 'Lean Canvas', desc: 'Tập trung MVP & đo lường nhanh' },
  { key: 'gtm', icon: '🚀', label: 'Go-to-Market', desc: 'Chiến lược ra thị trường 90 ngày' },
];

export default function ChatPage() {
  /* Chat */
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);

  /* Config */
  const [config, setConfig] = useState(null);
  const [settings, setSettings] = useState({
    industry: 'tech_startup', market: 'vietnam', budget: '50',
    target: '', constraints: '', selectedFrameworks: [], outputMode: 'full',
  });

  /* Panel */
  const [panelOpen, setPanelOpen] = useState(false);
  const [panelTab, setPanelTab] = useState('config');

  /* Knowledge */
  const [knowledgeFiles, setKnowledgeFiles] = useState({});
  const [activeKnowledge, setActiveKnowledge] = useState(null);
  const [knowledgeContent, setKnowledgeContent] = useState('');
  const [knowledgeOriginal, setKnowledgeOriginal] = useState('');
  const [knowledgeSaving, setKnowledgeSaving] = useState(false);

  /* Compare mode */
  const [compareMode, setCompareMode] = useState(false);
  const [compareIdeas, setCompareIdeas] = useState(['', '']);
  const [compareResults, setCompareResults] = useState([]);
  const [comparing, setComparing] = useState(false);

  /* API settings */
  const [apiSettings, setApiSettings] = useState({
    api_provider: 'gemini_direct', gemini_api_key: '',
    model_fast: 'gemini-2.0-flash', model_pro: 'gemini-2.5-pro', tavily_api_key: '',
  });

  /* Conversations */
  const [conversations, setConversations] = useState([]);
  const [activeConv, setActiveConv] = useState(null);
  const [toast, setToast] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/api/config`).then(r => r.json()).then(data => {
      setConfig(data);
      if (data.frameworks) setSettings(s => ({ ...s, selectedFrameworks: data.frameworks[s.industry] || [] }));
    }).catch(() => { });
    fetch(`${API}/api/settings`).then(r => r.json()).then(d => setApiSettings(p => ({ ...p, ...d }))).catch(() => { });
    const saved = localStorage.getItem('dr_conversations');
    if (saved) try { setConversations(JSON.parse(saved)); } catch { }
  }, []);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);
  useEffect(() => {
    if (config?.frameworks?.[settings.industry]) setSettings(s => ({ ...s, selectedFrameworks: config.frameworks[s.industry] }));
  }, [settings.industry, config]);

  /* Knowledge */
  const loadKnowledgeFiles = async () => {
    const results = {};
    for (const cat of ['frameworks', 'industries', 'markets']) {
      try { const d = await fetch(`${API}/api/knowledge/${cat}`).then(r => r.json()); results[cat] = d.files || []; }
      catch { results[cat] = []; }
    }
    setKnowledgeFiles(results);
  };

  const openKnowledge = async (cat, name) => {
    try {
      const d = await fetch(`${API}/api/knowledge/${cat}/${name}`).then(r => r.json());
      setActiveKnowledge({ category: cat, name }); setKnowledgeContent(d.content); setKnowledgeOriginal(d.content);
    } catch { showToast('Lỗi đọc file', 'error'); }
  };

  const saveKnowledge = async () => {
    if (!activeKnowledge) return; setKnowledgeSaving(true);
    try {
      await fetch(`${API}/api/knowledge/${activeKnowledge.category}/${activeKnowledge.name}`, {
        method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content: knowledgeContent }),
      });
      setKnowledgeOriginal(knowledgeContent); showToast(`✅ Đã lưu ${activeKnowledge.name}.md`, 'success');
    } catch (e) { showToast('❌ ' + e.message, 'error'); }
    setKnowledgeSaving(false);
  };

  /* Conversations */
  const saveConversation = (msgs) => {
    if (!msgs.length) return;
    const userMsg = msgs.find(m => m.role === 'user');
    const id = activeConv || Date.now().toString();
    const conv = { id, title: userMsg?.content?.slice(0, 50) || 'New', date: new Date().toISOString(), messages: msgs, settings: { ...settings } };
    setConversations(prev => {
      const updated = [conv, ...prev.filter(c => c.id !== id)].slice(0, 30);
      localStorage.setItem('dr_conversations', JSON.stringify(updated));
      return updated;
    });
    setActiveConv(id);
  };

  const startNewChat = () => { setMessages([]); setActiveConv(null); setCompareMode(false); setCompareResults([]); inputRef.current?.focus(); };

  /* === CORE: Run Pipeline === */
  const runPipeline = async (idea, existingMsgs = null) => {
    const userMsg = { role: 'user', content: idea, timestamp: new Date().toISOString() };
    const assistantMsg = {
      role: 'assistant', content: '', step: 0, totalSteps: 5,
      stepName: '', logs: [], streaming: true, filename: '',
      outputMode: settings.outputMode,
      frameworks: [...settings.selectedFrameworks],
      scorecard: null,
    };

    const base = existingMsgs || messages;
    const newMsgs = [...base, userMsg, assistantMsg];
    setMessages(newMsgs);
    setStreaming(true);

    try {
      const response = await fetch(`${API}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idea,
          industry: settings.industry,
          market: settings.market,
          context: {
            budget_vnd: parseInt(settings.budget || '50') * 1_000_000,
            is_bootstrap: true, needs_fundraising: false,
            target_customers: settings.target || undefined,
            constraints: settings.constraints ? settings.constraints.split(',').map(c => c.trim()) : undefined,
            selected_frameworks: settings.selectedFrameworks,
            output_mode: settings.outputMode,
          },
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split('\n\n');
        buf = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const data = JSON.parse(line.slice(6));
            setMessages(prev => {
              const upd = [...prev];
              const last = { ...upd[upd.length - 1] };
              switch (data.event) {
                case 'step':
                  last.step = data.step; last.totalSteps = data.total; last.stepName = data.name;
                  last.logs = [...(last.logs || []), { type: 'step', text: `Step ${data.step}/${data.total}: ${data.name}` }];
                  break;
                case 'log':
                  last.logs = [...(last.logs || []), { type: 'log', text: data.message }];
                  break;
                case 'result':
                  last.content = data.content; last.filename = data.filename; last.streaming = false;
                  last.scorecard = extractScorecard(data.content);
                  break;
                case 'error':
                  last.content = `❌ **Error**: ${data.message}`; last.streaming = false; break;
                case 'done':
                  last.streaming = false; break;
              }
              upd[upd.length - 1] = last;
              return upd;
            });
          } catch { }
        }
      }
    } catch (err) {
      setMessages(prev => {
        const upd = [...prev];
        const last = { ...upd[upd.length - 1] };
        last.content = `❌ **Connection Error**: ${err.message}\n\nChạy: \`python app.py\``;
        last.streaming = false;
        upd[upd.length - 1] = last;
        return upd;
      });
    }

    setStreaming(false);
    setMessages(prev => { saveConversation(prev); return prev; });
  };

  /* === Extract scorecard from result === */
  function extractScorecard(content) {
    const scores = {};
    const patterns = [
      { key: 'market', regex: /(?:thị trường|market\s*size|TAM|SAM).*?(\d+)/i, label: 'Thị trường' },
      { key: 'competition', regex: /(?:cạnh tranh|competition|competitive).*?(\d+)/i, label: 'Cạnh tranh' },
      { key: 'feasibility', regex: /(?:khả thi|feasibility|viability).*?(\d+)/i, label: 'Khả thi' },
      { key: 'investment', regex: /(?:đầu tư|investment|ROI|return).*?(\d+)/i, label: 'Đầu tư' },
    ];

    for (const p of patterns) {
      const m = content.match(p.regex);
      if (m) {
        const val = parseInt(m[1]);
        if (val >= 1 && val <= 10) scores[p.key] = { score: val, label: p.label };
      }
    }

    // Fallback — generate estimated scores from content signals
    if (Object.keys(scores).length < 3) {
      const hasFinancial = /ROI|IRR|NPV|dòng tiền|cash flow/i.test(content);
      const hasCompetitor = /đối thủ|competitor|cạnh tranh/i.test(content);
      const hasRisk = /rủi ro|risk|thách thức/i.test(content);
      const hasOpportunity = /cơ hội|opportunity|tiềm năng/i.test(content);
      const hasMoat = /moat|lợi thế|barrier/i.test(content);

      return {
        market: { score: hasOpportunity ? 7 : 5, label: 'Thị trường' },
        competition: { score: hasCompetitor ? (hasMoat ? 7 : 5) : 6, label: 'Cạnh tranh' },
        feasibility: { score: hasFinancial ? 7 : 5, label: 'Khả thi' },
        risk: { score: hasRisk ? 5 : 7, label: 'Rủi ro' },
        overall: { score: Math.round((hasOpportunity ? 7 : 5) * 0.3 + (hasMoat ? 7 : 5) * 0.2 + (hasFinancial ? 7 : 5) * 0.3 + (hasRisk ? 6 : 7) * 0.2), label: 'Tổng' },
      };
    }

    return scores;
  }

  const handleSend = async (text) => {
    const idea = text || input.trim();
    if (!idea || streaming) return;
    setInput('');
    await runPipeline(idea);
  };

  /* === Compare Mode === */
  const runComparison = async () => {
    const validIdeas = compareIdeas.filter(i => i.trim());
    if (validIdeas.length < 2 || comparing) return;
    setComparing(true);
    setCompareResults([]);

    const results = [];
    for (const idea of validIdeas) {
      try {
        const response = await fetch(`${API}/api/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            idea, industry: settings.industry, market: settings.market,
            context: {
              budget_vnd: parseInt(settings.budget || '50') * 1_000_000,
              is_bootstrap: true, selected_frameworks: settings.selectedFrameworks.slice(0, 4),
              output_mode: 'lean',
            },
          }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buf = '', content = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          const lines = buf.split('\n\n');
          buf = lines.pop();
          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            try {
              const data = JSON.parse(line.slice(6));
              if (data.event === 'result') content = data.content;
            } catch { }
          }
        }

        results.push({ idea, content, scorecard: extractScorecard(content) });
        setCompareResults([...results]);
      } catch (err) {
        results.push({ idea, content: `❌ Error: ${err.message}`, scorecard: null });
        setCompareResults([...results]);
      }
    }

    setComparing(false);
  };

  /* === Quick Actions === */
  const quickRefine = async (action) => {
    const lastResult = messages.filter(m => m.role === 'assistant' && m.content && !m.streaming).pop();
    if (!lastResult) return;
    const prompts = {
      pitch: `Dựa trên phân tích trước, tạo outline Pitch Deck (SequoiaFormat): Problem → Solution → Market → Product → Traction → Team → Ask. Ngắn gọn, mỗi slide 3-5 bullet points.`,
      risks: `Dựa trên phân tích trước, đào sâu vào 5 rủi ro lớn nhất và đề xuất mitigation strategy cụ thể cho từng rủi ro. Thực tế, không nói chung chung.`,
      gtm: `Dựa trên phân tích trước, tạo Go-to-Market plan 90 ngày: Week 1-2 (Setup), Week 3-4 (Launch), Month 2 (Grow), Month 3 (Scale). Với budget ${settings.budget} triệu VND.`,
      competitors: `Dựa trên phân tích trước, so sánh chi tiết với 3-5 đối thủ cạnh tranh trực tiếp tại ${config?.markets?.[settings.market] || 'Vietnam'}. Bảng so sánh: Tính năng, Giá, Điểm mạnh/yếu, Market share.`,
      financial: `Dựa trên phân tích trước, tạo bảng tài chính chi tiết 12 tháng: Revenue projection, Cost breakdown, Break-even analysis, Unit economics. Với vốn ${settings.budget} triệu VND.`,
    };
    await runPipeline(prompts[action] || prompts.pitch);
  };

  const handleKeyDown = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } };
  const showToast = (msg, type) => { setToast({ msg, type }); setTimeout(() => setToast(null), 3000); };
  const toggleFramework = (fw) => {
    setSettings(s => ({
      ...s, selectedFrameworks: s.selectedFrameworks.includes(fw) ? s.selectedFrameworks.filter(f => f !== fw) : [...s.selectedFrameworks, fw],
    }));
  };
  const saveApiSettings = async () => {
    try {
      await fetch(`${API}/api/settings`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(apiSettings) });
      showToast('✅ Saved', 'success');
    } catch (e) { showToast('❌ ' + e.message, 'error'); }
  };

  return (
    <div className="app">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <div className="sidebar-icon">🧠</div>
            <h1>Deep Research</h1>
          </div>
          <button className="new-chat-btn" onClick={startNewChat} title="New Chat">+</button>
        </div>

        {/* Output Mode Selector */}
        <div className="output-modes">
          {OUTPUT_MODES.map(mode => (
            <button key={mode.key}
              className={`output-mode-btn ${settings.outputMode === mode.key ? 'active' : ''}`}
              onClick={() => setSettings(s => ({ ...s, outputMode: mode.key }))}
              title={mode.desc}>
              {mode.icon} {mode.label}
            </button>
          ))}
        </div>

        <div className="chat-history">
          {conversations.length > 0 && (
            <>
              <div className="history-date">Gần đây</div>
              {conversations.map(conv => (
                <div key={conv.id} className={`history-item ${activeConv === conv.id ? 'active' : ''}`}
                  onClick={() => { setMessages(conv.messages); setActiveConv(conv.id); }}>
                  💬 {conv.title}
                </div>
              ))}
            </>
          )}
        </div>

        <div className="sidebar-footer">
          <button className="sidebar-link" onClick={() => { setPanelOpen(true); setPanelTab('config'); }}>🎛️ Tinh chỉnh AI</button>
          <button className="sidebar-link" onClick={() => { setPanelOpen(true); setPanelTab('knowledge'); loadKnowledgeFiles(); }}>📚 Knowledge Base</button>
          <button className="sidebar-link" onClick={() => { setPanelOpen(true); setPanelTab('compare'); }}>⚖️ So sánh Ideas</button>
          <button className="sidebar-link" onClick={() => { setPanelOpen(true); setPanelTab('api'); }}>🔌 API Config</button>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', padding: '6px 10px', fontStyle: 'italic', lineHeight: 1.4 }}>
            "<span style={{ color: 'var(--accent)' }}>AI</span> tạo sản phẩm.
            <span style={{ color: 'var(--success)' }}> Con người</span> vận hành dịch vụ."
          </div>
        </div>
      </aside>

      {/* MAIN CHAT */}
      <main className="chat-main">
        <div className="messages-container">
          <div className="messages-inner">
            {messages.length === 0 ? (
              /* Welcome */
              <div className="welcome">
                <div className="welcome-icon">🧠</div>
                <h2>Business Deep Research</h2>
                <p>AI agent tạo kế hoạch kinh doanh chi tiết — {settings.selectedFrameworks.length} MBA frameworks + real-time Google Search.</p>

                {/* Moat badges */}
                <div className="moat-badges">
                  <span className="moat-badge">🔍 Real-time Search</span>
                  <span className="moat-badge">📐 {settings.selectedFrameworks.length} Frameworks</span>
                  <span className="moat-badge">📊 Auto Scorecard</span>
                  <span className="moat-badge">⚖️ Compare Mode</span>
                  <span className="moat-badge">🎤 Pitch Generator</span>
                </div>

                <div className="config-summary">
                  <span className="config-tag">{config?.industries?.[settings.industry]}</span>
                  <span className="config-tag">{config?.markets?.[settings.market]}</span>
                  <span className="config-tag">{settings.budget}tr VND</span>
                  <span className="config-tag active">{OUTPUT_MODES.find(m => m.key === settings.outputMode)?.icon} {OUTPUT_MODES.find(m => m.key === settings.outputMode)?.label}</span>
                  <button className="config-edit-btn" onClick={() => { setPanelOpen(true); setPanelTab('config'); }}>🎛️ Tinh chỉnh</button>
                </div>

                <div className="welcome-chips">
                  {EXAMPLES.map((ex, i) => (
                    <button key={i} className="chip" onClick={() => handleSend(ex)}>{ex}</button>
                  ))}
                </div>
              </div>
            ) : (
              /* Messages */
              messages.map((msg, i) => (
                <div key={i} className="message">
                  <div className="message-header">
                    <div className={`message-avatar ${msg.role}`}>{msg.role === 'user' ? '👤' : '🧠'}</div>
                    <span className="message-name">{msg.role === 'user' ? 'Bạn' : 'Deep Research Agent'}</span>
                    {msg.role === 'assistant' && msg.outputMode && (
                      <span className="mode-badge">{OUTPUT_MODES.find(m => m.key === msg.outputMode)?.icon} {OUTPUT_MODES.find(m => m.key === msg.outputMode)?.label}</span>
                    )}
                  </div>
                  <div className="message-body">
                    {msg.role === 'assistant' && msg.streaming && !msg.content ? (
                      <div className="step-progress">
                        <div className="step-progress-header">
                          ⚡ {msg.stepName || 'Khởi tạo pipeline...'} {msg.step > 0 && `(${msg.step}/${msg.totalSteps})`}
                        </div>
                        <div className="step-bar">
                          <div className="step-bar-fill" style={{ width: `${((msg.step || 0) / (msg.totalSteps || 5)) * 100}%` }} />
                        </div>
                        <div className="step-framework-tags">
                          {(msg.frameworks || settings.selectedFrameworks).slice(0, 6).map(fw => (
                            <span key={fw} className="framework-mini-tag">{fw}</span>
                          ))}
                        </div>
                        {msg.logs?.length > 0 && (
                          <div className="step-logs">
                            {msg.logs.slice(-8).map((log, j) => (
                              <div key={j} className={`log-${log.type}`}>{log.text}</div>
                            ))}
                          </div>
                        )}
                        <span className="streaming-dot" />
                      </div>
                    ) : (
                      <>
                        {/* Scorecard */}
                        {msg.role === 'assistant' && msg.scorecard && !msg.streaming && (
                          <div className="scorecard">
                            <div className="scorecard-title">📊 Startup Scorecard</div>
                            <div className="scorecard-grid">
                              {Object.entries(msg.scorecard).map(([key, item]) => (
                                <div key={key} className="score-item">
                                  <div className="score-label">{item.label}</div>
                                  <div className="score-bar-bg">
                                    <div className="score-bar-fill" style={{ width: `${item.score * 10}%`, background: item.score >= 7 ? 'var(--success)' : item.score >= 4 ? 'var(--warning)' : 'var(--error)' }} />
                                  </div>
                                  <div className="score-value">{item.score}/10</div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        <MarkdownContent text={msg.content} />

                        {/* Quick Actions */}
                        {msg.role === 'assistant' && msg.content && !msg.streaming && (
                          <div className="quick-actions">
                            <div className="quick-actions-label">🚀 Deep Dive:</div>
                            <div className="quick-actions-grid">
                              <button className="quick-btn" onClick={() => quickRefine('pitch')} disabled={streaming}>🎤 Pitch Deck</button>
                              <button className="quick-btn" onClick={() => quickRefine('gtm')} disabled={streaming}>📅 Go-to-Market 90d</button>
                              <button className="quick-btn" onClick={() => quickRefine('financial')} disabled={streaming}>💰 Tài chính chi tiết</button>
                              <button className="quick-btn" onClick={() => quickRefine('competitors')} disabled={streaming}>🎯 Phân tích đối thủ</button>
                              <button className="quick-btn" onClick={() => quickRefine('risks')} disabled={streaming}>⚠️ Rủi ro & Giải pháp</button>
                            </div>
                            <div className="result-actions" style={{ marginTop: '8px' }}>
                              <button className="action-btn" onClick={() => {
                                const blob = new Blob([msg.content], { type: 'text/markdown' });
                                const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
                                a.download = msg.filename || 'business_plan.md'; a.click();
                              }}>⬇️ Download</button>
                              <button className="action-btn" onClick={() => navigator.clipboard.writeText(msg.content)}>📋 Copy</button>
                            </div>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="input-area">
          <div className="input-container">
            <textarea ref={inputRef} className="input-box" placeholder="Mô tả ý tưởng startup..."
              value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown}
              rows={1} disabled={streaming} />
            <button className="send-btn" onClick={() => handleSend()} disabled={streaming || !input.trim()}>➤</button>
          </div>
          <div className="input-hint">
            {config?.industries?.[settings.industry]} • {config?.markets?.[settings.market]} • {settings.budget}tr •
            {OUTPUT_MODES.find(m => m.key === settings.outputMode)?.icon} •
            <button className="hint-link" onClick={() => { setPanelOpen(true); setPanelTab('config'); }}>
              {settings.selectedFrameworks.length} frameworks ✏️
            </button>
          </div>
        </div>
      </main>

      {/* RIGHT PANEL */}
      {panelOpen && (
        <>
          <div className="panel-overlay" onClick={() => setPanelOpen(false)} />
          <div className="panel">
            <div className="panel-header">
              <div className="panel-tabs">
                {PANEL_TABS.map(tab => (
                  <button key={tab.key} className={`panel-tab ${panelTab === tab.key ? 'active' : ''}`}
                    onClick={() => { setPanelTab(tab.key); if (tab.key === 'knowledge') loadKnowledgeFiles(); }}>
                    {tab.icon} {tab.label}
                  </button>
                ))}
              </div>
              <button className="panel-close" onClick={() => setPanelOpen(false)}>✕</button>
            </div>

            <div className="panel-body">
              {/* Pipeline Config */}
              {panelTab === 'config' && (
                <div className="fade-in">
                  <div className="panel-section">
                    <div className="panel-label">Output Format</div>
                    <div className="output-format-grid">
                      {OUTPUT_MODES.map(mode => (
                        <button key={mode.key}
                          className={`output-format-btn ${settings.outputMode === mode.key ? 'active' : ''}`}
                          onClick={() => setSettings(s => ({ ...s, outputMode: mode.key }))}>
                          <span style={{ fontSize: '16px' }}>{mode.icon}</span>
                          <span style={{ fontWeight: 500 }}>{mode.label}</span>
                          <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>{mode.desc}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="panel-row">
                    <div className="panel-section">
                      <div className="panel-label">Ngành</div>
                      <select className="panel-select" value={settings.industry}
                        onChange={e => setSettings(s => ({ ...s, industry: e.target.value }))}>
                        {config?.industries && Object.entries(config.industries).map(([k, v]) => (
                          <option key={k} value={k}>{v}</option>
                        ))}
                      </select>
                    </div>
                    <div className="panel-section">
                      <div className="panel-label">Thị trường</div>
                      <select className="panel-select" value={settings.market}
                        onChange={e => setSettings(s => ({ ...s, market: e.target.value }))}>
                        {config?.markets && Object.entries(config.markets).map(([k, v]) => (
                          <option key={k} value={k}>{v}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="panel-row">
                    <div className="panel-section">
                      <div className="panel-label">Vốn (tr VND)</div>
                      <input className="panel-input" type="number" value={settings.budget}
                        onChange={e => setSettings(s => ({ ...s, budget: e.target.value }))} />
                    </div>
                    <div className="panel-section">
                      <div className="panel-label">Khách hàng</div>
                      <input className="panel-input" placeholder="SME, GenZ..." value={settings.target}
                        onChange={e => setSettings(s => ({ ...s, target: e.target.value }))} />
                    </div>
                  </div>

                  <div className="panel-section">
                    <div className="panel-label" style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>Frameworks ({settings.selectedFrameworks.length})</span>
                      <button className="mini-btn" onClick={() => {
                        const all = config?.frameworks?.[settings.industry] || [];
                        setSettings(s => ({ ...s, selectedFrameworks: s.selectedFrameworks.length === all.length ? [] : [...all] }));
                      }}>{settings.selectedFrameworks.length === (config?.frameworks?.[settings.industry]?.length || 0) ? 'Bỏ' : 'All'}</button>
                    </div>
                    <div className="framework-grid">
                      {config?.frameworks?.[settings.industry]?.map(fw => (
                        <button key={fw} className={`framework-chip ${settings.selectedFrameworks.includes(fw) ? 'active' : ''}`}
                          onClick={() => toggleFramework(fw)}>
                          {settings.selectedFrameworks.includes(fw) ? '✓' : '○'} {fw}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Knowledge */}
              {panelTab === 'knowledge' && (
                <div className="fade-in">
                  {activeKnowledge ? (
                    <>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                        <button className="mini-btn" onClick={() => setActiveKnowledge(null)}>← Back</button>
                        <button className="save-btn" style={{ width: 'auto', padding: '6px 14px' }}
                          onClick={saveKnowledge} disabled={knowledgeSaving || knowledgeContent === knowledgeOriginal}>
                          {knowledgeSaving ? '⏳' : '💾'} Save
                        </button>
                      </div>
                      <div className="panel-label">{activeKnowledge.category}/{activeKnowledge.name}.md</div>
                      <textarea className="knowledge-editor" value={knowledgeContent}
                        onChange={e => setKnowledgeContent(e.target.value)} spellCheck={false} />
                    </>
                  ) : (
                    ['frameworks', 'industries', 'markets'].map(cat => (
                      <div key={cat} className="panel-section">
                        <div className="panel-label">{cat === 'frameworks' ? '📐 Frameworks' : cat === 'industries' ? '🏢 Industries' : '🌍 Markets'}</div>
                        {(knowledgeFiles[cat] || []).map(f => (
                          <div key={f.name} className="knowledge-file" onClick={() => openKnowledge(cat, f.name)}>
                            <span>📄 {f.name}</span>
                            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{(f.size / 1024).toFixed(1)}KB</span>
                          </div>
                        ))}
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Compare Mode */}
              {panelTab === 'compare' && (
                <div className="fade-in">
                  <div className="panel-info" style={{ marginBottom: '16px' }}>
                    ⚖️ So sánh 2 ý tưởng song song — cùng thị trường, cùng frameworks. ChatGPT không làm được điều này.
                  </div>
                  {compareIdeas.map((idea, i) => (
                    <div key={i} className="panel-section">
                      <div className="panel-label">Ý tưởng {i + 1}</div>
                      <textarea className="panel-input" style={{ minHeight: '60px', resize: 'vertical' }}
                        placeholder={`VD: ${EXAMPLES[i]}`} value={idea}
                        onChange={e => { const arr = [...compareIdeas]; arr[i] = e.target.value; setCompareIdeas(arr); }} />
                    </div>
                  ))}

                  <button className="save-btn" onClick={runComparison}
                    disabled={comparing || compareIdeas.filter(i => i.trim()).length < 2}>
                    {comparing ? '⏳ Đang so sánh...' : '⚖️ So sánh ngay'}
                  </button>

                  {compareResults.length > 0 && (
                    <div style={{ marginTop: '16px' }}>
                      <div className="panel-label">Kết quả</div>
                      {compareResults.map((r, i) => (
                        <div key={i} className="compare-result">
                          <div style={{ fontWeight: 600, fontSize: '13px', marginBottom: '6px' }}>
                            {i === 0 ? '🅰️' : '🅱️'} {r.idea.slice(0, 40)}...
                          </div>
                          {r.scorecard && (
                            <div className="scorecard-mini">
                              {Object.entries(r.scorecard).map(([k, v]) => (
                                <div key={k} className="score-mini">
                                  <span>{v.label}</span>
                                  <span style={{ color: v.score >= 7 ? 'var(--success)' : v.score >= 4 ? 'var(--warning)' : 'var(--error)', fontWeight: 600 }}>
                                    {v.score}/10
                                  </span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* API */}
              {panelTab === 'api' && (
                <div className="fade-in">
                  <div className="panel-section">
                    <div className="panel-label">Provider</div>
                    <div className="provider-toggle">
                      <button className={`provider-btn ${apiSettings.api_provider === 'gemini_direct' ? 'active' : ''}`}
                        onClick={() => setApiSettings(s => ({ ...s, api_provider: 'gemini_direct' }))}>🔑 Gemini</button>
                      <button className={`provider-btn ${apiSettings.api_provider === 'antigravity_proxy' ? 'active' : ''}`}
                        onClick={() => setApiSettings(s => ({ ...s, api_provider: 'antigravity_proxy' }))}>🔀 Antigravity</button>
                    </div>
                  </div>
                  <div className="panel-section">
                    <div className="panel-label">Gemini API Key</div>
                    <input className="panel-input" type="password" value={apiSettings.gemini_api_key}
                      onChange={e => setApiSettings(s => ({ ...s, gemini_api_key: e.target.value }))} />
                  </div>
                  <div className="panel-row">
                    <div className="panel-section">
                      <div className="panel-label">Fast Model</div>
                      <input className="panel-input" value={apiSettings.model_fast}
                        onChange={e => setApiSettings(s => ({ ...s, model_fast: e.target.value }))} />
                    </div>
                    <div className="panel-section">
                      <div className="panel-label">Pro Model</div>
                      <input className="panel-input" value={apiSettings.model_pro}
                        onChange={e => setApiSettings(s => ({ ...s, model_pro: e.target.value }))} />
                    </div>
                  </div>
                  <div className="panel-section">
                    <div className="panel-label">Tavily Key</div>
                    <input className="panel-input" type="password" value={apiSettings.tavily_api_key}
                      onChange={e => setApiSettings(s => ({ ...s, tavily_api_key: e.target.value }))} />
                  </div>
                  <button className="save-btn" onClick={saveApiSettings}>💾 Lưu</button>
                  <div className="panel-info" style={{ marginTop: '12px' }}>
                    🔗 <a href="https://comarai.com" target="_blank" style={{ color: 'var(--accent)' }}>Comarai</a> •
                    <a href="https://github.com/hungpixi" target="_blank" style={{ color: 'var(--text-muted)', marginLeft: '6px' }}>GitHub</a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {toast && <div className={`toast toast-${toast.type}`}>{toast.msg}</div>}
    </div>
  );
}

function MarkdownContent({ text }) {
  if (!text) return null;
  const html = text
    .replace(/^#### (.*$)/gm, '<h4>$1</h4>').replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>').replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^\|(.+)\|$/gm, m => { const c = m.split('|').filter(x => x.trim()); if (c.every(x => /^[\s:-]+$/.test(x))) return ''; return '<tr>' + c.map(x => `<td>${x.trim()}</td>`).join('') + '</tr>'; })
    .replace(/^- (.*$)/gm, '<li>$1</li>').replace(/^(\d+)\. (.*$)/gm, '<li>$2</li>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
    .replace(/^---$/gm, '<hr/>').replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br/>');
  return <div dangerouslySetInnerHTML={{ __html: `<p>${html}</p>` }} />;
}
