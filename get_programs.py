import os
import shutil
import sys
import logging
import threading
import _thread


def del_non_dir(path):
    """
    Clean empty files,清理空文件夹和空文件
    :param path: 文件路径，检查此文件路径下的子文件
    :return: None
    """
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(path + file):  # 如果是文件夹
            print("Dir: ", file)
            if not os.listdir(path + file):  # 如果子文件为空
                print("Remove empty ", file)
                os.rmdir(path + file)  # 删除空文件夹
        elif os.path.isfile(file):  # 如果是文件
            print("File: ", file)
            if os.path.getsize(file) == 0:  # 文件大小为 0
                os.remove(file)  # 删除这个文件
        else:
            print("? ", file)
    print("Over!")


def del_github(path):
    """
    删除 .github 文件夹和.gitignore .travis.yml 文件
    :param path: 文件路径
    :return: None
    """
    files = os.listdir(path)
    for file in files:
        if os.path.exists(path + file + "/.github"):
            shutil.rmtree(path + file + "/.github")
        if os.path.isfile(path + file + "/.gitignore"):
            os.remove(path + file + "/.gitignore")
    print("Over!")


def write_files(file, line):
    if not os.path.isfile(file):
        print("%s not exits!" % file)
        return
    with open(file, 'a+', encoding='utf-8') as f:
        f.writelines(line)
    return


def download_programs(output_directory, program_link):
    """
    从GitHub上下载项目
    :param output_directory: 项目保存路径
    :param program_link: 项目链接
    :param program_name: 项目名称
    :return: None
    """
    try:
        program_name = program_link.split('/')[-1].split('.')[0]
        if os.path.exists(output_directory + program_name):
            logging.debug("Git program already exists: %s", program_link)
            return

        result = os.system('git clone ' + program_link +
                           ' ' + output_directory + program_name)
        if result == 0:
            os.system('chmod -R 777 ' + output_directory + program_name)
        else:
            # write_files(output_directory + error_file, program_link)
            logging.debug("result not 0: %s", program_link)
    except:
        logging.error("Try download except: %s", program_link)


def down_from_github(output_directory, program_links):
    """
    根据url_file下载项目到output_directory
    :param output_directory: 保存下载项目的路径
    :param url_file: 要下载项目的链接
    :return: None
    """
    try:
        length = len(program_links)
        for i in range(0, length, 10):
            if length > i + 10:
                k = 10
            else:
                k = length - i
            try: 
                threads = [threading.Thread(target=download_programs, args=(output_directory, program_links[i+j])) for j in range(k)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
            except:
                logging.error("Thread Download Error: %s", program_links[i])          
    except:
        logging.critical("Unknown Error!")


url_file = './clone_urls_6000.txt' 
dir_path = '/data/zdj/java_project/'
LOG_FORMAT = "%(levelname)s %(thread)d %(funcName)s %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

if not os.path.exists(dir_path):
    logging.error("output directory not exist!")

if os.path.isfile(url_file):
    with open(url_file, 'r', encoding='utf-8') as f:
        url = [line.strip() for line in f.readlines()]
else:
    logging.error("存放GitHub项目url的文件不存在")

down_from_github(dir_path, url)
