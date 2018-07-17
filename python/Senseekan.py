from utils import make_logger

from Motor import Motor
from Wiimote import Wiimote, WiimoteDelegate


class Senseekan(WiimoteDelegate):

    def __init__(self, left_motor, right_motor):
        self.logger = make_logger(__name__)
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.wiimote = Wiimote(self)

    def connect(self):
        self.logger.info('Attempting to connect wiimote...')
        self.wiimote.search_and_connect()

    def start_going_forward(self):
        self.logger.debug('start_going_forward')
        self.left_motor.start()
        self.right_motor.start()

    def start_turning_right(self):
        self.logger.debug('start_turning_right')
        self.left_motor.start()
        self.right_motor.stop()

    def start_turning_left(self):
        self.logger.debug('start_turning_left')
        self.right_motor.start()
        self.left_motor.stop()

    def stop(self):
        self.logger.debug('stop')
        self.right_motor.stop()
        self.left_motor.stop()

    def shutdown(self):
        self.logger.info('shutdown')
        self.wiimote.disconnect()
        GPIO.cleanup()

    # Wiimote Delegate Methods

    def wiimote_did_connect(self, wiimote):
        self.logger.info('Connected to wiimote!')

    def wiimote_disconnected(self, wiimote):
        self.logger.info('Wiimote disconnected!')
        self.stop()
        # self.connect()
        self.shutdown()

    def wiimote_pressed_left(self, wiimote):
        self.logger.debug('Turning Left')
        self.start_turning_left()

    def wiimote_released_left(self, wiimote):
        self.logger.debug('Stopping Left Turn')
        self.stop()

    def wiimote_pressed_right(self, wiimote):
        self.logger.debug('Turning Right')
        self.start_turning_right()

    def wiimote_released_right(self, wiimote):
        self.logger.debug('Stopping Right Turn')
        self.stop()

    def wiimote_pressed_up(self, wiimote):
        self.logger.debug('Going Forward')
        self.start_going_forward()

    def wiimote_released_up(self, wiimote):
        self.logger.debug('Stopping Going Foward')
        self.stop()

    def wiimote_pressed_down(self, wiimote):
        pass

    def wiimote_released_down(self, wiimote):
        pass

    def wiimote_pressed_A(self, wiimote):
        pass

    def wiimote_released_A(self, wiimote):
        pass

    def wiimote_pressed_B(self, wiimote):
        pass

    def wiimote_released_B(self, wiimote):
        pass


if __name__ == '__main__':
    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)

    left = Motor(37, 35)
    right = Motor(33, 31)
    seekan = Senseekan(left, right)

    try:
        seekan.connect()
    except KeyboardInterrupt:
        print("Cleaning up...")
        seekan.shutdown()
        print("Done")
