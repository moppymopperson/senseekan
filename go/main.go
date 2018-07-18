package main

import (
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

// The boat that we will control with the server.
var boat = NewSenseekan(MotorPins{6, 13}, MotorPins{19, 26})

// Configure the upgrader to convert HTTP requests to websockets
var upgrader = websocket.Upgrader{}

// Command from the client including direcitions "forward", "left", "right"
type Command struct {
	Direction string `json:"direction"`
	IsPing    bool   `json:"ping"`
}

type ping struct{}

// A channel for queuing commands
var commands = make(chan Command)

// A channel for queing ping messages (keep alives)
var pings = make(chan ping)

func main() {

	// Create a simple file server. This will serve the .js files to clients.
	fs := http.FileServer(http.Dir("../public"))
	http.Handle("/", fs)

	// Configure websocket route
	http.HandleFunc("/ws", handleConnection)

	// Start listening for incoming chat messages
	go handleCommands()

	// Start the server on localhost port 8000 and log any errors
	log.Println("http server started on :8000")
	if err := http.ListenAndServe(":8000", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

func handleConnection(w http.ResponseWriter, r *http.Request) {
	// Upgrade initial GET request to a websocket.
	// For our purposes we accept connections from anywhere.
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatal(err)
	}

	// Make sure we close the connection when the function returns
	defer ws.Close()

	// Run a thread that will monitor and close the socket if it doesn't
	// check in frequently enough.
	go monitorPings(ws, 2*time.Second)

	for {
		// Read in a new message as JSON and map it to a Command object
		var cmd Command
		if err := ws.ReadJSON(&cmd); err != nil {
			log.Printf("error: %v", err)
			boat.Stop()
			break
		}

		// Send the newly received command to the proper queue
		if cmd.IsPing {
			pings <- ping{}
		} else {
			commands <- cmd
		}
	}
}

func handleCommands() {
	for {
		cmd := <-commands
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
}

// We want to stop the motors if the connection drops for any reason,
// so we create a watchdog timer. The client sends ping messages at
// a regular interval, which is shorter than the watchdog timeout.
// Each time we receive a ping message from the client, we reset the
// watchdog to keep the connection alive.
func monitorPings(ws *websocket.Conn, timeout time.Duration) {

	watchdog := time.NewTimer(timeout)
	for {
		select {
		case <-pings:
			log.Println("ping!")
			watchdog.Reset(timeout)
		case <-watchdog.C:
			log.Println("Watchdog timed out!")
			ws.Close()
			return
		}
	}
}
