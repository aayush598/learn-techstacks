# Concurrency vs Parallelism

## Core Definitions
- **Concurrency:** dealing with **many things at once** (interleaved execution)
  - Multiple tasks **in progress** (logical simultaneity)
  - Single core can do it (time-slicing)
- **Parallelism:** doing **many things at once** (simultaneous execution)
  - Multiple tasks **running simultaneously** (physical simultaneity)
  - Requires multi-core / multi-processor

## Key Distinction (Rob Pike)
| | Concurrency | Parallelism |
|---|-------------|-------------|
| **Focus** | Structure / design | Execution |
| **Mechanism** | Interleaving / multiplexing | Simultaneous processing |
| **Hardware needed** | One core suffices | Multiple cores required |
| **Goal** | Manage complexity | Speed up computation |
| **Analogy** | Chess grandmaster playing 50 games (one at a time) | 50 grandmasters each playing one game |

## Relationship
- **Concurrency enables parallelism** (well-structured concurrent tasks are easier to parallelize)
- **Parallelism ≠ Concurrency** (you can have concurrency without parallelism)
- **Concurrency is about composition** — structuring programs as independently executing tasks
- **Parallelism is about efficiency** — using hardware resources

## Examples
- **Single-core:** multiple processes time-shared → concurrent, not parallel
- **Multi-core:** multiple threads on different cores → concurrent AND parallel
- **Node.js event loop:** concurrent (async), but not parallel (single thread)
- **Go runtime:** goroutines are concurrent; they run parallel if GOMAXPROCS > 1

## Programming Models

| Model | Concurrency | Parallelism | Example |
|-------|-------------|-------------|---------|
| **Async/await** | Yes | No (single thread) | JS, Python asyncio |
| **Goroutines** | Yes | Yes (if available) | Go |
| **Thread pools** | Yes | Yes | Java Executors |
| **Actors** | Yes | Yes | Erlang, Akka |
| **SIMD** | No | Yes (data parallel) | AVX, CUDA |

## Interview Questions Twist
- *"Can concurrent code be parallel? Yes — on multi-core"*
- *"Can parallel code be non-concurrent? Yes — SIMD instructions (same op, different data)"*
- *"Goroutines are concurrent by design, parallel when GOMAXPROCS > 1"*

## Amdahl's Law Reminder
- Parallel portions benefit from parallelism
- **Serial portion** (by definition concurrent but not parallelizable) limits speedup
- Concurrency helps structure the serial portion; parallelism helps the parallel portion

## Interview Tip
- *"Concurrency is about dealing with lots of things at once; parallelism is about doing lots of things at once"* — Rob Pike
- *"You can have concurrency without parallelism (single-core time-sharing)"*
- *"You can have parallelism without concurrency (SIMD — all cores do the same thing)"*
