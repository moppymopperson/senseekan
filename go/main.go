package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

// The boat that we will control with the server.
// var boat = NewSenseekan(MotorPins{6, 13}, MotorPins{19, 26})

// Configure the upgrader to convert HTTP requests to websockets
var upgrader = websocket.Upgrader{}

// Command from the client including direcitions "forward", "left", "right"
type Command struct {
	Direction string `json:"direction"`
	IsPing    bool   `json:"ping"`
}

// A channel for queuing commands
var commands = make(chan Command)

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
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

// We want to stop the motors if the connection drops for any reason,
// so we create a watchdog timer. The client sends ping messages at
// a regular interval, which is shorter than the watchdog timeout.
// Each time we receive a ping message from the client, we reset the
// watchdog to keep the connection alive.
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

	for {
		// Read in a new message as JSON and map it to a Command object
		var cmd Command
		err := ws.ReadJSON(&cmd)
		if err != nil {
			log.Printf("error: %v", err)
			break
		}
		// Send the newly received command to the queue
		commands <- cmd
	}
}

func handleCommands() {
	for {
		cmd := <-commands
		log.Println(cmd)
	}
}
