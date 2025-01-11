// 初始化Socket.IO连接
const socket = io();

// 生成浮动图标
function initFloatingIcons() {
    const container = document.querySelector('.floating-icons');
    const icons = ['fa-microchip', 'fa-brain', 'fa-network-wired'];
    
    // 创建6个浮动图标
    for (let i = 0; i < 6; i++) {
        const icon = document.createElement('div');
        icon.className = 'floating-icon';
        icon.innerHTML = `<i class="fas ${icons[i % icons.length]} fa-3x"></i>`;
        
        // 随机位置
        icon.style.left = `${Math.random() * 90}%`;
        icon.style.top = `${Math.random() * 90}%`;
        icon.style.transform = `rotate(${Math.random() * 360}deg)`;
        icon.style.animationDuration = `${5 + Math.random() * 5}s`;
        
        container.appendChild(icon);
    }
    
    // 创建粒子效果
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 2}s`;
        particle.style.animationDuration = `${3 + Math.random() * 4}s`;
        
        container.appendChild(particle);
    }
}

// 处理文本输入
function handleTextInput() {
    showUrlInput('请输入网页链接...');
}

// 处理音频输入
function handleAudioInput() {
    showUrlInput('请输入音频链接...');
}

// 处理文件上传
function handleUpload() {
    // TODO: 实现文件上传功能
    alert('文件上传功能即将推出');
}

// 显示URL输入框
function showUrlInput(placeholder) {
    const inputGroup = document.getElementById('urlInputGroup');
    const urlInput = document.getElementById('urlInput');
    
    inputGroup.classList.remove('d-none');
    urlInput.placeholder = placeholder;
    urlInput.focus();
}

// 处理URL
function processUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('请输入链接');
        return;
    }

    // 显示进度相关元素
    document.getElementById('progressContainer').classList.remove('d-none');
    document.getElementById('logsContainer').classList.remove('d-none');
    
    // 禁用处理按钮
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = true;
    
    // 发送处理请求
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: url})
    })
    .then(response => response.json())
    .then(data => {
        if (data.task_id) {
            pollTaskStatus(data.task_id);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addLog('处理失败', 'error');
        resetUI();
    });
}

// 轮询任务状态
function pollTaskStatus(taskId) {
    const interval = setInterval(() => {
        fetch(`/task/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.state === 'SUCCESS') {
                clearInterval(interval);
                if (data.result && data.result.status === 'success') {
                    document.getElementById('downloadBtn').classList.remove('d-none');
                    addLog('处理完成！', 'success');
                } else {
                    addLog(`处理失败：${data.result ? data.result.message : '未知错误'}`, 'error');
                }
                resetUI();
            } else if (data.state === 'FAILURE') {
                clearInterval(interval);
                addLog(`处理失败：${data.status || '任务执行失败'}`, 'error');
                resetUI();
            } else if (data.state === 'PROGRESS') {
                addLog(data.status || '处理中...', 'info');
            } else if (data.state === 'PENDING') {
                addLog('任务等待中...', 'info');
            }
        })
        .catch(error => {
            clearInterval(interval);
            console.error('Error:', error);
            addLog('系统错误，请稍后重试', 'error');
            resetUI();
        });
    }, 2000);
}

// 添加日志
function addLog(message, type = 'info') {
    const logs = document.getElementById('logs');
    const log = document.createElement('div');
    log.className = `log-entry ${type}`;
    
    // 根据消息类型选择图标
    let icon = 'info-circle';
    if (type === 'error') icon = 'times-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'warning') icon = 'exclamation-circle';
    
    log.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    logs.appendChild(log);
    logs.scrollTop = logs.scrollHeight;

    // 更新进度条
    if (message.includes('处理第')) {
        const match = message.match(/处理第 (\d+)\/(\d+)/);
        if (match) {
            updateProgress(parseInt(match[1]), parseInt(match[2]));
        }
    }
}

// 更新进度条
function updateProgress(current, total) {
    const progressFill = document.getElementById('progressFill');
    const progress = (current / total) * 100;
    progressFill.style.width = `${progress}%`;
}

// 重置UI状态
function resetUI() {
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = false;
}

// 下载结果
function downloadResult() {
    window.location.href = '/download';
}

// Socket.IO事件处理
socket.on('progress', function(data) {
    addLog(data.message);
});

socket.on('complete', function(data) {
    addLog(data.message, data.status === 'success' ? 'success' : 'error');
    resetUI();
    if (data.status === 'success') {
        document.getElementById('downloadBtn').classList.remove('d-none');
    }
});

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initFloatingIcons();
}); 