from kombu import Exchange, Queue
from config import settings

# Redis 配置
broker_url = settings.REDIS_URL
result_backend = settings.REDIS_URL
broker_connection_retry = True
broker_connection_retry_on_startup = True

# 基本配置
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True

# Windows 特定配置
worker_pool = 'solo'
worker_max_tasks_per_child = 1  # 每个worker处理完一个任务后重启
worker_prefetch_multiplier = 1  # 限制每个worker同时处理的任务数
worker_concurrency = 1  # 限制并发数为1

# 任务配置
task_track_started = True
task_time_limit = 30 * 60  # 30 分钟
task_soft_time_limit = 25 * 60  # 25 分钟
task_acks_late = True  # 任务完成后再确认
task_reject_on_worker_lost = True  # worker丢失时拒绝任务

# 结果配置
result_expires = 24 * 60 * 60  # 24 小时
result_persistent = True  # 持久化存储结果
result_cache_max = 1000  # 最大缓存结果数

# 队列配置
task_default_queue = 'default'
task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# 任务路由
task_routes = {
    'main.process_content': {'queue': 'default'}
}

# 日志配置
worker_redirect_stdouts = True
worker_redirect_stdouts_level = 'INFO' 