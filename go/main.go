package main

import "log"

var boat = NewSenseekan(MotorPins{19, 26}, MotorPins{13, 6})
var commandServer = NewWebsocketCommandServer("../public")

func main() {
	commandServer.HandleCommand = handleCommand
	commandServer.ListenAndServe(":8000")
}

func handleCommand(cmd Command) {
	log.Println("Handling Command", cmd)
	switch cmd.Direction {
	case "left":
		boat.TurnLeft()
	case "right":
		boat.TurnRight()
	case "forward":
		boat.GoForward()
	case "stop":
		boat.Stop()
	}
}
