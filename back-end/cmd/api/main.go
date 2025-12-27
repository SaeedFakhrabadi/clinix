package main

import (
	"log"

	"yourproject/internal/config"
	"yourproject/internal/server"
)

func main() {
	cfg := config.Load()
	app := server.New(cfg)
	log.Fatal(app.Run(cfg.Port))
}
