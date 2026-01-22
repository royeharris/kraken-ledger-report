#!/bin/bash
cd "$(dirname "$0")"
echo "Starting local server for Kraken Report..."
echo "Please keep this window open while using the report."
# Open the browser after 1 second
sleep 1 && open "http://localhost:8000/Kraken Ledger Report.html" &
# Start Python server
python3 -m http.server 8000
