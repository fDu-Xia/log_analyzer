import json
import re
from datetime import datetime


def get_time_stamp(log):
    if log is None:
        return None
    pattern = r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"
    match = re.search(pattern, log)

    if match:
        date_str = match.group(1)
        # 转换为datetime对象
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # 获取时间戳
        return int(dt.timestamp())
def get_block_time(log):
    if log is None:
        return None
    pattern = r'receive hook: (.+)$'
    match = re.search(pattern, log)

    if match:
        json_str = match.group(1)
        # 解析JSON
        data = json.loads(json_str)
        # 获取timestamp
        timestamp = data['event']['data']['block']['timestamp']
        return int(timestamp)/1000