#!/usr/bin/env python3

import os
import json
import socket

# Path to MPV's IPC socket
MPV_SOCKET = "/tmp/mpvsocket"

def get_mpv_status():
    if not os.path.exists(MPV_SOCKET):
        return {"text": "MPV not running", "tooltip": "MPV player is not running"}

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(MPV_SOCKET)
        client.sendall(b'{"command": ["get_property", "media-title"]}\n')
        response = client.recv(1024)
        client.sendall(b'{"command": ["get_property", "pause"]}\n')
        pause_response = client.recv(1024)
        client.close()

        media_title = json.loads(response).get("data", "No media")
        paused = json.loads(pause_response).get("data", False)

        text = f"{'[Paused] ' if paused else ''}{media_title}"

        return {"text": text, "tooltip": text}
    except Exception as e:
        return {"text": "Error", "tooltip": str(e)}

if __name__ == "__main__":
    status = get_mpv_status()
    print(json.dumps(status))

