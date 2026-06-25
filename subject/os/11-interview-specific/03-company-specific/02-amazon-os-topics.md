# Amazon — OS Topics Interview Guide

## Amazon's OS & Infrastructure
- **Amazon Linux:** customized Red Hat-based distribution (optimized for AWS)
- **Nitro System:** hypervisor + dedicated hardware (KVM-based)
- **Firecracker:** microVM for AWS Lambda & Fargate

## Nitro Hypervisor
- **KVM-based** but offloads virtualization to dedicated hardware
- **Nitro cards:** VPC networking, EBS storage, NVMe, GPU
- **No host OS overhead:** bare-metal-like performance
- **Bare-metal instances:** direct hardware access (no hypervisor)

## Firecracker MicroVM
- **Purpose:** serverless (Lambda, Fargate) — lightweight but secure
- Each microVM: shared kernel (Linux), ~5MB memory overhead, <125ms boot
- **Security:** KVM-based isolation (stronger than containers)
- **interface:** vsock (VM-to-host), virtio-net/virtio-blk
- **Limits:** 1 vCPU per microVM, up to 32GB RAM

## Storage Systems (OS Perspective)
| Service | Technology | OS Relevance |
|---------|-----------|--------------|
| **EBS** | Replicated block storage (network-attached) | NVMe interface, dm-multipath |
| **S3** | Object storage (HTTP-based) | File system ≠ object store |
| **EFS** | NFS-based file system | NFSv4, POSIX semantics |
| **Instance Store** | Local NVMe SSD | Ephemeral, fast I/O |

## Performance Optimization Topics
- **NVMe:** multiple queues (per-core queue pairs), no legacy overhead
- **EBS optimization:** ENA (Elastic Network Adapter), NVMe reservation
- **Huge pages:** reduce TLB misses (2MB/1GB pages)
- **NUMA pinning:** keep processes on same socket (avoid remote memory)

## Lambda Execution Environment
- Firecracker microVM per invocation (or reused for ~15 min)
- `/tmp` storage 512MB–10GB (ephemeral)
- **Cold start:** ~100–500ms (reduced via **SnapStart** — snapshot + resume)
- **SnapStart:** Firecracker snapshot of pre-initialized VM

## Distributed Systems at Amazon
- **DynamoDB:** distributed KV store (SSD-backed, consistent hashing)
- **Consistency:** eventual (eventually consistent reads) vs strong (consistent reads)
- **Replication:** Multi-AZ synchronous replication
- **Leader election:** Paxos-based (or MultiPaxos)

## Interview Tips
- *"Firecracker microVMs combine container speed with VM security (KVM isolation)"*
- *"Nitro offloads virtualization to hardware — no host OS overhead"*
- *"EBS: network-attached block storage — know NVMe and ENA for performance"*
- *"Amazon Linux 2023: minimal, optimized for AWS, uses DNF"*
