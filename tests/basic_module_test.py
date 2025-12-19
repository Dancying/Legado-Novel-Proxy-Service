from core.source_handler import get_latest_source


def get_source_test():
    source = get_latest_source()
    print(source)
    return None


if __name__ == '__main__':
    get_source_test()
