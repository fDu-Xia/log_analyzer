from extractor.interface import extract_error, extract_coast

log_count = 0
coast_sum = 0
interface_error_count = 0

def interface_analyze(log):
    global log_count
    global coast_sum
    global interface_error_count
    log_count += 1
    error = extract_error(log)
    if error is not None:
        interface_error_count += 1
    coast = extract_coast(log)
    if coast == 0:
        log_count -= 1
    print('接口错误率：'+str(interface_error_count/log_count))
    print('接口平均响应时间（ms）：'+str(coast_sum/log_count))