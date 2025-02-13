from extractor.interface import extract_error
from utils.time import get_time_stamp


def swap_analyze(swap_logs, bundle_logs, hook_logs):
    average_time(swap_logs,bundle_logs,hook_logs)
    swap_error_analyze(swap_logs,hook_logs)

def average_time(swap_logs, bundle_logs, hook_logs):
    n = len(swap_logs)
    sum1, sum2, sum3 = 0, 0, 0
    for i in range(n):
        if bundle_logs[i] is None or hook_logs is None:
            n = n - 1
            continue
        swap_time = get_time_stamp(swap_logs[i])
        send_bundle_time = get_time_stamp(bundle_logs[i])
        diff1 = send_bundle_time - swap_time
        sum1 += diff1
        receive_hook_time = get_time_stamp(hook_logs[i])
        diff2 = receive_hook_time - send_bundle_time
        sum2 += diff2
    print('swap交易构建完成到发送完成平均时间：' + str(sum1 / n))
    print('发送完成到上链平均时间：' + str(sum2 / n))

def swap_error_analyze(swap_logs,hook_logs):
    n = len(swap_logs)
    on_chain_count = 0
    swap_error_count = 0
    error_map = {}
    for i in range(n):
        if hook_logs[i] is not None:
            on_chain_count += 1
        error_type = extract_error(swap_logs[i])
        if error_type is not None:
            swap_error_count += 1
            if error_type in error_map:
                error_map[error_type] += 1
            else:
                error_map[error_type] = 1

    print('swap上链率： '+str(on_chain_count/n))
    print('swap接口错误率：'+str(swap_error_count/n))
    for error_type, count in error_map.items():
        print(f"错误代码: {error_type}, 数量: {count}")