from analyzer.interfaceAnalyze import interface_analyze
from extractor.interface import extract_error, extract_coast
from extractor.transaction import extract_tx_info
from transaction.hash import get_tx_hash

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
