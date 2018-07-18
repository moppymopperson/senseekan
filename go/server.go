package main

import (
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

// Command from the client including direcitions "forward", "left", "right"
type Command struct {
	Direction string `json:"direction"`
	IsPing    bool   `json:"ping"`
}

// WebsocketCommandServer receives commands from the webclient and provides a callback
// to process commands.
type WebsocketCommandServer struct {
	publicDir     http.Dir
	timeout       time.Duration
	commandQueue  chan Command
	HandleCommand func(cmd Command)
}

// NewWebsocketCommandServer creates a new websocket server that serves that also
// serves static files in the given directory.
func NewWebsocketCommandServer(publicDir string) *WebsocketCommandServer {
	return &WebsocketCommandServer{
		http.Dir(publicDir),
		2 * time.Second,
		make(chan Command),
		func(cmd Command) { log.Println("HandleCommand has not been set!") },
	}
}

// ListenAndServe begins serving static content and receiving websocket connection
// requests.
func (wss *WebsocketCommandServer) ListenAndServe(addr string) {
	// Create a simple file server. This will serve the .js files to clients.
	fs := http.FileServer(http.Dir("../public"))
	http.Handle("/", fs)

	// Configure websocket route
	http.HandleFunc("/ws", wss.handleConnection)

	log.Println("http server started on :8000")
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

func (wss *WebsocketCommandServer) handleConnection(w http.ResponseWriter, r *http.Request) {
	// Upgrade initial GET request to a websocket.
	// For our purposes we accept connections from anywhere.
	upgrader := websocket.Upgrader{}
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }
	ws, err := upgrader.Upgrade(w, r, nil)
	defer ws.Close()
	if err != nil {
		log.Fatalf("Upgrade error: %v", err)
	}

	// Monitor ping and process commands each on their own threads
	watchdog := time.NewTimer(wss.timeout)
	go monitorPings(ws, watchdog)
	go wss.processCommands()

	// Read from the websocket on this thread
	for {
		var cmd Command
		if err := ws.ReadJSON(&cmd); err != nil {
			log.Printf("Connection closed: %v", err)
			break
		}

		if cmd.IsPing {
			log.Println("ping received!")
			watchdog.Reset(wss.timeout)
		} else {
			log.Println("command received!")
			watchdog.Reset(wss.timeout)
			wss.commandQueue <- cmd
		}
	}
}

func monitorPings(ws *websocket.Conn, watchdog *time.Timer) {
	<-watchdog.C
	ws.Close()
	log.Println("Watchdog expired, cutting connection!")
}

func (wss *WebsocketCommandServer) processCommands() {
	for {
		cmd := <-wss.commandQueue
		wss.HandleCommand(cmd)
	}
}
