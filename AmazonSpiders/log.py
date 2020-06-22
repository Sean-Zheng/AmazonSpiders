import os


def write_log(content, filename='./crawl.log'):
    log_file = open(filename, 'a', encoding='utf-8')
    log_file.write(content+'\n')
    log_file.close()


def read_log(filename='./crawl.log'):
    if not os.path.exists(filename):
        return
    log_file = open(filename, 'r', encoding='utf-8')
    lines = log_file.readlines()
    log_file.close()
    return ''.join(lines)


def remove_log(filename='./crawl.log'):
    if os.path.exists(filename):  # 如果文件存在
        os.remove(filename)
