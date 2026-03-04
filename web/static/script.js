// Финальная версия с реальными данными
document.addEventListener('DOMContentLoaded', function() {
    console.log('Jarvis UI initialized');
    
    // Загружаем данные при загрузке
    updateStatusBar();
    loadPageData();
    
    // Обновляем статус каждые 5 секунд
    setInterval(updateStatusBar, 5000);
    
    // Командная форма
    const commandForm = document.getElementById('command-form');
    if (commandForm) {
        commandForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const command = document.getElementById('command-input').value;
            const mode = document.getElementById('mode-select').value;
            
            const output = document.getElementById('command-output');
            output.textContent = 'Executing...';
            
            try {
                const response = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command, mode})
                });
                const result = await response.json();
                output.textContent = JSON.stringify(result, null, 2);
            } catch (err) {
                output.textContent = 'Error: ' + err.message;
            }
        });
    }
});

// Загрузка данных в зависимости от страницы
function loadPageData() {
    const path = window.location.pathname;
    
    if (path === '/memory') {
        loadMemoryData();
    } else if (path === '/nodes') {
        loadNodesData();
    } else if (path === '/tasks') {
        loadTasksData();
    } else if (path === '/compiler') {
        loadCompilerData();
    } else {
        loadDashboardData();
    }
}

// Обновление статус-бара
async function updateStatusBar() {
    try {
        // Nodes count
        const nodesRes = await fetch('/api/nodes');
        const nodesData = await nodesRes.json();
        document.getElementById('node-count').textContent = 'Nodes: ' + (nodesData.count || 0);
        
        // Cache stats
        const cacheRes = await fetch('/api/cache/stats');
        const cacheData = await cacheRes.json();
        const hitRate = ((cacheData.hit_rate || 0) * 100).toFixed(1);
        document.getElementById('cache-status').textContent = 'Cache: ' + (cacheData.size || 0) + ' entries (' + hitRate + '% hits)';
        
    } catch (err) {
        console.error('Status update error:', err);
    }
}

// Загрузка данных для Dashboard
async function loadDashboardData() {
    try {
        const statsDiv = document.getElementById('system-stats');
        if (!statsDiv) return;
        
        // Получаем статус
        const statusRes = await fetch('/api/status');
        const statusData = await statusRes.json();
        
        // Получаем память
        const memoryRes = await fetch('/api/memory');
        const memoryData = await memoryRes.json();
        
        let experiencesCount = 0;
        let bestSequencesCount = 0;
        let patternsCount = 0;
        
        if (memoryData.experiences) experiencesCount = memoryData.experiences.length;
        if (memoryData.best_sequences) bestSequencesCount = Object.keys(memoryData.best_sequences).length;
        if (memoryData.patterns) patternsCount = Object.keys(memoryData.patterns).length;
        
        statsDiv.innerHTML = `
            <p><strong>Version:</strong> ${statusData.version}</p>
            <p><strong>Core:</strong> ✅ Active</p>
            <p><strong>Experiences:</strong> ${experiencesCount}</p>
            <p><strong>Best Sequences:</strong> ${bestSequencesCount}</p>
            <p><strong>Patterns:</strong> ${patternsCount}</p>
        `;
    } catch (err) {
        console.error('Dashboard load error:', err);
        document.getElementById('system-stats').innerHTML = '<p style="color:red">Error loading data: ' + err.message + '</p>';
    }
}

// Загрузка данных для Memory
async function loadMemoryData() {
    try {
        const response = await fetch('/api/memory');
        const data = await response.json();
        
        const contentDiv = document.getElementById('memory-content');
        if (contentDiv) {
            contentDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    } catch (err) {
        console.error('Memory load error:', err);
    }
}

// Загрузка данных для Nodes
async function loadNodesData() {
    try {
        const response = await fetch('/api/nodes');
        const data = await response.json();
        
        const contentDiv = document.getElementById('memory-content');
        if (contentDiv) {
            if (data.count === 0) {
                contentDiv.innerHTML = '<p>No active nodes found. Start discovery with --distributed flag.</p>';
            } else {
                contentDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
        }
    } catch (err) {
        console.error('Nodes load error:', err);
    }
}

// Загрузка данных для Tasks
async function loadTasksData() {
    try {
        const response = await fetch('/api/scheduler/tasks');
        const data = await response.json();
        
        const contentDiv = document.getElementById('memory-content');
        if (contentDiv) {
            if (!data.tasks || data.tasks.length === 0) {
                contentDiv.innerHTML = '<p>No scheduled tasks.</p>';
            } else {
                contentDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
        }
    } catch (err) {
        console.error('Tasks load error:', err);
    }
}

// Загрузка данных для Compiler
async function loadCompilerData() {
    try {
        const response = await fetch('/api/cache/stats');
        const data = await response.json();
        
        const contentDiv = document.getElementById('memory-content');
        if (contentDiv) {
            const hitRate = ((data.hit_rate || 0) * 100).toFixed(2);
            contentDiv.innerHTML = `
                <h3>Cache Statistics</h3>
                <table border="1" cellpadding="5">
                    <tr><td>Hits:</td><td>${data.hits || 0}</td></tr>
                    <tr><td>Misses:</td><td>${data.misses || 0}</td></tr>
                    <tr><td>Hit Rate:</td><td>${hitRate}%</td></tr>
                    <tr><td>Cache Size:</td><td>${data.size || 0} entries</td></tr>
                </table>
            `;
        }
    } catch (err) {
        console.error('Compiler load error:', err);
    }
}
