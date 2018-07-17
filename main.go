package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

// A list of connected clients. Typically there will only be one.
var clients = make(map[*websocket.Conn]bool)

// The boat that we will control with the server.
var boat = NewSenseekan(MotorPins{1, 2}, MotorPins{3, 4})

// Configure the upgrader
var upgrader = websocket.Upgrader{}

// Command from the client including direcitions "forward", "left", "right"
type Command struct {
	Direction string `json:"direction"`
}

// A channel for queuing commands
var commands = make(chan Command)

func main() {

	// Create a simple file server. This will serve the .js files to clinets.
	fs := http.FileServer(http.Dir("./public"))
	http.Handle("/", fs)

	// Configure websocket route
	http.HandleFunc("/ws", handleConnection)

	// Start listening for incoming chat messages
	go handleCommand()

	// Start the server on localhost port 8000 and log any errors
	log.Println("http server started on :8000")
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

func handleConnection(w http.ResponseWriter, r *http.Request) {
	// Upgrade initial GET request to a websocket
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatal(err)
	}
	// Make sure we close the connection when the function returns
	defer ws.Close()

	// Register our new client
	clients[ws] = true

	for {
		var cmd Command
		// Read in a new message as JSON and map it to a Command object
		err := ws.ReadJSON(&cmd)
		if err != nil {
			log.Printf("error: %v", err)
			delete(clients, ws)
			break
		}
		// Send the newly received command to the queue
		commands <- cmd
	}
}

func handleCommand() {
	for {
		// Grab the next message from the broadcast channel
		cmd := <-commands
		log.Print(cmd)
	}
}
