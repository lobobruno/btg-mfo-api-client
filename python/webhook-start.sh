#!/bin/bash

PORT=8000

echo "Starting webhook server on port $PORT..."
python webhook_server.py &
SERVER_PID=$!

sleep 1

echo "Starting ngrok tunnel..."
ngrok http $PORT &
NGROK_PID=$!

trap "echo 'Shutting down...'; kill $SERVER_PID $NGROK_PID 2>/dev/null; exit" INT TERM

echo ""
echo "Both services running. Press Ctrl+C to stop."
echo "  Python server PID: $SERVER_PID"
echo "  ngrok PID: $NGROK_PID"
echo ""
echo "Check your ngrok URL at: http://127.0.0.1:4040"
echo ""

wait
