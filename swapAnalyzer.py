from analyzer.swapAnalyze import swap_analyze
from extractor.extract import extract_send_bundle_log, extract_webhook_log
from extractor.interface import extract_error, extract_coast
from extractor.transaction import extract_tx_info
from transaction.hash import get_tx_hash


def start_analyze(filename):
    global log_count
    global coast_sum
    global interface_error_count
    swap_logs = []
    bundle_logs = []
    hook_logs = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:  # 到达文件末尾
                break
            line = line.strip()
            log_count += 1
            error = extract_error(line)
            if error is not None:
                interface_error_count += 1
            coast = extract_coast(line)
            if int(coast) == 0:
                log_count -= 1
            else:
                coast_sum += int(coast)
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
        print('接口错误率：' + "{:.6f}".format(interface_error_count/log_count))
        print('接口平均响应时间（ms）：' + str(coast_sum / log_count))
    return swap_logs,bundle_logs,hook_logs

def main():
    swap_logs,bundle_logs,hook_logs = start_analyze('data-pull-debug.log.2025_0121')
    swap_analyze(swap_logs, bundle_logs, hook_logs)



if __name__ == "__main__":
    log_count = 0
    coast_sum = 0
    interface_error_count = 0
    main()
