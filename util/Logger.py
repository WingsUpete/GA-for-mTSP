"""
Logger that logs to both stdout and a file
"""
import logging
from datetime import datetime
import sys
import os

LOGGING_FOLDER = 'log/'
if not os.path.isdir(LOGGING_FOLDER):
    os.mkdir(LOGGING_FOLDER)


class Logger:
    def __init__(self, activate=True, logging_folder=LOGGING_FOLDER, time_tag=None, std_out=True):
        self.activate = activate
        self.time_tag = time_tag if time_tag else datetime.now().strftime("%Y%m%d_%H_%M_%S")
        if self.activate:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
            self.logging_folder = logging_folder
            if not os.path.isdir(self.logging_folder):
                os.mkdir(self.logging_folder)

            # Create a File Handler
            fName = '{}.log'.format(self.time_tag)
            self.f_handler = logging.FileHandler(os.path.join(self.logging_folder, fName))
            self.f_handler.terminator = ''
            self.logger.addHandler(self.f_handler)

            # Create an stdout Stream Handler
            self.std_out = std_out
            if self.std_out:
                self.stdout_handler = logging.StreamHandler(sys.stdout)
                self.stdout_handler.terminator = ''
                self.logger.addHandler(self.stdout_handler)

    """
        Log a message into stdout and log file simultaneously
    """
    def log(self, message='\nCHECK YOUR CODE\n'):
        if self.activate:
            self.logger.debug(message)

    def close(self):
        if self.activate:
            self.f_handler.close()
            if self.std_out:
                self.stdout_handler.close()


if __name__ == '__main__':
    """
        Test
    """
    logger = Logger(activate=False)
    logger.log('Test test\n')
    logger.log('Test 0\n')
    logger.log('Test 1\n')
    logger.close()

    print('\nTest activated logger.')

    logger = Logger(activate=True, logging_folder='test/')
    logger.log('Test test\n')
    logger.log('Test 0\n')
    logger.log('Test 1\n')
    logger.close()