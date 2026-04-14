"""
VertexHandshake — P2P Handshake Agent with FoxMQ (Tashi Vertex)
Two agents discover each other, sync state, and recover from failure.
All messages are consensus-ordered by Vertex via FoxMQ broker.
"""

import json
import time
import random
import argparse
import paho.mqtt.client as mqtt

TOPIC_HELLO = "swarm/hello"
TOPIC_STATE = "swarm/state"


class HandshakeAgent:
    def __init__(self, agent_id, host="127.0.0.1", port=1883, username=None, password=None):
        self.agent_id = agent_id
        self.host = host
        self.port = port

        # Shared state
        self.counter = 0
        self.temp = 20 + random.random() * 5
        self.sync_count = 0

        # Peer tracking
        self.peers = {}
        self.connected = False
        self.running = True

        # MQTT
        self.client = mqtt.Client(
            client_id=agent_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        if username:
            self.client.username_pw_set(username, password or "")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print(f"[{self.agent_id}] ✓ Connected to FoxMQ (Vertex consensus broker)")
            client.subscribe(TOPIC_HELLO)
            client.subscribe(TOPIC_STATE)

            # Publish HELLO
            hello = {
                "type": "HELLO",
                "agent_id": self.agent_id,
                "timestamp": time.time()
            }
            client.publish(TOPIC_HELLO, json.dumps(hello), qos=1)
            print(f"[{self.agent_id}] → HELLO published to {TOPIC_HELLO}")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        self.connected = False
        print(f"[{self.agent_id}] ⚠ Disconnected (rc={rc})")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except:
            return

        sender = data.get("agent_id")
        if sender == self.agent_id:
            return

        now = time.time()

        if msg.topic == TOPIC_HELLO:
            if sender not in self.peers:
                print(f"[{self.agent_id}] [MESH] ✓ Discovered peer: {sender}")
            self.peers[sender] = {"last_seen": now, "state": data}

        elif msg.topic == TOPIC_STATE:
            self.peers[sender] = {"last_seen": now, "state": data}
            # Sync state from peer
            peer_counter = data.get("counter", 0)
            peer_temp = data.get("temp", 0)
            if peer_counter > self.counter:
                self.counter = peer_counter
                self.temp = peer_temp
                self.sync_count += 1
                print(f"[{self.agent_id}] [SYNC] ← Synced from {sender}: counter={self.counter} temp={self.temp:.1f}°C")

    def check_stale(self):
        now = time.time()
        for pid in list(self.peers.keys()):
            if now - self.peers[pid]["last_seen"] > 10:
                print(f"[{self.agent_id}] [STALE] ⚠ Peer {pid} marked stale (>10s)")
                del self.peers[pid]

    def run(self):
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()

        for _ in range(50):
            if self.connected:
                break
            time.sleep(0.1)

        if not self.connected:
            print(f"[{self.agent_id}] ✗ Could not connect")
            return

        print(f"[{self.agent_id}] Running... (Ctrl+C to stop)")
        try:
            while self.running:
                # Increment state
                self.counter += 1
                self.temp = 20 + random.random() * 10

                # Publish heartbeat
                state = {
                    "type": "HEARTBEAT",
                    "agent_id": self.agent_id,
                    "timestamp": time.time(),
                    "counter": self.counter,
                    "temp": round(self.temp, 1),
                    "sync_count": self.sync_count,
                    "peers": list(self.peers.keys())
                }
                self.client.publish(TOPIC_STATE, json.dumps(state), qos=1)

                # Check stale
                self.check_stale()

                # Display
                peer_names = list(self.peers.keys())
                print(f"[{self.agent_id}] counter={self.counter} temp={self.temp:.1f}°C "
                      f"syncs={self.sync_count} peers={peer_names}")

                time.sleep(2)
        except KeyboardInterrupt:
            print(f"\n[{self.agent_id}] Stopped.")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VertexHandshake Agent (FoxMQ)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", default="")
    parser.add_argument("--agent-id", required=True)
    args = parser.parse_args()

    agent = HandshakeAgent(
        agent_id=args.agent_id,
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )
    agent.run()
