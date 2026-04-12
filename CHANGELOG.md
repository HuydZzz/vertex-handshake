# Changelog

All notable changes to VertexHandshake will be documented in this file.

## [0.2.0] - 2026-04-12

### Added
- Logo embedded directly in HTML for reliable rendering
- Vercel deployment configuration
- MIT License

### Improved
- Node cards show real-time counter, temperature, latency, and sync count
- Event log with color-coded event types (mesh, sync, fail, recover)
- Mesh stats panel displaying peers, latency, syncs, and cloud calls

## [0.1.0] - 2026-04-11

### Added
- Two-node P2P handshake simulation
- Gossip-based peer discovery — no registration server
- State synchronization with shared counter and temperature values
- Node failure simulation with KILL NODE-B button
- Automatic fault detection via missing gossip events
- Solo mode with state buffering during partition
- Re-discovery and full state recovery on node rejoin
- Real-time dashboard with animated mesh visualization
- Data packet animation between connected peers
- Reset functionality for demo replay

### Technical
- Vertex gossip-about-gossip protocol for peer discovery
- Virtual voting on DAG for state consensus
- Fault detection via gossip gap analysis
- Zero cloud dependency — fully local P2P coordination
