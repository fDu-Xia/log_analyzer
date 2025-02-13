import json
import re


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