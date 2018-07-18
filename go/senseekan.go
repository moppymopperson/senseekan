package main

import (
	"github.com/stianeikeland/go-rpio"
)

func init() {
	if err := rpio.Open(); err != nil {
		// log.Fatal("Unable to initialize GPIO", err)
	}
}

// Senseekan represents a boat capable of moving left, right, and forward
type Senseekan struct {
	leftMotor  *motor
	rightMotor *motor
}

// MotorPins specifies the pins to be used for a motor
type MotorPins struct {
	pos int
	neg int
}

// NewSenseekan creates a new boat from the pins associated with its motors.
func NewSenseekan(leftPins MotorPins, rightPins MotorPins) *Senseekan {
	leftMotor := newMotor(leftPins)
	rightMotor := newMotor(rightPins)
	return &Senseekan{leftMotor, rightMotor}
}

// GoForward makes the boat move forward in a straight line at full speed.
func (s *Senseekan) GoForward() {
	s.leftMotor.run()
	s.rightMotor.run()
}

// TurnRight makes the boat turn to the right.
func (s *Senseekan) TurnRight() {
	s.leftMotor.run()
	s.rightMotor.stop()
}

// TurnLeft makes the boat turn to the left.
func (s *Senseekan) TurnLeft() {
	s.leftMotor.stop()
	s.rightMotor.stop()
}

// Stop makes the boat stop
func (s *Senseekan) Stop() {
	s.leftMotor.stop()
	s.rightMotor.stop()
}

type motor struct {
	posPin rpio.Pin
	negPin rpio.Pin
}

func newMotor(pins MotorPins) *motor {
	posPin := rpio.Pin(pins.pos)
	negPin := rpio.Pin(pins.neg)

	posPin.Output()
	posPin.Low()

	negPin.Output()
	negPin.Low()

	return &motor{posPin, negPin}
}

func (m *motor) run() {
	m.posPin.High()
}

func (m *motor) stop() {
	m.posPin.Low()
}
