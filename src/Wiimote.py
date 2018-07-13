from abc import ABCMeta, abstractmethod
from utils import make_logger
from threading import Thread
from time import sleep
import cwiid

class WiimoteDelegate:
    __metaclass__ = ABCMeta

    @abstractmethod
    def wiimote_did_connect(self, wiimote):
        pass

    @abstractmethod
    def wiimote_disconnected(self, wiimote):
        pass
    
    @abstractmethod
    def wiimote_pressed_A(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_A(self, wiimote):
        pass

    @abstractmethod
    def wiimote_pressed_B(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_B(self, wiimote):
        pass

    @abstractmethod
    def wiimote_pressed_left(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_left(self, wiimote):
        pass

    @abstractmethod
    def wiimote_pressed_right(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_right(self, wiimote):
        pass

    @abstractmethod
    def wiimote_pressed_up(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_up(self, wiimote):
        pass

    @abstractmethod
    def wiimote_pressed_down(self, wiimote):
        pass

    @abstractmethod
    def wiimote_released_down(self, wiimote):
        pass

class Wiimote(object):

    def __init__(self, delegate=None):
        self.logger = make_logger(__name__)
        self.logger.info('Created new Wiimote!')
        self.delegate = delegate
        self._is_connected = False
        self.worker_thread = Thread(target=self._loop)
        self.check_interval = 0.1
        self._remote = None
        self._left_pressed = False
        self._right_pressed = False
        self._down_pressed = False
        self._up_pressed = False
        self._A_pressed = False
        self._B_pressed = False

    @property
    def is_connected(self):
        return self._is_connected

    def search_and_connect(self):
        self.logger.info('Search and connect...')
        try:
            self._remote = cwiid.Wiimote()
            self._remote.rpt_mode = cwiid.RPT_BTN
            self.rumble(0.3, 3)

            self.logger.info('Connected to wiimote!')
            self._is_connected = True
            if self.delegate is not None:
                self.delegate.wiimote_did_connect(self)
            self.worker_thread.start()
        except RuntimeError:
            self.logger.warn('Failed to connect to remote. Attempting again.')
            self.search_and_connect()

    def rumble(self, duration=1, times=1):
        if self._remote is None:
            self.logger.warn('Cannot rumble in disconnected state!')
            return
        
        for _ in range(times):
            self._remote.rumble = 1
            sleep(duration)
            self._remote.rumble = 0
            sleep(duration)

    def _loop(self):
        self.logger.debug('Beginning loop')

        while True:
            sleep(self.check_interval)
            buttons = self._remote.state['buttons']
            self._handle_presses(buttons)
            if self._check_exit_condition(buttons) == True:
                break

        self.logger.info('User disconnected wiimote!')
        self._reset_state()
        self.rumble()
        if self.delegate is not None:
            self.delegate.wiimote_disconnected(self)


    def _check_exit_condition(self, buttons):
        # Check if + and - are pressed together
        return buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0

    def _handle_presses(self, buttons):
        if (buttons & cwiid.BTN_A):
            self.logger.debug('Pressed A')
            if not self._A_pressed:
                self._A_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_A(self)
        elif self._A_pressed:
            self.logger.debug('Released A')
            self._A_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_A(self)

        if (buttons & cwiid.BTN_B):
            self.logger.debug('Pressed B')
            if not self._B_pressed:
                self._B_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_B(self)
        elif self._B_pressed:
            self.logger.debug('Released B')
            self._B_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_B(self)

        if (buttons & cwiid.BTN_UP):
            self.logger.debug('Pressed Up')
            if self._up_pressed:
                self._up_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_up(self)
        elif self._up_pressed:
            self.logger.debug('Released Up')
            self._up_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_up(self)

        if (buttons & cwiid.BTN_DOWN):
            self.logger.debug('Pressed Down')
            if not self._down_pressed:
                self._down_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_down(self)
        elif self._down_pressed:
            self.logger.debug('Released Down')
            self._down_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_down(self)

        if (buttons & cwiid.BTN_LEFT):
            self.logger.debug('Pressed Left')
            if not self._left_pressed:
                self._left_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_left(self)
        elif self._left_pressed:
            self.logger.debug('Pressed Left')
            self._left_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_left(self)
        
        if (buttons & cwiid.BTN_RIGHT):
            self.logger.debug('Pressed Right')
            if not self._right_pressed:
                self._right_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_right(self)
        elif self._right_pressed:
            self.logger.debug('Released Right')
            self._right_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_right(self)

    def _reset_state(self):
        self.logger.info('Resetting wiimote to original state')

        if self._A_pressed:
            self._A_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_A(self)

        if self._B_pressed:
            self._B_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_B(self)

        if self._up_pressed:
            self._up_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_up(self)

        if self._down_pressed:
            self._down_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_down(self)

        if self._left_pressed:
            self._left_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_left(self)

        if self._right_pressed:
            self._right_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_right(self)


if __name__ == '__main__':
    remote = Wiimote()
    remote.search_and_connect()
