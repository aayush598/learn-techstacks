# Segmentation

## Motivation

- User/programmer views memory as **logical units**: code, data, stack, heap
- Pagination is invisible to programmer; segmentation matches user's view
- Each segment is a **variable-sized** contiguous block

## Logical Address

```
Logical address: [ segment# (s bits) | offset (d bits) ]
```

- Segment# indexes into **segment table** (per process)
- Segment table entry: `[base, limit, protection]`
- **Base:** starting physical address of segment
- **Limit:** size (length) of segment
- Protection: read/write/execute permissions per segment

## Address Translation

```
1. Extract segment# and offset
2. Check: offset < limit? (else → segmentation fault)
3. Physical address = base + offset
```

```
Process:
+--------+  Code segment (base=0x400000, limit=64KB, R+X)
+--------+  Data segment (base=0x500000, limit=32KB, R+W)
+--------+  Stack segment (base=0x700000, limit=8KB, R+W)
```

## Protection & Sharing

- Each segment has independent **protection bits**
- **R** (read), **W** (write), **X** (execute)
- Segments can be **shared** between processes (same base/limit)
- Example: shared library code segment (R+X) is shared, data segment (R+W) is private
- Segmentation fault: accessing beyond limit or violating protection

## Fragmentation

- **External fragmentation:** segments are variable-sized
- Allocation/termination creates holes over time
- **Compaction** needed (expensive, may need dynamic relocation)
- No internal fragmentation (segment exactly fits process's logical unit)

## Intel x86 Segmentation

- x86 had segmentation **before** paging became standard
- **Segment registers:** CS (code), DS (data), SS (stack), ES, FS, GS
- Protected mode: segment selector → Global/Local Descriptor Table → segment descriptor
- **Descriptor:** base (32-bit), limit (20-bit), G (granularity), DPL (privilege), type
- Modern x86-64: segmentation mostly **disabled** in 64-bit mode (CS/DS/SS treated as base=0)
- Linux uses **flat memory model**: all segments base=0, limit=max

## Segmentation vs Paging

| Aspect | Segmentation | Paging |
|---|---|---|
| **View** | Programmer's logical view | Hardware's physical view |
| **Size** | Variable | Fixed (4 KB) |
| **Fragmentation** | External | Internal (last page) |
| **Sharing** | Natural (by segment) | Via shared pages |
| **Protection** | Per segment | Per page |
| **Memory waste** | Holes between segments | Last page waste |
