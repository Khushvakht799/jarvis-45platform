// Global state
let systemLog = [];
let refreshInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateStatusBar();
    loadPageData();
    
    // Start periodic updates
    refreshInterval = setInterval(updateStatusBar, 5000);
    
    // Command form handler
    const commandForm = document.getElementById('command-form');
    if (commandForm) {
        commandForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const command = document.getElementById('command-input').value;
            const mode = document.getElementById('mode-select').value;
            await executeCommand(command, mode);
        });
    }
    
    // Task form handler
    const taskForm = document.getElementById('task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const command = document.getElementById('task-command').value;
            const type = document.getElementById('task-type').value;
            const interval = document.getElementById('task-interval').value;
            await scheduleTask(command, type, interval);
        });
    }
    
    // Compile form handler
    const compileForm = document.getElementById('compile-form');
    if (compileForm) {
        compileForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const command = document.getElementById('compile-command').value;
            await compileCommand(command);
        });
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});

// Load data based on current page
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

// Update status bar
async function updateStatusBar() {
    try {
        // Nodes count
        const nodesRes = await fetch('/api/nodes');
        const nodesData = await nodesRes.json();
        document.getElementById('node-count').textContent = Nodes: ${nodesData.count};
        
        // Cache stats
        const cacheRes = await fetch('/api/cache/stats');
        const cacheData = await cacheRes.json();
        document.getElementById('cache-status').textContent = Cache: ${cacheData.size || 0} entries (${(cacheData.hit_rate * 100 || 0).toFixed(1)}% hits);
        
        // Distributed stats
        const distRes = await fetch('/api/distributed/stats');
        const distData = await distRes.json();
        document.getElementById('distributed-status').textContent = Distributed: ${distData.running ? 'Active' : 'Inactive'};
    } catch (err) {
        console.error('Status update error:', err);
    }
}

// Execute command
async function executeCommand(command, mode) {
    const outputDiv = document.getElementById('command-output');
    outputDiv.textContent = 'Executing...';
    
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command, mode})
        });
        const result = await response.json();
        outputDiv.textContent = JSON.stringify(result, null, 2);
        addLogEntry(Executed: ${command} (${mode}));
    } catch (err) {
        outputDiv.textContent = Error: ${err.message};
    }
}

// Schedule task
async function scheduleTask(command, type, interval) {
    alert('Task scheduling coming soon!');
}

// Compile command
async function compileCommand(command) {
    alert('Compiler coming soon!');
}

// Load memory data
async function loadMemoryData() {
    try {
        const response = await fetch('/api/memory');
        const data = await response.json();
        
        // Update stats
        const statsDiv = document.getElementById('memory-stats');
        statsDiv.innerHTML = 
            <p>Total experiences: ${data.experiences?.length || 0}</p>
            <p>Best sequences: ${Object.keys(data.best_sequences || {}).length}</p>
            <p>Patterns: ${Object.keys(data.patterns || {}).length}</p>
        ;
        
        // Update table
        const tbody = document.getElementById('memory-body');
        if (tbody) {
            tbody.innerHTML = '';
            const experiences = data.experiences || [];
            experiences.slice(-10).reverse().forEach(exp => {
                const row = tbody.insertRow();
                row.innerHTML = 
                    <td>${new Date(exp.timestamp).toLocaleString()}</td>
                    <td>${exp.command || ''}</td>
                    <td>${exp.avgr?.intent?.type || ''}</td>
                    <td>${exp.syvgr?.symptom?.status || ''}</td>
                    <td>${exp.syvgr?.symptom?.deviation || 0}</td>
                    <td><button onclick="viewExperience('${exp.timestamp}')">View</button></td>
                ;
            });
        }
        
        // Update best sequences
        const bestDiv = document.getElementById('best-sequences');
        if (bestDiv) {
            bestDiv.innerHTML = '<pre>' + JSON.stringify(data.best_sequences || {}, null, 2) + '</pre>';
        }
    } catch (err) {
        console.error('Memory load error:', err);
    }
}

// Load nodes data
async function loadNodesData() {
    try {
        const response = await fetch('/api/nodes');
        const data = await response.json();
        
        const tbody = document.getElementById('nodes-body');
        if (tbody) {
            tbody.innerHTML = '';
            Object.entries(data.nodes || {}).forEach(([nodeId, info]) => {
                const row = tbody.insertRow();
                const lastSeen = new Date(info.last_seen * 1000).toLocaleString();
                row.innerHTML = 
                    <td>${nodeId}</td>
                    <td>${info.address}</td>
                    <td>${lastSeen}</td>
                    <td>${Object.keys(info.capabilities || {}).join(', ')}</td>
                    <td>0</td>
                ;
            });
        }
        
        // Load distributed stats
        const distRes = await fetch('/api/distributed/stats');
        const distData = await distRes.json();
        document.getElementById('distributed-stats').innerHTML = 
            <p>Node ID: ${distData.node_id}</p>
            <p>Status: ${distData.running ? 'Running' : 'Stopped'}</p>
            <p>Active tasks: ${Object.keys(distData.node_tasks || {}).length}</p>
        ;
    } catch (err) {
        console.error('Nodes load error:', err);
    }
}

// Load tasks data
async function loadTasksData() {
    try {
        const response = await fetch('/api/scheduler/tasks');
        const data = await response.json();
        
        const tbody = document.getElementById('tasks-body');
        if (tbody) {
            tbody.innerHTML = '';
            (data.tasks || []).forEach(task => {
                const row = tbody.insertRow();
                const nextRun = new Date(task.time * 1000).toLocaleString();
                row.innerHTML = 
                    <td>${task.id}</td>
                    <td>${task.command}</td>
                    <td>${nextRun}</td>
                    <td>recurring</td>
                    <td><button onclick="cancelTask('${task.id}')">Cancel</button></td>
                ;
            });
        }
    } catch (err) {
        console.error('Tasks load error:', err);
    }
}

// Load compiler data
async function loadCompilerData() {
    try {
        const response = await fetch('/api/cache/stats');
        const data = await response.json();
        
        document.getElementById('cache-stats').innerHTML = 
            <p>Hits: ${data.hits || 0}</p>
            <p>Misses: ${data.misses || 0}</p>
            <p>Hit rate: ${(data.hit_rate * 100 || 0).toFixed(2)}%</p>
            <p>Cache size: ${data.size || 0} entries</p>
        ;
    } catch (err) {
        console.error('Compiler load error:', err);
    }
}

// Load dashboard data
async function loadDashboardData() {
    try {
        // System stats
        const memoryRes = await fetch('/api/memory');
        const memoryData = await memoryRes.json();
        
        document.getElementById('system-stats').innerHTML = 
            <p>Experiences: ${memoryData.experiences?.length || 0}</p>
            <p>Best sequences: ${Object.keys(memoryData.best_sequences || {}).length}</p>
            <p>Patterns: ${Object.keys(memoryData.patterns || {}).length}</p>
        ;
        
        // Recent tasks
        const tasksRes = await fetch('/api/scheduler/tasks');
        const tasksData = await tasksRes.json();
        
        const recentTasks = document.getElementById('recent-tasks');
        recentTasks.innerHTML = <p>${(tasksData.tasks || []).length} tasks scheduled</p>;
        
        // Active nodes
        const nodesRes = await fetch('/api/nodes');
        const nodesData = await nodesRes.json();
        
        const activeNodes = document.getElementById('active-nodes');
        activeNodes.innerHTML = <p>${nodesData.count} nodes active</p>;
        
        // Add a sample log entry
        addLogEntry('Dashboard loaded');
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

// Add log entry
function addLogEntry(message) {
    const logDiv = document.getElementById('system-log');
    if (!logDiv) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = <span class="log-time">[${timestamp}]</span> ${message};
    logDiv.appendChild(entry);
    logDiv.scrollTop = logDiv.scrollHeight;
}

// Node discovery
async function discoverNodes() {
    try {
        const response = await fetch('/api/nodes');
        const data = await response.json();
        addLogEntry(Discovered ${data.count} nodes);
        loadNodesData();
    } catch (err) {
        console.error('Discovery error:', err);
    }
}

// Distributed mode controls
async function startDistributed() {
    alert('Starting distributed mode...');
    // Will be implemented
}

async function stopDistributed() {
    alert('Stopping distributed mode...');
    // Will be implemented
}

// Memory controls
async function refreshMemory() {
    await loadMemoryData();
    addLogEntry('Memory refreshed');
}

async function clearMemory() {
    if (confirm('Clear all memory? This cannot be undone.')) {
        addLogEntry('Memory cleared');
    }
}

// View experience details
function viewExperience(timestamp) {
    alert(Viewing experience from ${timestamp});
}

// Cancel task
function cancelTask(taskId) {
    alert(Cancelling task ${taskId});
}