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
        
    # Wiimote Delegate Methods
    def wiimote_did_connect(self, wiimote):
        self.logger.info('Connected to wiimote!')

    def wiimote_disconnected(self, wiimote):
        self.logger.info('Wiimote disconnected!')

    def wiimote_pressed_A(self, wiimote):
        self.logger.debug('Pressed A')
    
    def wiimote_released_A(self, wiimote):
        self.logger.debug('Released A')

    def wiimote_pressed_B(self, wiimote):
        self.logger.debug('Pressed B')

    def wiimote_released_B(self, wiimote):
        self.logger.debug('Released B')
    
    def wiimote_pressed_left(self, wiimote):
        self.logger.debug('Pressed Left')

    def wiimote_released_left(self, wiimote):
        self.logger.debug('Released Left')

    def wiimote_pressed_right(self, wiimote):
        self.logger.debug('Pressed Right')
    
    def wiimote_released_right(self, wiimote):
        self.logger.debug('Released Right')

    def wiimote_pressed_up(self, wiimote):
        self.logger.debug('Pressed Up')

    def wiimote_released_up(self, wiimote):
        self.logger.debug('Released Up')

    def wiimote_pressed_down(self, wiimote):
        self.logger.debug('Pressed Dowear')

    def wiimote_released_down(self, wiimote):
        self.logger.debug('Released Down')
        

if __name__ == '__main__':
    left_motor = Motor(37, 35)
    right_motor = Motor(33, 31)
    seekan = Senseekan(left_motor, right_motor)
    seekan.connect()