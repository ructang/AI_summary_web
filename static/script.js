const socket = io();
let progressCount = 0;
let totalSteps = 0;

function processUrl() {
    const urlInput = document.getElementById('urlInput');
    const processBtn = document.getElementById('processBtn');
    const spinner = processBtn.querySelector('.spinner-border');
    const progressBar = document.getElementById('progressBar');
    const logContainer = document.getElementById('logContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    const logs = document.getElementById('logs');

    if (!urlInput.value) {
        alert('请输入URL');
        return;
    }

    // 重置状态
    progressCount = 0;
    totalSteps = 0;
    logs.innerHTML = '';
    progressBar.querySelector('.progress-bar').style.width = '0%';
    
    // 显示进度元素
    processBtn.disabled = true;
    spinner.classList.remove('d-none');
    progressBar.classList.remove('d-none');
    logContainer.classList.remove('d-none');
    downloadBtn.classList.add('d-none');

    // 发送请求
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlInput.value })
    })
    .catch(error => {
        console.error('Error:', error);
        addLog('处理失败: ' + error.message, 'text-danger');
        resetUI();
    });
}

function downloadResult() {
    window.location.href = '/download';
}

function addLog(message, className = '') {
    const logs = document.getElementById('logs');
    const log = document.createElement('div');
    log.className = className + ' animate-fade-in';
    log.textContent = message;
    logs.appendChild(log);
    logs.scrollTop = logs.scrollHeight;

    // 更新进度条
    if (message.includes('处理第')) {
        const match = message.match(/处理第 (\d+)\/(\d+)/);
        if (match) {
            progressCount = parseInt(match[1]);
            totalSteps = parseInt(match[2]);
            updateProgress();
        }
    }
}

function updateProgress() {
    const progressBar = document.getElementById('progressBar').querySelector('.progress-bar');
    const progress = (progressCount / totalSteps) * 100;
    progressBar.style.width = `${progress}%`;
}

function resetUI() {
    const processBtn = document.getElementById('processBtn');
    const spinner = processBtn.querySelector('.spinner-border');
    processBtn.disabled = false;
    spinner.classList.add('d-none');
}

// Socket.io 事件处理
socket.on('progress', function(data) {
    addLog(data.message);
});

socket.on('complete', function(data) {
    addLog(data.message, data.status === 'success' ? 'text-success' : 'text-danger');
    resetUI();
    if (data.status === 'success') {
        document.getElementById('downloadBtn').classList.remove('d-none');
    }
}); 