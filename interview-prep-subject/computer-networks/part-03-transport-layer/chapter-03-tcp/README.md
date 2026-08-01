# TCP — Transmission Control Protocol

> **TL;DR**: The reliable, ordered, connection-oriented transport that powers 80%+ of Internet bytes — three-way handshake, sequence/ACK numbers, flow control (rwnd), congestion control (cwnd), retransmission, and a state machine — all in ~10 pages of RFC 793 (now 9293), running in the kernel of every host on the planet.

## Chapter Roadmap
- **Segment anatomy**: TCP header, sequence numbers, window scaling, options, and how one segment carries flags.
- **The handshake**: 3-way SYN/SYN-ACK/ACK, sequence synchronization, and why it costs one RTT.
- **Teardown**: 4-way FIN/ACK exchange, TIME_WAIT, and why it lasts 2×MSL.
- **Flow control**: sliding window, rwnd, zero-window, and window scaling (why throughput hits 16 GB/s+).
- **Congestion control**: slow start, congestion avoidance, Reno/NewReno/CUBIC, BBR — the math behind TCP's fairness.
- **Reliability mechanics**: timeouts, fast retransmit, selective ACK (SACK), duplicate ACKs, timers.
- **The state machine + extra algorithms**: TCP finite state machine, Nagle, delayed ACK, keepalive, and the gotchas they cause.

## Section Files
- `section-01-tcp-segment-structure.md` — header, sequence numbers, window scaling, options.
- `section-02-tcp-three-way-handshake.md` — establishment, SYN cookies, RTT measurement.
- `section-03-tcp-connection-termination-four-way.md` — FIN/ACK, TIME_WAIT, half-close, RST.
- `section-04-tcp-flow-control-sliding-window.md` — rwnd, sliding window, zero-window, scaling.
- `section-05-tcp-congestion-control.md` — slow start, AIMD, Reno/NewReno/CUBIC/BBR, bufferbloat.
- `section-06-tcp-reliability-retransmission-and-timers.md` — RTO, Karn's, fast retransmit, SACK, DUPACKs.
- `section-07-tcp-state-machine-and-nagle-etc.md` — FSM, Nagle, delayed ACK, keepalive, TFO.

## Interview Q&A Preview
- **"Why does TCP need a 3-way handshake?"** → To synchronize *sequence numbers* (each side picks a random ISN and confirms the peer's) and exchange the initial rwnd/options — two one-way channels need two round trips of state, compressed to 3 segments.
- **"Why 4-way teardown?"** → Each direction closes independently (half-close): 2× (FIN + ACK). The active closer waits 2×MSL in TIME_WAIT so late segments can't corrupt a new connection reusing the tuple.
- **"How does TCP achieve gigabit+ throughput?"** → Window scaling + large buffers: throughput ≈ window/RTT. A 16 GB window at 10 ms RTT ≈ 13 Tbps potential; cwnd grows by slow start/AIMD.
- **"What's the difference between flow and congestion control?"** → Flow control = don't overwhelm the *receiver* (rwnd, receiver buffer); congestion control = don't overwhelm the *network* (cwnd, sender side). Two independent windows, one per connection.

## Key Diagrams to Recreate
1. **TCP segment header**: src(16) dst(16) seq(32) ack(32) dataoff+flags(16) window(16) cksum(16) urg(16) + options.
2. **Handshake**: SYN(seq=x) → SYN+ACK(seq=y, ack=x+1) → ACK(seq=x+1, ack=y+1); 1 RTT.
3. **Teardown**: FIN(x) → ACK(x+1) → FIN(y) → ACK(y+1); 4 segments, 2×MSL TIME_WAIT.
4. **Windows**: sender (cwnd: ssthresh, slow start, AIMD) × receiver (rwnd: advertised) → effective = min.
5. **Sawtooth of cwnd over time**: exponential ramp (slow start) → linear (AIMD) → halve on loss (Reno).
