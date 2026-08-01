# RAID Levels

> **TL;DR**: RAID combines multiple disks for **performance** (striping), **reliability** (mirroring/parity), or both. RAID 0 stripes with no redundancy; RAID 1 mirrors; RAID 5/6 stripe + distributed parity (tolerates 1/2 failures); RAID 10 mirrors striped sets. It's redundancy — **not backup**.

## 1. Why Does This Exist?
A single disk has a MTBF (mean time between failures) of ~1M–3M hours and a finite bandwidth. If you want more capacity, more speed, or protection against a disk dying mid-service, you can't wait for the manufacturer. RAID (Redundant Array of Independent/Inexpensive Disks) lets software or a controller treat many physical disks as one logical volume, spreading reads/writes across spindles (bandwidth ↑) and adding redundancy (MTBF of the array ≫ MTBF of one disk). It exists because at some point one disk is a bottleneck and a single point of failure.

## 2. How Does It Work?
- **RAID 0 (striping)**: data is split into stripes (chunks, e.g., 64 KB) spread round-robin across all disks. No parity, no mirror. Any disk failure = total data loss. Usable = n × size. Best performance, zero redundancy.
- **RAID 1 (mirroring)**: every block written to two disks (or mirrored pairs). Read can go to either (2× read throughput), write is 2×. Tolerates ≥1 disk per pair. Usable = n/2 × size.
- **RAID 5 (striped + distributed parity)**: one parity block per stripe, distributed across all disks. Tolerates 1 disk failure. Usable = (n−1) × size. Every write touches all disks (the read-modify-write for parity) → write penalty.
- **RAID 6 (double parity)**: two parity blocks per stripe. Tolerates 2 failures. Usable = (n−2) × size. Higher write penalty.
- **RAID 10 (1+0, mirrored stripes)**: mirror pairs striped. Tolerates one disk per mirror pair. Usable = n/2. Best reliability+performance, expensive.
- Other nestings: RAID 01 (striped mirrors — poor failure tolerance), RAID 50, 60 (parity over stripe), RAID 0+... all are compositions.
- **Details**: hot spare (idle disk auto-rebuilds after failure), scrubbing (background parity check), rebuild cost (reading all surviving disks), write hole, and the "RAID 5 of SSDs" degradation during rebuild.

## 3. When Is It Used?
- **RAID 0**: scratch/cache/temp, or where data is already replicated elsewhere (log aggregation).
- **RAID 1**: OS/system disks, boot volumes, databases wanting read amplification cheaply.
- **RAID 5**: general file servers — capacity + single-disk tolerance.
- **RAID 6**: large disks (4TB+), long rebuild times, enterprises needing 2-disk tolerance (Amazon/big-data defaults).
- **RAID 10**: OLTP databases (PostgreSQL/MySQL) needing both IOPS and safety.
- **Software RAID** (`mdadm` Linux) vs **hardware RAID** (controller cards, BBU) vs **storage pools** (ZFS RAIDZ, btrfs raid levels, hardware HPE SmartArray / LSI MegaRAID).

## 4. Why Wasn't Another Approach Chosen?
- **No RAID** — one disk, one failure point; rejected for critical workloads.
- **RAID 1 everywhere** — safest but 50% capacity; too expensive at scale.
- **RAID 4 (dedicated parity disk)** — parity disk becomes a bottleneck; replaced by distributed parity RAID 5.
- **RAID 5 on huge disks** — rebuild window grows (read 4–16 TB); URE (unrecoverable read error) probability during rebuild makes RAID 6 the modern choice.
- **RAID 2 (bit-level ECC)** — obsolete; controllers do ECC internally.
- **ZFS RAIDZ / btrfs raid** — filesystem-level RAID with checksums; software approach chosen where "bitrot" detection matters.
- **Erasure coding** (Reed-Solomon) — beyond RAID levels for distributed storage (Ceph, Hadoop) — more flexible but complex.

## 5. Intuition
Think of it as a **stunt double team**: RAID 0 is the "one person does everything fast" — no backup. RAID 1 is "two people do the same job" — safe but 2× the headcount. RAID 5 is "team of n, where one of them is the helper that can fill in for anyone" — rotating helper duty so nobody is a bottleneck. RAID 10 is "pairs of identical twins, working in parallel" — each pair is interchangeable, and all pairs work simultaneously. The cost of a helper (parity) is a write penalty: every write is a small update choreography with the helper.

## 6. Real-World Analogy
**School group projects with a shared Google doc**: RAID 0 = each person writes their own sections directly, no backup (one hard drive crash = project gone). RAID 1 = two people keep identical copies and sync (safe, double the effort). RAID 5 = the group keeps a "notes-taker" who records a summary of everyone's edits; if anyone is absent, the notes + other people's work reconstruct what was missing. The notes-taker (parity) costs a bit of extra write effort on every edit but recovers anyone. RAID 10 = pairs of people assigned identical sections, all pairs working in parallel.

## 7. Formal Definition
A RAID level is a data-layout + redundancy scheme across a disk set: **RAID 0**: `data_i = stripe(chunk_i mod n)`, no redundancy. **RAID 1**: each logical block replicated to ≥2 member disks. **RAID 5**: per stripe of n blocks, one parity block `P = D1 ⊕ D2 ⊕ … ⊕ D(n−1)`, distributed round-robin across disks; any single member lost is reconstructed as `Di = P ⊕ D1 ⊕ … ⊕ D(n−1)\{Di}`. **RAID 6**: two independent parity blocks (Reed-Solomon or diagonal), tolerates two losses. **RAID 10**: RAID 0 of RAID 1 pairs. Usable capacity: `(n − r) × S` where r = redundancy (0,1,2) and S = per-disk size. Read/write throughput scales with parallel members; parity writes incur a read-modify-write penalty of `(n−2)/n`... (write amplification ≈ ×3 for RAID 5 single-block writes).

## 8. Example
3 disks, 1 TB each, stripe chunk 64 KB. File `F` = 256 KB (4 chunks):
- **RAID 0**: chunks D0→disk1, D1→disk2, D2→disk3, D3→disk1. Usable 3 TB. Read 3 disks in parallel. Any disk fails → F gone.
- **RAID 1** (3 disks as mirror+mirror... typically pairs): 2 disks mirror A, 3rd unused or part of another pair; usable 1.5 TB; reads can split.
- **RAID 5**: stripes of 3 data + 1 parity across... with 3 disks, each stripe has 2 data blocks + 1 parity block: D0 D1 P0 / P1 D2 D3... Usable 2 TB; tolerates one disk failure; a single 4 KB write forces read D0, read P0, write D0', write P0' (4 I/Os).
- **RAID 6** (4 disks): usable 2 TB; two parity blocks per stripe; tolerates two failures.
- **RAID 10** (4 disks, 2 mirror pairs): usable 2 TB; writes to both mirrors of a pair in parallel; tolerates 1 disk per pair (up to 2 total if in different pairs).

## 9. Internal Working
1. Controller/SW splits a logical block stream into chunks (strip size).
2. Writes: data chunks to member disks; parity computed (XOR) and written to the parity member (RAID 5/6) — typically via **read-modify-write**: read old data + old parity, compute new parity, write data + parity.
3. Reads: single disk (random) or all disks (sequential/striped).
4. Failure: drive errors out → array degrades; hot spare activates → rebuild reads all surviving disks and reconstructs; if second failure before rebuild completes → data loss (RAID 5).
5. Scrubbing: periodically read all + verify parity (detect silent bit-rot; ZFS adds checksums).
6. Linux `md` (mdadm), hardware RAID controllers with BBU (battery-backed write cache), ZFS RAIDZ/`raidz2`.

## 10. Time Complexity
- Read (RAID 0/5/10): O(1) per block — parallel striping, scales ~linearly with disks for sequential.
- Write (RAID 5 single block): read-modify-write = 2 reads + 2 writes (4 I/Os); the "small write penalty" — write amplification ~×2–3 vs raw.
- Rebuild (RAID 5, one disk lost): must read ~(n−1) × S — rebuild time scales with disk size (a 16 TB disk can take a day).
- RAID 6: two parity computations per write; write penalty higher than RAID 5.
- XOR parity: O(m) per block (m = number of data blocks), constant factor cheap (hardware XOR engines).
- Failure tolerance: RAID 5 = 1, RAID 6 = 2, RAID 10 = 1 per mirror (min), RAID 0 = 0.

## 11. Advantages
- **RAID 0**: full capacity, max throughput, zero overhead.
- **RAID 1**: simple, great reads, instant recovery (mirror), tolerates 1+.
- **RAID 5**: capacity-efficient redundancy ((n−1)/n).
- **RAID 6**: survives 2 failures and rebuild-era UREs.
- **RAID 10**: performance + reliability for OLTP; reads hit either mirror; rebuild is a copy (cheap).
- **Hot spares + scrubbing**: automatic failure recovery and corruption detection.

## 12. Disadvantages
- **RAID 0**: zero protection — one disk = total loss.
- **RAID 1**: 50% capacity cost.
- **RAID 5**: write penalty (read-modify-write); catastrophic risk on large disks during rebuild; rebuild *performance* degradation (all surviving disks busy).
- **RAID 6**: higher write penalty, more compute.
- **RAID 10**: expensive (50% usable), many disks needed.
- **All**: RAID ≠ backup (delete/corruption/lambda/ransomware still destroy data); rebuild relies on surviving disks not failing; controller/`md` complexity.
- Parity algorithms add CPU cost (XOR/Reed-Solomon).

## 13. Interview Questions
1. **Q: What is RAID?** A: Redundant Array of Independent Disks — combining multiple disks into one logical volume for performance (striping) and/or redundancy (mirroring, parity).
2. **Q: RAID 0?** A: Striping only — chunks spread across disks, full capacity (n×S), max throughput, but zero redundancy: any disk failure loses everything.
3. **Q: RAID 1?** A: Mirroring — every block on ≥2 disks; reads can use either; 50% usable; tolerates a disk failing; instant rebuild (copy from the twin).
4. **Q: RAID 5?** A: Striped + distributed parity — one parity block per stripe across all disks; usable (n−1)×S; tolerates one failure; write penalty from read-modify-write.
5. **Q: RAID 6?** A: Double distributed parity — tolerates two failures; usable (n−2)×S; higher write penalty; the choice for big disks with long rebuilds.
6. **Q: RAID 10 vs RAID 5? (Hot)** A: RAID 10 = mirrored striped pairs: better write performance (no parity penalty), faster rebuild (copy), tolerates a disk per mirror, but 50% capacity. RAID 5 = cheaper capacity, one-failure tolerance, but write penalty + slow rebuild + risk on large disks.
7. **Q: Is RAID a backup? (Tricky)** A: No. RAID protects against *disk failure*, not deletion, corruption, ransomware, or site loss — you still need backups. "RAID is not a backup" is the standard interview punchline.
8. **Q: What is the RAID 5 write penalty?** A: A single small write becomes read-old-data + read-old-parity + write-data + write-parity (read-modify-write, ~4 I/Os), plus the extra parity transfer — write amplification ~×2–3.
9. **Q: What is a hot spare?** A: An idle disk in the array that automatically rebuilds data onto itself when a member fails — reduces the failure window.
10. **Q: Why is RAID 5 risky on 16 TB disks?** A: Rebuild must read all surviving disks (huge), and during that window a second URE/failure is more likely → RAID 6 recommended.
11. **Q: What is scrubbing?** A: Periodically reading all blocks and verifying parity (or checksums in ZFS) to catch silent corruption before it's needed for rebuild.
12. **Q: RAID in ZFS?** A: RAIDZ/raidz2/raidz3 — filesystem-level RAID with checksums and copy-on-write; avoids the "write hole" and detects bit-rot, at the cost of controller-flexibility.

## 14. Follow-Up Questions
1. **Q: Software vs hardware RAID?** A: Software (mdadm/ZFS) uses CPU, flexible, no vendor lock; hardware (controller) has its own CPU + battery-backed cache (BBU) for crash-safe writes; modern systems often use software for cost/complexity.
2. **Q: What is the write hole?** A: In parity RAID, a crash mid-write can leave data + parity inconsistent; full parity re-computation is needed on recovery (ZFS RAIDZ avoids via copy-on-write).
3. **Q: What is erasure coding?** A: Generalization beyond RAID (e.g., Reed-Solomon (k, m) with m parity) used in distributed storage (Ceph, HDFS) — more flexible than fixed RAID levels.
4. **Q: RAID 5 rebuild impact?** A: Array runs degraded (all surviving disks busy reconstructing), read performance drops, exposure to second failure rises; hot spares + careful disk sizing mitigate.

## 15. Coding Example
```c
// Software RAID 5 parity (XOR) for one stripe of 3 data blocks
#include <stdint.h>
#include <stdio.h>

// compute parity for a stripe: P = D0 ^ D1 ^ D2
uint64_t raid5_parity(uint64_t d0, uint64_t d1, uint64_t d2) {
    return d0 ^ d1 ^ d2;
}

// reconstruct a missing block given parity and the other blocks
int raid5_reconstruct(uint64_t *out, int missing_idx, uint64_t p,
                      uint64_t *d, int n) {
    uint64_t acc = p;                 // start from parity
    for (int i = 0; i < n; i++)
        if (i != missing_idx) acc ^= d[i];   // XOR out the present blocks
    *out = acc;                        // result = missing block
    return 0;
}

int main(void) {
    uint64_t d0 = 0x0F0F, d1 = 0xAAAA, d2 = 0x1234;
    uint64_t p  = raid5_parity(d0, d1, d2);
    printf("parity = 0x%04llX\n", (unsigned long long)p);

    uint64_t recovered;
    raid5_reconstruct(&recovered, 1, p, (uint64_t[]){d0, d1, d2}, 3);
    printf("recovered d1 = 0x%04llX (expected 0xAAAA)\n",
           (unsigned long long)recovered);
    return 0;
}
```

## 16. Industry Usage
- **mdadm** (Linux software RAID); **ZFS** (RAIDZ); **btrfs** raid1/raid5/raid6 (raid1c3).
- **Hardware controllers**: LSI/Broadcom MegaRAID, HPE Smart Array, Dell PERC — with BBU/flash-backed cache.
- **Cloud storage**: EBS volumes use distributed systems (not classic RAID), but concepts persist (erasure coding in S3/EBS-replicated).
- **Databases**: PostgreSQL/MySQL on RAID 10 (OLTP) or RAID 6 (warehousing).
- **Big data**: Hadoop HDFS default replication (3×) instead of RAID — replication is "RAID for the distributed era."

## 17. References
- Silberschatz, *Operating System Concepts*, Ch. 10.7 "RAID Structure".
- Patterson, Gibson, Katz (1988), "A Case for Redundant Arrays of Inexpensive Disks (RAID)" — the original paper.
- Tanenbaum, *Modern Operating Systems*, Ch. 5.5 (RAID).
- `man mdadm`; Linux `Documentation/admin-guide/md.rst`.
- ZFS documentation: RAIDZ and reconstruction (`raidz`).

## 18. Cheat Sheet
- RAID 0: strip, n×S, 0 tolerance, max perf.
- RAID 1: mirror, n/2×S, 1 per pair, cheap rebuild.
- RAID 5: distributed parity, (n−1)×S, 1 failure, write penalty.
- RAID 6: double parity, (n−2)×S, 2 failures, higher penalty.
- RAID 10: mirrored strips, n/2×S, 1 per pair, OLTP choice.
- Write penalty: RAID 5 single-block = read-modify-write (4 I/Os).
- Hot spare + scrubbing mitigate failure windows.
- RAID ≠ backup.

## 19. Quiz
1. RAID 0 tolerates how many failures? a) 0 b) 1 c) 2 d) n → **a**
2. RAID 5 usable capacity for 4×2TB disks? a) 8TB b) 6TB c) 4TB d) 2TB → **b**
3. The RAID 5 write penalty comes from? a) mirroring b) read-modify-write for parity c) stripping d) scrubbing → **b**
4. Best for OLTP databases? a) RAID 0 b) RAID 1 c) RAID 5 d) RAID 10 → **d**
5. RAID 6 tolerates? a) 0 b) 1 c) 2 d) 3 → **c**
6. RAID is a backup? a) yes b) no c) only RAID 1 d) only with hot spare → **b**

## 20. Flashcards
- **Q: RAID 0?** → **A:** Striping, full capacity, zero redundancy.
- **Q: RAID 1?** → **A:** Mirroring, 50% usable, tolerates failure.
- **Q: RAID 5?** → **A:** Distributed parity, (n−1) usable, 1 failure.
- **Q: RAID 6?** → **A:** Double parity, (n−2) usable, 2 failures.
- **Q: RAID 10?** → **A:** Mirrored stripes; OLTP favorite.
- **Q: RAID ≠ ?** → **A:** Backup.

## 21. Revision
RAID combines disks for speed, safety, or both. RAID 0 = pure striping (no protection); RAID 1 = mirroring (safe, half capacity); RAID 5/6 = striped + distributed parity (tolerate 1/2 failures, write penalty); RAID 10 = mirrored stripes (best for OLTP). The fundamental trade-off is usable capacity vs redundancy vs write cost — and the interview line everyone wants to hear: **RAID is redundancy, not backup**. Rebuild risk on large disks and the small-write read-modify-write penalty are the two details that separate a good answer from a great one.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is RAID and why?" | 1 Why / 13 Q1 |
| "RAID 0/1/5/6/10 comparison" | 8 Example / 13 Q2–6 |
| "RAID 10 vs RAID 5 for a DB" | 13 Q6 / 16 Industry |
| "Is RAID a backup?" | 13 Q7 / 12 Disadvantages |
| "RAID 5 write penalty?" | 13 Q8 / 9 Internal |
| "Why RAID 6 for big disks?" | 13 Q10 / 3 When |
| "Hot spare / scrubbing?" | 13 Q9 / 13 Q11 |
