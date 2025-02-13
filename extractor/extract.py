import json
import re

from transaction.hash import get_tx_hash


def extract_tx_info(swap_log):
    try:
        # 提取result部分的JSON字符串
        result_match = re.search(r'result \[(.*?)] coast', swap_log)
        if result_match:
            result_json = json.loads(result_match.group(1))

            # 获取交易信息
            info = result_json['data']['tx']['56']['tx']
            return info
    except TypeError:
        return None

def extract_tx_error(swap_log):
    try:
        result_match = re.search(r'result \[(.*?)] coast', swap_log)
        if result_match:
            result_json = json.loads(result_match.group(1))
            if  result_json['code'] != 0:
                return result_json['code']
    except TypeError:
        return None


def extract_send_bundle_log(f,tx_hash):
    while True:
        bundle_line = f.readline()
        if not bundle_line:  # 到达文件末尾
            return None
        if tx_hash in bundle_line and 'eth_sendBundle' in bundle_line:
            return bundle_line

def extract_webhook_log(f,tx_hash):
    while True:
        hook_line = f.readline()
        if not hook_line:  # 到达文件末尾
            return None
        if tx_hash in hook_line and 'hook' in hook_line:
            return hook_line

def get_useful_logs(filename):
    swap_logs = []
    bundle_logs = []
    hook_logs = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:  # 到达文件末尾
                break
            line = line.strip()
            if '/swap-tx' in line:
                swap_logs.append(line)
                tx_info = extract_tx_info(line)

                pos = f.tell()
                tx_hash = get_tx_hash(f,tx_info)

                bundle_log = extract_send_bundle_log(f,tx_hash)

                bundle_logs.append(bundle_log)
                hook_log = extract_webhook_log(f,tx_hash)

                hook_logs.append(hook_log)
                f.seek(pos)
    return swap_logs,bundle_logs,hook_logs