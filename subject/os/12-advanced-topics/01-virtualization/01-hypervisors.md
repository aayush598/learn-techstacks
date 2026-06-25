# Hypervisors & Virtualization

## Type 1 vs Type 2 Hypervisors

| Property | Type 1 (Bare-Metal) | Type 2 (Hosted) |
|----------|---------------------|-----------------|
| **Host OS** | No host OS — hypervisor runs directly on hardware | Requires host OS (Windows, Linux, macOS) |
| **Performance** | Near-native (~2–5% overhead) | Higher overhead (~10–20%) |
| **Isolation** | Stronger (less attack surface) | Weaker (depends on host OS) |
| **Use case** | Servers, cloud, datacenters | Development, testing, desktop VMs |
| **Examples** | VMware ESXi, Xen, KVM, Hyper-V, Nutanix AHV | VirtualBox, VMware Workstation, Parallels |

## Virtualization Techniques

### Para-virtualization (PV)
- Guest OS **modified** — knows it's virtualized
- Uses **hypercalls** instead of privileged instructions
- **Xen PV:** aware guests, faster I/O (frontend/backend drivers)
- **Pro:** better performance (less emulation)
- **Con:** requires modified OS (can't run Windows unmodified)

### Full Virtualization (Binary Translation)
- Guest OS **unmodified** — thinks it's on real hardware
- Hypervisor translates privileged instructions on-the-fly
- **VMware ESXi:** binary translation + direct execution
- **Pro:** runs any OS
- **Con:** binary translation is overhead

### Hardware-Assisted Virtualization (HVM)
- **CPU extensions** handle privileged instructions
  - **Intel VT-x:** VMX root (hypervisor) / VMX non-root (guest)
  - **AMD-V:** equivalent
- Guest runs directly on CPU for most instructions
- Hypervisor only traps for specific operations (I/O, MMIO, etc.)
- **Dominant today** — used by all major hypervisors

## KVM (Kernel-based Virtual Machine)
- **Linux kernel module** that turns Linux into a Type 1 hypervisor
- `kvm.ko` + processor-specific (`kvm-intel.ko`, `kvm-amd.ko`)
- Each VM = Linux process (managed with cgroups, namespaces)
- Uses `/dev/kvm` interface: `KVM_CREATE_VM`, `KVM_RUN`, `KVM_CREATE_VCPU`
- **QEMU** provides device emulation + management (userspace)
- **Libvirt** provides management API (virt-manager, virsh)

## Performance Comparison

| Technique | CPU Overhead | Memory Overhead | I/O Overhead |
|-----------|-------------|-----------------|--------------|
| **Para-virtualization** | <1% | Minimal | Low (driver optimized) |
| **Full virtualization (BT)** | 5–15% | Low | High (device emulation) |
| **Hardware-assisted (HVM)** | <1% | Minimal | Medium (depends on I/O model) |
| **HVM + PV drivers** | <1% | Minimal | Near-native |
| **Container (shared kernel)** | ~0% | ~0% | ~0% (but weaker isolation) |

## Key Concepts
- **VM Exit:** CPU transitions from guest → hypervisor (on privileged op, I/O, interrupt)
- **VM Entry:** hypervisor → guest
- **EPT (Extended Page Tables):** Intel's 2nd level address translation (guest physical → host physical)
- **Shadow Page Tables:** older method — hypervisor maintains shadow PT (EPT replaced this)

## Interview Tips
- *"KVM turns Linux into a Type 1 hypervisor — VMs are just processes"*
- *"Intel VT-x (VMX) allows direct guest execution with hardware trapping"*
- *"Para-virtualization trades OS compatibility for performance"*
- *"Today: HVM + PV drivers (virtio) is the standard approach"*
