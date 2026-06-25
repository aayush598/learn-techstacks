# Actor Model

## Core Concepts
- **Actor** = fundamental unit of computation (has state, behavior, mailbox)
- Communication via **asynchronous messages** (no shared state)
- Each actor processes messages **sequentially** (one at a time)
- Actors can: create actors, send messages, change behavior
- **No locks, no shared memory, no race conditions**

## Actor Properties
- **Encapsulation:** actors own their state (no external access)
- **Location transparency:** actors addressed by ID, not memory address
- **Fault tolerance:** "let it crash" → supervisor restarts actors
- **Elasticity:** actors are lightweight (millions per JVM/Erlang VM)

## Implementations

| Framework | Language | Notable Features |
|-----------|----------|-----------------|
| **Erlang OTP** | Erlang/Elixir | BEAM VM, hot code reload, process ~300 bytes |
| **Akka** | Java/Scala | Typed actors, cluster sharding, Akka Streams |
| **ProtoActor** | Go/C# | Virtual actors, cluster support |
| **Orleans** | C# | Virtual actors (grains), Azure-powered |
| **Pony** | Pony | Reference capabilities (compile-time race freedom) |

## Supervision Trees
- **Supervisor** monitors child actors, decides restart strategy
- Strategies: **one-for-one**, **one-for-all**, **rest-for-one**
- Hierarchical: root supervisor → workers → sub-supervisors
- **Fault isolation:** crash in one actor doesn't affect peers

## Actor Model vs Thread-Based Concurrency

| Aspect | Actor Model | Shared Memory + Locks |
|--------|-------------|----------------------|
| State | per-actor, isolated | shared mutable state |
| Communication | async messages | shared memory |
| Synchronization | none needed | mutexes, semaphores, CVs |
| Scalability | excellent | complex at scale |
| Debugging | message tracing | deadlock/race hunting |
| Hardware | single or multi-core | same |

## Use Cases
- **Telecom** (Erlang — Ericsson AXD301: 99.9999999% uptime)
- **Gaming** (server-side concurrency per player/session)
- **Distributed systems** (event sourcing, CQRS)
- **IoT** (device actors, state isolation)
- **WhatsApp** (2M+ connections per node on Erlang)

## Interview Tips
- *"Actors solve concurrency by eliminating shared state"*
- Contrast with threads: *"Threads share memory and synchronize; actors no-share and message"*
- Know **supervision trees** for fault tolerance
- Erlang's BEAM uses **preemptive scheduling** of actor processes
