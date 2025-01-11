const socket = io();
let progressCount = 0;
let totalSteps = 0;

function processUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('请输入URL');
        return;
    }

    // 显示进度条
    document.getElementById('progressBar').classList.remove('d-none');
    
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
        alert('处理失败');
    });
}

function pollTaskStatus(taskId) {
    const interval = setInterval(() => {
        fetch(`/task/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.state === 'SUCCESS') {
                clearInterval(interval);
                document.getElementById('downloadBtn').classList.remove('d-none');
                alert('处理完成！');
            } else if (data.state === 'FAILURE') {
                clearInterval(interval);
                alert('处理失败：' + data.status);
            }
        });
    }, 2000);
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