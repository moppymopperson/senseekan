from utils import make_logger
from RPi import GPIO


class Motor(object):

    def __init__(self, plus_pin, minus_pin):
        GPIO.setup([plus_pin, minus_pin], GPIO.OUT)
        self.logger = make_logger(__name__)
        self.plus_pin = plus_pin
        self.minus_pin = minus_pin
        self.stop()

    def start(self):
        self.logger.info('Starting motor!')
        GPIO.output(self.plus_pin, GPIO.HIGH)

    def stop(self):
        self.logger.info('Stopping motor!')
        GPIO.output(self.plus_pin, GPIO.LOW)
        GPIO.output(self.minus_pin, GPIO.LOW)


if __name__ == "__main__":
    from time import sleep
    GPIO.setmode(GPIO.BOARD)
    motor = Motor(37, 35)
    motor.start()
    sleep(2.0)
    motor.stop()

    GPIO.cleanup()
