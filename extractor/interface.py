import json
import re

def extract_error(log):
    try:
        result_match = re.search(r'result \[(.*?)] coast', log)
        if result_match:
            result_json = json.loads(result_match.group(1))
            if  'code' in result_json and result_json['code'] != 0:
                return result_json['code']
            else:
                return None
    except TypeError:
        return None

def extract_coast(log):
    pattern = r'coast\[(\d+)\]ms'
    match = re.search(pattern, log)
    if match:
        coast = match.group(1)
        return coast
    else:
        return 0