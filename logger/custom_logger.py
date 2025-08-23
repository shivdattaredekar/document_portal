import logging
import os
from datetime import datetime


class CustomLogger:
    def __init__(self, logs_dir = 'logs'):
        # Ensure log directory exists
        self.log_dir = os.path.join(os.getcwd(), logs_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        # Create Timestamped log Filename
        log_file =  f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        log_file_path = os.path.join(self.log_dir, log_file)

        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            format="[%(asctime)s] %(filename)s %(name)s (line:%(lineno)d) - %(message)s",
            level=logging.INFO,
        )

    def get_logger(self, name = __file__):
        return logging.getLogger(os.path.basename(name))
    

if __name__ == '__main__':
    logger = CustomLogger()
    logger = logger.get_logger(__file__)
    logger.info("Custom logger initialized.")


