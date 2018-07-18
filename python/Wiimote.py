from abc import ABCMeta, abstractmethod
from threading import Thread
from time import sleep
import re
import subprocess
import cwiid

from utils import make_logger


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
        # Public
        self.logger = make_logger(__name__)
        self.logger.info('Created new Wiimote!')
        self.delegate = delegate
        self.check_interval = 0.1
        self.watchdog_timeout = 1.0

        # Private
        self._is_connected = False
        self._worker_thread = None
        self._watchdog_thread = None
        self._should_terminate = False
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
            self._set_disconnect_timeout()
            self.rumble(0.3, 3)

            self.logger.info('Connected to wiimote!')
            self._is_connected = True
            if self.delegate is not None:
                self.delegate.wiimote_did_connect(self)

            self._worker_thread = Thread(target=self._loop)
            self._worker_thread.start()

            self._watchdog_thread = Thread(target=self._watchdog_loop)
            self._watchdog_thread.start()

        except RuntimeError:
            self.logger.warning(
                'Failed to connect to remote. Attempting again.')
            self.search_and_connect()

    def rumble(self, duration=1, times=1):
        if self._remote is None:
            self.logger.warning('Cannot rumble in disconnected state!')
            return

        for _ in range(times):
            self._remote.rumble = 1
            sleep(duration)
            self._remote.rumble = 0
            sleep(duration)

    def disconnect(self):
        if not self.is_connected:
            self.logger.warning('Remote already disconnected. Ignoring.')
            return

        self.logger.info('User disconnected wiimote!')
        if self._remote is not None:
            self.rumble()
            self._remote.close()
        self._should_terminate = True
        self._watchdog_thread.join()
        self._reset_state()
        if self.delegate is not None:
            self.delegate.wiimote_disconnected(self)

    def _loop(self):
        self.logger.debug('Beginning loop')

        while not self._should_terminate:
            sleep(self.check_interval)
            self._handle_presses()
            if self._check_exit_condition():
                break

        self.disconnect()

    def _check_exit_condition(self):
        # If the remote has been disconnected, we'll count that is an exit
        if self._remote is None:
            return True

        # Check if + and - are pressed together
        buttons = self._remote.state['buttons']
        return buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0

    def _watchdog_loop(self):
        # Check to see if the remote is still connected and force the thread
        # to exit if there is an issue
        self.logger.info('Watchdog loop starting up')
        while not self._should_terminate:
            try:
                self.logger.debug('request_status')
                self._remote.request_status()
                sleep(self.watchdog_timeout)
            except ValueError:
                self.logger.warning('Wiimote was closed when watchdog expired')
            except RuntimeError:
                self.logger.error('Wiimote disconnected!')
                self._should_terminate = True
                self._remote = None

    def _set_disconnect_timeout(self):
        # See https://github.com/abstrakraft/cwiid/issues/23 for details
        connected_devices = subprocess.check_output(("hcitool", "con"))

        # extract bluetooth MAC addresses
        addresses = re.findall(
            r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))", connected_devices)
        for i in addresses:
            name = subprocess.check_output(("hcitool", "name", i[0]))
            # identify Wiimotes. You may need to change this if looking for
            # balance boards we are also assuming that you only have one
            # Wiimote attached at one time, or that we want to set them all to
            # have the same timeout
            if name.strip() == "Nintendo RVL-CNT-01":
                self.logger.info('Setting timeout...')
                subprocess.call(
                    ("sudo", "hcitool", "lst", i[0],
                     str(1000 * self.watchdog_timeout*16/10)))

    def _handle_presses(self):
        if self._remote is None:
            self.logger.warning('Checked presses for discconected wiimote')
            return
        buttons = self._remote.state['buttons']

        if buttons & cwiid.BTN_A:
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

        if buttons & cwiid.BTN_B:
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

        if buttons & cwiid.BTN_UP:
            self.logger.debug('Pressed Up')
            if not self._up_pressed:
                self._up_pressed = True
                if self.delegate is not None:
                    self.delegate.wiimote_pressed_up(self)
        elif self._up_pressed:
            self.logger.debug('Released Up')
            self._up_pressed = False
            if self.delegate is not None:
                self.delegate.wiimote_released_up(self)

        if buttons & cwiid.BTN_DOWN:
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

        if buttons & cwiid.BTN_LEFT:
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

        if buttons & cwiid.BTN_RIGHT:
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
        self._is_connected = False
        self._should_terminate = False

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
