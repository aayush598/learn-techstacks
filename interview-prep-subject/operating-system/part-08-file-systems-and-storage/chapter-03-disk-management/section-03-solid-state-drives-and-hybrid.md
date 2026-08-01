# Solid State Drives and Hybrid

> **TL;DR**: SSDs use NAND flash with **no moving parts** — no seek or rotational latency, so random I/O is as fast as sequential. But flash can't overwrite in place: blocks must be erased before rewriting, wearing out over time. **Wear leveling**, **TRIM**, and **garbage collection** (GC) are how the FTL manages this; "hybrid" designs tier hot/cold data across HDD and SSD (or Optane).

## 1. Why Does This Exist?
HDDs hit a wall: moving a head takes milliseconds, so random IOPS are ~100 and access is dominated by physics. NAND flash replaces the mechanism with transistors — reads and writes happen in microseconds, random = sequential (no head). But flash introduces a new physics: you can program (write) a cell only after erasing an entire block, and each cell survives only a limited number of program/erase cycles (wear). SSDs and their FTLs (Flash Translation Layers) exist to (a) present a clean block-device interface that abstracts NAND's erase-before-write, and (b) spread wear evenly so the drive doesn't die after one hot block gets hammered. Hybrid designs exist because flash still costs more per byte than spinning disks.

## 2. How Does It Work?
- **NAND types**: SLC (1 bit/cell, ~100K P/E cycles), MLC (2 bits, ~3–10K), TLC (3 bits, ~1–3K), QLC (4 bits, ~500–1K). More bits = cheaper/denser but fewer cycles and slower.
- **Pages vs blocks**: a page (4–16 KB) is the read/write unit; a block (256 pages+) is the erase unit. Writing a page in a block that has data requires: read all valid pages → erase block → write back valid + new (GC).
- **FTL (Flash Translation Layer)**: maps logical block addresses (LBAs) to physical pages; a **logical-to-physical map** in RAM/DRAM. Writes go to a fresh (already-erased) page; the old page's mapping is remapped — this is *out-of-place* update.
- **Wear leveling**: the FTL picks erase victims to keep P/E counts even — *dynamic* (move cold data around) + *static* (also move hot data / relocate cold blocks).
- **TRIM**: when the OS deletes a file, it tells the SSD (ATA TRIM / NVMe deallocate) which LBAs are dead, so GC can skip copying them.
- **Garbage collection**: reclaims blocks with many invalid pages; background GC + foreground (when free space is low → write amplification and latency spikes).
- **Overprovisioning** (spare area ~7–28%): hidden free blocks that keep GC smooth and absorb wear.
- **Hybrid**: HDD+SSD caching (bcache, dm-cache, Fusion drive), NVMe tiering, and Intel Optane (3D XPoint) as a middle tier.

## 3. When Is It Used?
- **Every modern machine**: SSDs are the default; `nvme`, `sata`, `usb` flash.
- **Databases**: PostgreSQL random_page_cost lowered (SSD), or log-write optimization.
- **Cloud/enterprise**: NVMe datacenter drives, 100K+ IOPS; ZFS special vdevs (L2ARC); HDFS tiered storage.
- **Hybrid systems**: hot/cold data tiering (warm tier HDD, hot tier SSD), laptop Fusion drives, cache layers.
- **Boot/OS drives**: cheap + fast; write-heavy temp/cache on HDD.

## 4. Why Wasn't Another Approach Chosen?
- **HDD (rejected for hot tier)**: seek latency + low IOPS; can't serve OLTP random workloads.
- **DRAM storage (rejected)**: volatile — needs batteries/backup; too expensive per GB.
- **Optane/3D XPoint (partially chosen)**: faster than NAND, more durable, but expensive — used as a cache/tier, not the bulk storage.
- **Log-structured FS everywhere (chosen by SSDs implicitly)**: NAND *forces* out-of-place update — that's the FTL's job; the host never sees it.
- **In-place NAND write (impossible)**: flash can't overwrite a page without block erase — hence FTL + GC.
- **No wear leveling (rejected)**: hot blocks would die in days; uniformity is required.

## 5. Intuition
**A whiteboard with limited erasings**: HDDs are like a book where you can flip to any page and edit instantly. NAND is a whiteboard where you can *write* on a page anytime, but to *erase* it you must erase the whole board (block) and it only survives ~10,000 erases before it's worn out. The FTL is the board manager who: always writes on the cleanest section (never erases a section until it must), keeps a map of "what's where," tells you (via TRIM) which sections are no longer needed, and occasionally clears the board in big sweeps (GC). Wear leveling = rotating which sections get erased so the board lasts evenly.

## 6. Real-World Analogy
**A parking garage that only lets you use the top floor for new arrivals**: cars (pages) arrive and park on the top floor (fresh block). When the top floor fills, the garage manager (FTL) has to clear lower floors (blocks) — he checks which spots (pages) still hold useful cars (valid data), moves them up, erases the floor, and parks new arrivals there. To avoid always erasing the same floor (wear), he rotates which floor gets cleared (wear leveling). TRIM = the garage attendant telling him "those spots in the back are abandoned" so he doesn't bother moving those cars during cleanup.

## 7. Formal Definition
A Solid State Drive presents a block-device interface while storing data in NAND flash managed by an **FTL** with: (1) a logical-to-physical address map (page granularity), (2) **out-of-place updates** (write to erased pages, remap), (3) **garbage collection** selecting victim blocks by invalid-page count and reclaiming them, (4) **wear leveling** equalizing program/erase counts across blocks, and (5) **TRIM/deallocate** notifications so the FTL knows which LBAs hold dead data. Metrics: IOPS (read/write), latency (µs), **write amplification** `WA = data written to NAND / data written by host`, endurance (TBW — total bytes written), and performance consistency (steady-state vs burst).

## 8. Example
1. Host writes logical LBA 0x100 (page size 4 KB). FTL allocates a fresh physical page P0x00A; map[0x100] = P0x00A. The old physical page holding 0x100's prior data is now *invalid* but not erased (its block has other valid pages).
2. GC timer fires: block B has 250 valid + 6 invalid pages. FTL reads the 250 valid pages, writes them to a free block, erases B → 256 free pages. That's the read+write amplification (250 reads + 250 writes for 6 freed pages, pre-TRIM).
3. Host deletes file → TRIM (0x100..0x13F) → FTL marks those LBAs' pages invalid without GC reading them → next GC is cheaper, WA ↓.
4. Over time, wear leveling picks victim blocks near the wear floor to keep P/E counts uniform → endurance extends.
5. Hybrid: `bcache` puts hot blocks on SSD and cold on HDD; on a miss the HDD data is promoted to SSD.

## 9. Internal Working
1. Host I/O → NVMe/SATA command → drive controller.
2. FTL lookup: map LBA → physical page (DRAM-resident map, e.g., 1 GB DRAM per TB with 4 KB pages — the map itself is a cost).
3. Write path: allocate erased page (from free-block pool maintained by GC); program page; update map; mark old page invalid.
4. GC path (background): pick victim block (least valid pages, adjusted for wear) → copy valid → erase → return to free pool.
5. TRIM path: host deallocates LBA ranges → FTL invalidates → boosts GC efficiency.
6. Wear leveling: periodically migrate cold data from heavily-erased... (static leveling) so low-wear blocks also get used.
7. Failure: power loss → the map is in DRAM → needs a journal/PLP (power loss protection) or the map is partially persisted; enterprise drives have capacitors.

## 10. Time Complexity
- Random read: O(1) map lookup + page read — **same as sequential** (~10–100 µs). No seek.
- Random write: O(1) mapped write, *if* a free erased page exists; else triggers GC → amortized cost includes GC.
- Write amplification: WA ≈ 1 (ideal) to ~2–5 (poor overprovisioning + un-TRIM'd) — the real cost of flash writes.
- GC: O(pages in block) read+write per victim block; background.
- Map lookup: O(1) hash/array (DRAM) or O(log n) if on-flash partial.
- Endurance: total writes before cells fail ≈ (capacity × P/E cycles) / WA.

## 11. Advantages
- **Performance**: ~10–100 µs latency, 100K+ IOPS, random = sequential.
- **No seek/rotation** → deterministic latency, parallel (multi-channel).
- **Low power, silent, shock-resistant**.
- **Wear leveling + TRIM + overprovisioning** make consumer drives survive ~10 years of typical use.
- **NVMe**: deep queues, PCIe bandwidth, low protocol overhead.

## 12. Disadvantages
- **Finite endurance** (P/E cycles): write-heavy workloads (logging, temp DBs) can exhaust TBW.
- **Write amplification**: GC copies valid data — up to 5× the host's writes.
- **Performance cliff**: burst vs steady state; GC can stall writes.
- **Cost per GB** > HDD (hence hybrids and tiering).
- **Power-loss** → map consistency requires PLP (capacitors).
- **"SLC-cache" burst behavior** (TLC drives fake-SLC a chunk then drop to real speed) — peak specs mislead.

## 13. Interview Questions
1. **Q: Why is random I/O fast on SSDs?** A: No moving head/rotation — access is a map lookup + page read/write, independent of location; random ≈ sequential.
2. **Q: What is wear leveling?** A: The FTL distributes program/erase cycles evenly across blocks so hot blocks don't wear out early; dynamic (write to low-wear blocks) + static (migrate cold data).
3. **Q: What is write amplification?** A: The ratio (data written to NAND) / (data written by host) — GC and the erase-block-size mismatch force extra writes; TRIM + overprovisioning reduce it.
4. **Q: What is TRIM?** A: An ATA/NVMe command telling the drive which LBAs contain dead (deleted) data so GC can skip copying them — lowers WA and preserves endurance.
5. **Q: Why can't flash overwrite in place?** A: A page can only be programmed after its block is erased; erasing a block destroys all its pages — so writes go to fresh pages (out-of-place) and old ones are invalidated until GC reclaims the block.
6. **Q: What is garbage collection?** A: The FTL reclaims blocks with mostly-invalid pages: copy remaining valid pages to a free block, erase the victim, return to free pool — the source of WA and latency variance.
7. **Q: SLC vs MLC vs TLC vs QLC?** A: Bits per cell: 1/2/3/4. More bits = cheaper + denser but fewer P/E cycles (100K/10K/3K/1K), slower, and higher error rates.
8. **Q: What is overprovisioning?** A: Reserved spare capacity (~7–28%) not exposed to the host; gives GC slack so steady-state performance and endurance hold up.
9. **Q: What is the FTL?** A: Flash Translation Layer — the drive-internal mapping (LBA→physical page), out-of-place write engine, GC, and wear leveler; it's why the OS sees a normal block device.
10. **Q: Why do hybrid/HDD+SSD designs exist?** A: Cost — flash per GB is higher; tiering hot data (SSD) and cold data (HDD) delivers most of the speedup at a fraction of the price (bcache, dm-cache, Fusion).
11. **Q: What's the difference between an SSD's map and a page table?** A: Conceptually similar (logical→physical indirection), but the SSD map is at 4 KB page granularity in the drive's DRAM, updated by the FTL — a storage translation, not a virtual-memory one.
12. **Q: Why did disk scheduling become obsolete on SSDs?** A: No seek/rotation to minimize — access time is uniform; the OS uses `none`/noop, and NVMe queues handle ordering in hardware.

## 14. Follow-Up Questions
1. **Q: What is a power-loss protection (PLP) capacitor?** A: Enterprise drives use capacitors to flush the in-DRAM map (and cache) to NAND on power loss so mappings aren't lost.
2. **Q: What is L2ARC / special vdev?** A: ZFS's SSD cache and metadata/log devices — using flash as a tier for hot blocks and small synchronous writes.
3. **Q: What is NVMe multipath?** A: Two PCIe paths to the same NVMe namespace — failover and load balancing at the block layer (`nvme-multipath`).
4. **Q: What is the difference between a log-structured filesystem and an SSD?** A: A log-structured FS (Section 08-04-03) also does out-of-place updates — the SSD FTL is an *internal* log-structured translator; LFS + FTL stack redundantly but combine well.

## 15. Coding Example
```c
// Sketch of an FTL: map + out-of-place write + GC + wear leveling
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

#define NBLOCKS 4
#define PAGES   4   // pages per block
#define CYCLES  64  // erase limit per block (tiny, for illustration)

typedef struct { uint32_t lba; uint32_t wear; } page_t;

typedef struct {
    uint32_t map[256];   // lba -> physical page index
    uint32_t ppe[NBLOCKS * PAGES]; // physical page -> erase count (block id derived)
    page_t   data[NBLOCKS * PAGES];
} fsl;

void ftl_write(fsl *f, uint32_t lba, uint32_t val, uint32_t *free_pages) {
    // find the least-worn free page (dynamic wear leveling)
    int best = -1;
    for (int i = 0; i < NBLOCKS * PAGES; i++)
        if (f->map[i] == 0xFFFFFFFF && (best < 0 || f->ppe[i] < f->ppe[best])) best = i;
    f->map[best] = lba;           // out-of-place write: new page
    f->data[best].lba = val;      // (val would be real data)
    f->ppe[best]++;
    *free_pages = *free_pages - 1;
}

int main(void) {
    fsl f = {0};
    for (int i = 0; i < NBLOCKS * PAGES; i++) f.map[i] = 0xFFFFFFFF;
    uint32_t free_pages = NBLOCKS * PAGES;
    for (int i = 0; i < 8; i++) ftl_write(&f, i, i * 2, &free_pages);
    printf("free pages left: %u (GC would reclaim invalid ones)\n", free_pages);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `nvme` driver, `blk-mq` `none`/`noop` schedulers, `fstrim` (discard), `Documentation/nvme/`.
- **Kernel**: TRIM/discard via `blkdev_issue_discard`; filesystems issue it on delete (`fstrim`, auto-discard mount option).
- **Tiering**: `bcache`, `dm-cache`, ZFS L2ARC/special vdev, Intel RST/Rapid Storage (hybrid), Optane.
- **Enterprise**: NVMe datacenter drives, EBS gp3/io2 (NVMe-backed), Windows Storage Spaces tiering.
- **Databases**: PostgreSQL `random_page_cost = 1` on SSD; MySQL innodb_io_capacity tuning.

## 17. References
- Silberschatz, *Operating System Concepts*, Ch. 10.8 "SSDs and Flash".
- Tanenbaum, *Modern Operating Systems*, Ch. 5.5.6 (flash).
- Linux `Documentation/block/`, `Documentation/nvme/`.
- SNIA: "Solid State Storage Performance Test Specification", NAND Flash 101.
- Micron/Intel NAND reliability whitepapers (P/E cycles, WA).
- `man fstrim`, `nvme-cli` documentation.

## 18. Cheat Sheet
- No seek/rotation → random = sequential.
- NAND: erase-before-write (block) + finite P/E cycles.
- FTL: LBA→page map, out-of-place writes, GC, wear leveling.
- WA = NAND writes / host writes; TRIM + overprovisioning ↓ WA.
- SLC 100K / MLC 10K / TLC 3K / QLC 1K P/E cycles.
- GC picks victim blocks by invalid count; can stall writes.
- Hybrid: bcache/dm-cache/ZFS L2ARC tier hot data.
- Disk scheduling obsolete on SSDs → `none`/noop.
- PLP caps protect the in-DRAM map on power loss.

## 19. Quiz
1. SSDs' random access is fast because? a) cache b) no seek b) d) DMA → **b** (no moving head)
2. Erase unit of NAND is the? a) page b) block c) sector d) LBA → **b**
3. TRIM's purpose? a) faster reads b) tell SSD about dead LBAs c) defrag d) encrypt → **b**
4. Write amplification is reduced by? a) RAID b) TRIM + overprovisioning c) NCQ d) SLC → **b**
5. TLC vs SLC endurance? a) TLC higher b) SLC higher c) equal d) neither → **b**
6. Disk scheduling on SSDs is? a) critical b) obsolete c) SSTF d) SCAN → **b**

## 20. Flashcards
- **Q: Why random = sequential on SSD?** → **A:** No head to move.
- **Q: What is WA?** → **A:** NAND writes / host writes; GC overhead.
- **Q: What is TRIM?** → **A:** Host→SSD notice of dead LBAs.
- **Q: Why erase-before-write?** → **A:** Flash can only program a page in an erased block.
- **Q: SLC vs QLC cycles?** → **A:** ~100K vs ~1K.
- **Q: Why hybrids?** → **A:** Flash cost; tier hot/cold.

## 21. Revision
SSDs removed the moving head, making random access as fast as sequential — but NAND can only write to erased blocks and cells wear out. The FTL hides this: a DRAM logical→physical map, out-of-place writes, garbage collection of invalid pages, and dynamic+static wear leveling keep endurance and performance in check. TRIM tells the FTL which data is dead (reducing write amplification); overprovisioning gives GC slack; power-loss protection (PLP) preserves the map. Because there's no seek, the OS uses `none`/noop scheduling, and hybrids (bcache, ZFS L2ARC, Optane) tier hot data on flash and cold on HDD to balance cost and speed. Pair this with Section 01's HDD physics for the complete "storage substrate" picture.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is random I/O fast on SSDs?" | 1 Why / 13 Q1 |
| "What is wear leveling?" | 13 Q2 / 2 How |
| "What is write amplification?" | 13 Q3 / 9 Internal |
| "What is TRIM?" | 13 Q4 / 2 How |
| "Why erase-before-write?" | 13 Q5 / 2 How |
| "SLC vs TLC vs QLC?" | 13 Q7 / 2 How |
| "Why are hybrids used?" | 13 Q10 / 16 Industry |
| "Why is scheduling obsolete?" | 13 Q12 / 12 Disadvantages |
