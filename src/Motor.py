from utils import make_logger

class Motor(object):

    def __init__(self, plus_pin, minus_pin):
        self.logger = make_logger(__name__)
        self.plus_pin = plus_pin
        self.minus_pin = minus_pin

    def run(self):
        try:
            self.logger.info('Running motor!')
            pass
        except Exception as error:
            self.logger.error(error, exc_info=True)
    
    def stop(self):
        try:
            self.logger.info('Stopping motor!')
        except Exception as error:
            self.logger.error(error, exc_info=True)

if __name__ == "__main__":
    motor = Motor(1, 2)
    motor.run()
    motor.stop()
