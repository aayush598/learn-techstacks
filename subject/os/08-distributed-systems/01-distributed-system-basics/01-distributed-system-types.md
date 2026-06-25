# Distributed System Types

## Definition
- Collection of **independent computers** connected by network
- Appears to user as a **single coherent system**
- Each node has its own memory and runs its own OS

## Advantages
- **Resource sharing**: data, peripherals, storage
- **Computation speed**: parallelism, load balancing
- **Reliability**: redundancy, no single point of failure
- **Scalability**: add nodes horizontally
- **Cost-effective**: commodity hardware

## Architectural Styles
| Style | Description | Examples |
|-------|-------------|----------|
| **Client-Server** | Servers provide services, clients consume | Web apps, databases |
| **Peer-to-Peer** | All nodes equal, decentralized | BitTorrent, Blockchain |
| **Three-tier** | Presentation, logic, data layers separated | Web apps (UI → API → DB) |
| **n-tier** | Multiple specialized tiers | Microservices |
| **Master-Slave** | One coordinator, workers replicate | HDFS, MySQL replication |

## Network Types
| Type | Latency | Range |
|------|---------|-------|
| **LAN** | ~1 ms | Building/Campus |
| **WAN** | 10–100 ms | Countries/Continents |
| **MAN** | ~5–10 ms | City |

## Challenges
- **Partial failure**: some nodes fail while others work (hardest problem)
- **Latency**: network delays unpredictable
- **Concurrency**: race conditions, deadlocks across nodes
- **Security**: more attack surface, trust between nodes
- **Consistency**: keeping replicas in sync (CAP theorem)
- **Clock sync**: no global clock, need logical clocks
