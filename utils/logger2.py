import os
import shutil
import time
import logging

def spider_log(log_name='spider', file_folder='log_folder', level=logging.INFO, delete_existed_log=False):
    if os.path.exists(file_folder):
        if delete_existed_log == True:
            shutil.rmtree(file_folder)
            print(f"Delete {file_folder} success")
            os.mkdir(file_folder)
            print(f"Recreate {file_folder} success")
            os.chdir(file_folder)
        else:
            os.chdir(file_folder)
    else:
        os.mkdir(file_folder)
        os.chdir(file_folder)
        print(os.getcwd())
    
    create_time = time.strftime('%Y%m%d_%H%M%S')

    #Create a logger
    logger = logging.getLogger(log_name)

    #Set the log level
    logger.setLevel(level)

    #Create the log file handler
    file_hanlder = logging.FileHandler(f"{log_name}_{create_time}.txt")
    file_hanlder.setLevel(logging.DEBUG)

    #Create stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create the formatter
    formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
    file_hanlder.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    #Add the handler to logger
    logger.addHandler(file_hanlder)
    logger.addHandler(stream_handler)

    return logger

logger = spider_log(log_name='elk', file_folder='/tmp/logs')

if __name__ == '__main__':
    logger.warning('warn message')
    logger.info('info message')
    logger.debug('debug message')
    