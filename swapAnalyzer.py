from analyzer.analyze import analyze
from extractor.extract import get_useful_logs


def main():
    swap_logs,bundle_logs,hook_logs = get_useful_logs('data-pull-debug.log.2025_0121')
    analyze(swap_logs,bundle_logs, hook_logs)



if __name__ == "__main__":
    main()
