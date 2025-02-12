import binascii
import json
import re

from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict, encode_transaction
from eth_utils import keccak

def extract_signature(log_data):
    if log_data['code'] != 0:
        return None
    raw_tx = log_data['data']

    # 提取签名参数
    # -2 表示最后一个字节
    v = '0x' + raw_tx[-134:-132]

    # r 和 s 各占 32 字节(64个字符)
    # 从倒数第二个字节往前数 64 个字符是 s
    s = '0x' + raw_tx[-64:]

    # 从 s 前面取 64 个字符是 r
    r = '0x' + raw_tx[-130:-66]

    return r, s, v

def check_is_related_sign_log(sign_log,tx_info)->bool:
    if tx_info is None:
        return False

    pattern = r'params \[{(.+?)}\]'
    match = re.search(pattern, sign_log)
    if not match:
        return False
    params_str = match.group(1)
    params = params_str.split()
    return (
        tx_info['chainId'] == params[0] and
        tx_info['from'] == params[1] and
        tx_info['to'] == params[2] and
        tx_info['value'] == params[3] and
        tx_info['gas'] == params[4] and
        tx_info['gasPrice'] == params[5] and
        tx_info['nonce'] == params[6] and
        tx_info['data'] == params[7]
    )

def calculate_tx_hash(sign_log:str,tx_info: dict):
    if sign_log is None:
        return None
    r,s,v = extract_signature(sign_log)
    try:
        tx_info.pop('from')
        for key in ['chainId', 'nonce', 'value', 'gas', 'gasPrice']:
            tx_info[key] = int(tx_info[key])
    except KeyError:
        return None

    unsigned_transaction = serializable_unsigned_transaction_from_dict(
        tx_info, blobs=None
    )

    encoded_transaction = encode_transaction(unsigned_transaction, vrs=(int(v,16), int(r,16), int(s,16)))
    return binascii.hexlify(keccak(encoded_transaction)).decode('utf-8')

def get_tx_hash(f,tx_info):
    while True:
        sign_line = f.readline()
        if not sign_line:  # 到达文件末尾
            return None
        if '/signTransaction' in sign_line:
            if check_is_related_sign_log(sign_line, tx_info):
                pattern = r'result \[(.*?)]'
                match = re.search(pattern, sign_line)
                if not match:
                    continue
                sign_log = json.loads(match.group(1))
                return calculate_tx_hash(sign_log,tx_info)