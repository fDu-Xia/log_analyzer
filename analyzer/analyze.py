from utils.time import get_time_stamp


def analyze(swap_logs,bundle_logs,hook_logs):
    n = len(swap_logs)
    sum1,sum2,sum3 = 0,0,0
    average_diff1 = 0
    average_diff2 = 0
    average_diff3 = 0
    for i in range(n):
        if bundle_logs[i] is None or hook_logs is None:
            n = n-1
            continue
        swap_time = get_time_stamp(swap_logs[i])
        send_bundle_time = get_time_stamp(bundle_logs[i])
        diff1 = send_bundle_time - swap_time
        sum1 += diff1
        receive_hook_time = get_time_stamp(hook_logs[i])
        diff2 = receive_hook_time - send_bundle_time
        sum2 += diff2
    print(sum1/n)
    print(sum2/n)