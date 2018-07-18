package main

import "log"

var boat = NewSenseekan(MotorPins{6, 13}, MotorPins{19, 26})
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
