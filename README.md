<div align="center">

# VertexHandshake

### The Stateful P2P Handshake — Warm-Up Track

**[Vertex Swarm Challenge 2026](https://dorahacks.io/hackathon/global-vertex-swarm-challenge)**

[![Vertex SDK](https://img.shields.io/badge/Tashi_Vertex-P2P_Consensus-38bdf8?style=flat-square)](https://docs.tashi.network/)
[![Zero Cloud](https://img.shields.io/badge/Cloud_Calls-ZERO-ef4444?style=flat-square)](/)

**Two nodes. One mesh. Zero cloud.**

[Live Demo](https://vertexhandshake.vercel.app)

</div>

---

## What This Proves

The Warm-Up Track requires a foundational P2P connection: **two agents discover each other, sync state, and recover from a failure.** VertexHandshake demonstrates all three.

## The Three Phases

### 1. Discovery & Handshake
Two nodes broadcast gossip events via Vertex's gossip-about-gossip protocol. No registration server — peers find each other through the DAG. Once both sides confirm, a bidirectional P2P link is established.

### 2. State Synchronization  
Nodes continuously sync shared state (counter value, temperature readings) through Vertex consensus events. Both nodes maintain identical state — verified through virtual voting on the DAG.

### 3. Failure & Recovery
Node-B is killed (simulating network failure or crash). Node-A detects the loss via missing gossip events, enters solo mode, and buffers state changes. When Node-B comes back online, it re-discovers Node-A, re-establishes the handshake, and re-syncs all buffered state. Full consensus restored.

## Run It

### Live Demo
👉 **[vertexhandshake.vercel.app](https://vertexhandshake.vercel.app)**

### Local
```bash
git clone https://github.com/HuydZzz/vertex-handshake.git
cd vertex-handshake
# Just open public/index.html in a browser — no backend needed
```

## Dashboard

The real-time dashboard shows:
- **Visual mesh** — animated P2P connection with data packets flowing between nodes
- **Node cards** — status, counter, temperature, latency, sync count
- **Mesh stats** — peers online, average latency, total syncs, cloud calls (always 0)
- **Event log** — timestamped log of discovery, sync, failure, and recovery events

### Controls

| Button | Action |
|--------|--------|
| **KILL NODE-B** | Simulate node failure — watch discovery → solo mode → recovery |
| **↻ RESET** | Restart from boot |

## Vertex Features Used

| Primitive | Usage |
|-----------|-------|
| Gossip-about-gossip | Peer discovery |
| DAG events | State sync messages |
| Virtual voting | Consensus on shared state |
| Fault detection | Missing gossip → peer loss |

## Project Structure

```
vertex-handshake/
├── public/
│   └── index.html    # Standalone demo (no backend)
├── README.md
├── vercel.json
└── LICENSE
```

---

<div align="center">

*Built for the Vertex Swarm Challenge 2026 Warm-Up Track*

⬡

</div>
