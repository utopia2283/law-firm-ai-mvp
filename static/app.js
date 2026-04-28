// ==================== State ====================
let currentTab = 'chat';
let currentAdminTab = 'files';
let chatHistory = [];

// ==================== Tab Navigation ====================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        switchTab(tab);
    });
});

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(`${tab}-view`).classList.add('active');
    
    if (tab === 'dashboard') loadDashboard();
}

// ==================== Admin Tab Navigation ====================
document.querySelectorAll('.admin-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.adminTab;
        switchAdminTab(tab);
    });
});

function switchAdminTab(tab) {
    currentAdminTab = tab;
    document.querySelectorAll('.admin-tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-admin-tab="${tab}"]`).classList.add('active');
    document.querySelectorAll('.admin-panel').forEach(p => p.classList.remove('active'));
    document.getElementById(`admin-${tab}`).classList.add('active');
}

// ==================== Chat Functions ====================
function handleKeyPress(e) {
    if (e.key === 'Enter') sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    addMessage('user', message);
    input.value = '';
    
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        addMessage('bot', data.content);
    } catch (err) {
        addMessage('bot', '抱歉，系統暫時無法回應。請稍後再試。');
    }
}

function addMessage(role, content) {
    const container = document.getElementById('chat-messages');
    const isBot = role === 'bot';
    
    const msg = document.createElement('div');
    msg.className = `message ${role}`;
    msg.innerHTML = `
        <div class="message-avatar">${isBot ? '🤖' : '👤'}</div>
        <div class="message-content">
            <p>${content.replace(/\n/g, '<br>').replace(/•/g, '<li style="margin-left:20px">').replace(/<li>/g, '<ul><li>').replace(/<\/li>/g, '</li></ul>')}</p>
        </div>
        <div class="message-time">${new Date().toLocaleTimeString('zh-HK', { hour: '2-digit', minute: '2-digit' })}</div>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function sendQuickMessage(msg) {
    document.getElementById('chat-input').value = msg;
    sendMessage();
}

// ==================== Dashboard Functions ====================
async function loadDashboard() {
    try {
        const res = await fetch('/api/dashboard');
        const data = await res.json();
        
        // Update metrics
        document.getElementById('metric-queries').textContent = data.metrics.total_queries.toLocaleString();
        document.getElementById('metric-docs').textContent = data.metrics.documents_generated;
        document.getElementById('metric-kb').textContent = data.metrics.knowledge_base_hits.toLocaleString();
        document.getElementById('metric-cases').textContent = data.metrics.cases_processed;
        
        // Build bar chart
        const chart = document.getElementById('weekly-chart');
        chart.innerHTML = '';
        const maxQueries = Math.max(...data.weekly_stats.map(s => s.queries));
        data.weekly_stats.forEach(stat => {
            const height = (stat.queries / maxQueries) * 150;
            chart.innerHTML += `
                <div class="bar-item">
                    <div class="bar-value">${stat.queries}</div>
                    <div class="bar" style="height:${height}px"></div>
                    <div class="bar-label">${stat.day}</div>
                </div>
            `;
        });
        
        // Build activity list
        const list = document.getElementById('activity-list');
        list.innerHTML = '';
        data.recent_activity.forEach(act => {
            list.innerHTML += `
                <div class="activity-item">
                    <span class="activity-action">${act.action}</span>
                    <span class="activity-user">${act.user}</span>
                    <span class="activity-time">${act.time}</span>
                </div>
            `;
        });
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

// ==================== Admin Functions ====================
async function loadFiles() {
    try {
        const res = await fetch('/api/files');
        const data = await res.json();
        const tbody = document.getElementById('files-table-body');
        tbody.innerHTML = '';
        data.files.forEach((file, i) => {
            tbody.innerHTML += `
                <tr>
                    <td>${file.name}</td>
                    <td>${file.size}</td>
                    <td>${file.date}</td>
                    <td>${file.type.toUpperCase()}</td>
                    <td><button class="action-link" onclick="deleteFile(${i})">刪除</button></td>
                </tr>
            `;
        });
    } catch (err) {
        console.error('Files load error:', err);
    }
}

async function loadUsers() {
    // Default users for demo
    const users = [
        { name: '陳律師', role: '資深律師', permission: 'admin' },
        { name: '李助理', role: '法律助理', permission: 'user' },
        { name: '王書記', role: '書記員', permission: 'readonly' },
    ];
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = '';
    users.forEach((user, i) => {
        tbody.innerHTML += `
            <tr>
                <td>${user.name}</td>
                <td>${user.role}</td>
                <td><span class="permission-badge ${user.permission}">${user.permission}</span></td>
                <td><button class="action-link">編輯</button></td>
            </tr>
        `;
    });
}

// ==================== File Upload ====================
document.getElementById('file-input')?.addEventListener('change', handleFileUpload);
document.getElementById('admin-file-input')?.addEventListener('change', handleFileUpload);

function handleFileUpload(e) {
    const files = e.target.files;
    const container = document.getElementById('uploaded-files');
    Array.from(files).forEach(file => {
        const div = document.createElement('div');
        div.className = 'uploaded-file';
        div.innerHTML = `<span>📄</span><span>${file.name}</span>`;
        container.appendChild(div);
    });
    e.target.value = '';
}

// ==================== Init ====================
document.addEventListener('DOMContentLoaded', () => {
    loadFiles();
    loadUsers();
    
    // Add permission badge styles
    const style = document.createElement('style');
    style.textContent = `
        .permission-badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
        .permission-badge.admin { background: var(--gold); color: var(--bg-primary); }
        .permission-badge.user { background: #4ade80; color: #000; }
        .permission-badge.readonly { background: var(--text-muted); color: #fff; }
        .action-link { background: none; border: none; color: var(--gold); cursor: pointer; font-size: 14px; }
        .action-link:hover { text-decoration: underline; }
    `;
    document.head.appendChild(style);
});
