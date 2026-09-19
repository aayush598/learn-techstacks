# Cellular, 4G/5G and Mobility — 100 Interview Q&A

## Q1: What is a BTS in cellular networks?

**A:** A Base Transceiver Station (BTS) is the fixed equipment that handles wireless communication with mobile devices within a specific cell. It houses the radio transceivers, antennas, and signal processing hardware that transmit and receive RF signals to and from user equipment (UE). The BTS is responsible for encoding/decoding radio signals, modulation/demodulation, and maintaining the radio link with devices in its coverage area.

A BTS is controlled by a Base Station Controller (BSC) in 2G GSM networks or directly managed by the Radio Network Controller (RNC) in 3G UMTS. Each BTS covers one or more cells, and its transmit power, frequency, and antenna configuration determine the cell boundary. The BTS also handles handover measurements and reporting back to the controller, enabling seamless mobility as users move between cells.

In LTE and 5G, the BTS equivalent is the eNodeB (evolved NodeB) and gNodeB respectively, which combine the transceiver and controller functions into a single entity, flattening the network architecture.

## Q2: What is the role of the Radio Network Controller (RNC)?

**A:** The RNC is the governing element in the UMTS/3G radio access network (RAN) that controls multiple NodeBs. It manages radio resource allocation, handover decisions, encryption/decryption of user data, and admission control for new connections. The RNC aggregates traffic from multiple NodeBs and connects to the core network via the Iu interface.

RNCs communicate with each other via the Iur interface, which supports soft handover between RNCs—a key advantage of CDMA-based 3G systems. The RNC also performs macro diversity combining during soft handover, where a UE communicates with multiple NodeBs simultaneously and the RNC merges the signals for improved reliability.

In LTE, the RNC function was absorbed into the eNodeB, creating a flat all-IP architecture. This eliminated the Iur interface overhead and reduced handover latency, which was a significant architectural improvement over 3G.

## Q3: What is a cell in cellular networking?

**A:** A cell is the geographic area served by a single base station (BTS/eNodeB/gNodeB). The cellular concept, proposed by Bell Labs, divides a coverage region into a tessellation of cells, each using a subset of available frequencies. This enables frequency reuse across non-adjacent cells, dramatically increasing system capacity compared to a single high-power transmitter.

Cells are typically hexagonal in theoretical models but irregular in practice due to terrain, buildings, and propagation characteristics. Cell sizes range from macro cells (several kilometers radius) to micro cells (hundreds of meters) to pico and femto cells (tens of meters), enabling hierarchical coverage layers.

The cell concept is foundational to all generations of cellular networks. In 5G, ultra-dense deployments with small cells are critical for mmWave coverage, and the cell concept extends to virtual cells where multiple TRPs (Transmission Reception Points) serve a single logical cell.

## Q4: What is frequency reuse in cellular systems?

**A:** Frequency reuse is the technique of using the same set of frequencies in non-adjacent cells to increase spectral efficiency. Since radio signals attenuate with distance, cells sufficiently far apart can reuse the same frequency without causing unacceptable co-channel interference. The reuse factor N determines how many distinct frequency groups exist; for example, N=7 means frequencies are divided into 7 sets and each cell uses one set.

A smaller reuse factor increases capacity but raises co-channel interference. Modern cellular systems use a reuse factor of 1 (universal frequency reuse) combined with inter-cell interference coordination (ICIC) techniques. LTE uses orthogonal frequency division multiple access (OFDMA) which naturally mitigates much of the inter-cell interference through subcarrier-level scheduling.

In 5G NR, fractional frequency reuse and beamforming-based spatial isolation further enable aggressive frequency reuse while managing interference at the cell edge.

## Q5: What is the difference between hard handover and soft handover?

**A:** Hard handover is a "break-before-make" approach where the UE disconnects from the source cell before connecting to the target cell. There is a brief interruption in service, though modern implementations minimize this to tens of milliseconds. GSM and LTE use hard handover because their TDMA/OFDMA air interfaces make simultaneous transmission to two base stations impractical.

Soft handover is a "make-before-break" approach where the UE maintains simultaneous connections with multiple base stations during the transition. The UE is in the "handover zone" where signals from both source and target cells overlap. The RNC combines signals from multiple NodeBs (macro diversity), improving reliability and eliminating service interruption. This is a fundamental feature of CDMA-based 3G systems.

Softer handover occurs when multiple sectors of the same base station communicate with the UE simultaneously. Both hard and soft handovers require the UE to perform measurements (RSSI, RSRP, RSRQ) and report them to the network, which then makes the handover decision.

## Q6: What is CDMA and how does it work in cellular networks?

**A:** Code Division Multiple Access (CDMA) is a spread-spectrum multiple access technique where multiple users share the same frequency band simultaneously. Each user's data is multiplied by a unique spreading code (Walsh code), resulting in a wideband signal. The receiver uses the same code to extract the desired signal from the composite of all users' signals.

In CDMA, all users transmit on all frequencies at all times, but are separated by their unique codes. This provides soft capacity limits—the system degrades gracefully as more users are added, rather than blocking new calls abruptly. CDMA also provides inherent security through the spreading codes and resistance to multipath fading via RAKE receivers.

IS-95 (cdmaOne) was the first CDMA standard, followed by CDMA2000 and WCDMA (UMTS). CDMA2000 is the 3G evolution of IS-95, while WCDMA is the 3G standard developed by 3GPP as part of the UMTS family, using a 5 MHz channel bandwidth.

## Q7: What is GSM and how does it differ from CDMA?

**A:** Global System for Mobile Communications (GSM) is a TDMA-based cellular standard that uses narrowband 200 kHz channels with 8 time slots per carrier. Each user is assigned a specific time slot, providing deterministic capacity. GSM operates in 900 MHz and 1800 MHz bands (2100 MHz for UMTS), and uses SIM cards for subscriber identification.

Key differences from CDMA: GSM uses TDMA/FDMA for channel access with fixed capacity per cell, while CDMA uses spread spectrum with soft capacity. GSM hard handovers are simpler but less graceful than CDMA soft handovers. GSM provides better spectral efficiency at lower loads, while CDMA excels at higher loads due to its interference-limited nature.

GSM evolved to EDGE (Enhanced Data rates for GSM Evolution) for 2.5G, while CDMA evolved to CDMA2000 EV-DO for 3G. Both paths eventually converged to LTE/4G, which uses OFDMA—neither TDMA nor CDMA.

## Q8: What is the EPC in LTE architecture?

**A:** The Evolved Packet Core (EPC) is the core network architecture for LTE, designed as an all-IP flat architecture to minimize latency and maximize throughput. The EPC comprises four main elements: the Mobility Management Entity (MME), Serving Gateway (S-GW), PDN Gateway (P-GW), and Home Subscriber Server (HSS).

The MME handles signaling related to mobility, authentication, and bearer management. The S-GW routes and forwards user data packets, acting as the anchor for mobility between eNodeBs. The P-GW connects to external packet data networks (PDNs), performs IP address allocation, and enforces QoS policies. The HSS stores subscriber profiles and authentication vectors.

The EPC separates the control plane (MME) from the user plane (S-GW/P-GW), enabling independent scaling. This separation was a precursor to the Control and User Plane Separation (CUPS) architecture introduced in later 3GPP releases and carried forward into 5G core.

## Q9: What is an eNodeB in LTE?

**A:** An eNodeB (evolved NodeB) is the base station in LTE that combines the functions of the 2G BTS/BSC and 3G NodeB/RNC into a single entity. This flattening of the radio access network reduces latency and simplifies handover. The eNodeB manages radio resources, performs handover decisions, handles encryption/decoding, and schedules user data on the OFDMA air interface.

Each eNodeB connects to the EPC via S1 interfaces: S1-MME for control plane signaling to the MME, and S1-U for user plane data to the S-GW. eNodeBs communicate with each other via the X2 interface, which supports handover and inter-cell interference coordination (ICIC).

The eNodeB also implements features like Almost Blank Subframe (ABS) for enhanced ICIC, and supports carrier aggregation to combine multiple component carriers for higher throughput.

## Q10: What is OFDMA and why is it used in LTE/5G?

**A:** Orthogonal Frequency Division Multiple Access (OFDMA) divides the available bandwidth into many narrow orthogonal subcarriers (typically 15 kHz in LTE). Each user is assigned a subset of subcarriers (resource blocks) for each transmission time interval (TTI). The orthogonality between subcarriers eliminates inter-carrier interference without requiring guard bands.

OFDMA provides several advantages: robustness to multipath fading (since each subcarrier has a narrow bandwidth, frequency selective fading affects only a few subcarriers), flexible resource allocation (subcarriers can be assigned dynamically based on channel conditions), and efficient MIMO implementation (each subcarrier can independently apply MIMO precoding).

In LTE, each resource block consists of 12 subcarriers (180 kHz) over one slot (0.5 ms). In 5G NR, subcarrier spacing is scalable (15, 30, 60, 120, 240 kHz) to support different deployment scenarios, from sub-6 GHz to mmWave frequencies.

## Q11: What is LTE-Advanced and how does it enhance basic LTE?

**A:** LTE-Advanced (LTE-A), defined in 3GPP Release 10, is an enhancement of LTE that meets the ITU's IMT-Advanced requirements for 4G. Key features include carrier aggregation (combining up to 5 component carriers for 100 MHz aggregate bandwidth), enhanced MIMO (up to 8x8 DL and 4x4 UL), relay nodes, and enhanced inter-cell interference coordination (eICIC).

Carrier aggregation allows operators to combine fragmented spectrum holdings. Each component carrier can be up to 20 MHz, and carriers can be contiguous or non-contiguous, in the same or different bands. This enables peak data rates exceeding 1 Gbps downlink and 500 Mbps uplink.

LTE-A also introduced Coordinated Multipoint (CoMP) transmission, where multiple eNodeBs coordinate their transmissions to improve cell-edge performance. HetNet support with pico/femto cells overlaying macro cells became a key deployment scenario.

## Q12: What is LTE-Advanced Pro?

**A:** LTE-Advanced Pro (LTE-A Pro), defined in 3GPP Release 13-14, bridges LTE and 5G with further enhancements. It supports carrier aggregation of up to 32 component carriers, license-assisted access (LAA) using unlicensed spectrum, full-dimension MIMO (FD-MIMO) with massive antenna arrays, and NB-IoT for narrowband IoT communications.

FD-MIMO uses large antenna arrays (up to 16x16 two-dimensional arrays) to create elevation beamforming in addition to traditional azimuthal beamforming. This significantly increases spatial multiplexing gain and cell capacity.

LTE-A Pro also introduced enhancements for vehicle-to-everything (V2X) communication, positioning improvements, and mini-slots for reduced latency. These features laid the groundwork for many technologies that were later standardized in 5G NR.

## Q13: What is network slicing in 5G?

**A:** Network slicing is the ability to create multiple logical networks on top of a shared physical infrastructure, each tailored to specific service requirements. Each slice has its own virtualized network functions, resource allocation, and QoS policies. The three main slice types defined by 3GPP are eMBB (enhanced Mobile Broadband), URLLC (Ultra-Reliable Low-Latency Communications), and mMTC (massive Machine-Type Communications).

eMBB slices prioritize high throughput for applications like video streaming and AR/VR. URLLC slices minimize latency and maximize reliability for applications like industrial automation and autonomous driving. mMTC slices support massive connection density (up to 1 million devices per km²) for IoT applications like smart cities.

Slicing is implemented through the 5G Service-Based Architecture (SBA) using Network Slice Selection Assistance Information (NSSAI). The SMF (Session Management Function) and AMF (Access and Mobility Management Function) work together to select and manage slices based on subscriber profiles and service requirements.

## Q14: What is MIMO and how does it improve wireless performance?

**A:** Multiple-Input Multiple-Output (MIMO) uses multiple antennas at both transmitter and receiver to exploit multipath propagation. MIMO provides three key benefits: spatial multiplexing (transmitting independent data streams on parallel spatial channels, increasing throughput), diversity (transmitting redundant copies to improve reliability), and beamforming (focusing energy in specific directions to improve SNR and reduce interference).

Spatial multiplexing gain scales with the number of antenna pairs, up to min(Nt, Nr) where Nt is transmit antennas and Nr is receive antennas. A 4x4 MIMO system can theoretically quadruple the data rate compared to a SISO system in rich scattering environments.

In LTE, MIMO modes include transmit diversity (SFBC), spatial multiplexing (open-loop and closed-loop), and beamforming (Type I and Type II codebooks). 5G NR extends this with massive MIMO, using 64 or more antenna elements to serve multiple users simultaneously through MU-MIMO.

## Q15: What is beamforming in 5G?

**A:** Beamforming is a signal processing technique that focuses radio energy in the direction of a specific user or group of users by controlling the phase and amplitude of signals at each antenna element. This creates a directional beam pattern that increases the received signal strength at the intended user while reducing interference to others.

In 5G NR, beamforming operates at two levels: digital beamforming (performed in the baseband on individual OFDM subcarriers) and analog beamforming (performed using phase shifters in the RF domain). Hybrid beamforming combines both approaches, which is essential for mmWave frequencies where the large number of antenna elements makes full digital beamforming prohibitively expensive.

Beam management in 5G includes beam sweeping (the gNodeB transmits reference signals in multiple directions), beam measurement (the UE measures received power), beam reporting (the UE feeds back the best beam index), and beam tracking (adapting the beam as the UE moves). This is critical for mmWave bands where path loss is severe.

## Q16: What is the difference between 4G and 5G NR?

**A:** 5G NR (New Radio) is not just an evolution of LTE but a fundamentally redesigned air interface. Key differences include: scalable subcarrier spacing (15-240 kHz vs. fixed 15 kHz in LTE), support for frequencies up to 100 GHz (mmWave) vs. LTE's 6 GHz limit, flexible frame structure with mini-slots for low latency, and a new channel coding scheme (LDPC for data, Polar codes for control).

5G NR achieves peak data rates of 20 Gbps downlink and 10 Gbps uplink, with user-plane latency below 1 ms for URLLC. It supports massive MIMO with arrays of 64+ antennas, network slicing, and service-based core architecture. LTE maximum is 1 Gbps with ~10 ms user-plane latency.

The deployment options for 5G include Non-Standalone (NSA) mode, where 5G NR uses the LTE core network and EPC for control plane functions, and Standalone (SA) mode with the full 5G core (5GC). NSA enables faster initial deployment by leveraging existing LTE infrastructure.

## Q17: What are the 5G frequency bands?

**A:** 5G NR operates in three frequency ranges. FR1 (sub-6 GHz) includes bands from 410 MHz to 7.125 GHz, providing wide coverage and good building penetration. FR2 (mmWave) covers 24.25 GHz to 52.6 GHz, offering massive bandwidth for high throughput but with limited range and poor penetration. Extended FR2 covers up to 71 GHz for future deployments.

Common 5G bands include n77/n78 (3.3-4.2 GHz, C-band), n41 (2.5 GHz), n257/n258/n260/n261 (mmWave), and n1/n3/n28 (low-band refarmed spectrum). The C-band has become the primary 5G mid-band spectrum in many countries, balancing coverage and capacity.

Each band has different propagation characteristics. Sub-6 GHz bands provide coverage areas comparable to LTE, while mmWave requires dense small cell deployments with line-of-sight or near-line-of-sight conditions. Power class also varies, with FR2 supporting higher EIRP through beamforming gain.

## Q18: What is Fixed Wireless Access (FWA) in 5G?

**A:** Fixed Wireless Access uses 5G NR to provide broadband connectivity to a fixed location (home or business) as an alternative to fiber or cable. A 5G customer premises equipment (CPE) with an outdoor antenna receives the 5G signal and provides Wi-Fi/Ethernet connectivity inside the premises. FWA is one of the most commercially successful 5G use cases.

FWA is particularly valuable in areas where laying fiber is expensive or impractical, such as rural or suburban locations. A single 5G macro site can serve hundreds of FWA customers, and the economics become attractive when compared to last-mile fiber deployment costs.

Key technologies enabling FWA include massive MIMO for increased capacity, beamforming for directional coverage, and mmWave for high-throughput short-range links. Operators like T-Mobile and Verizon have deployed millions of FWA connections, and the technology is becoming a significant revenue stream for 5G operators.

## Q19: What is the 5G Service Based Architecture (SBA)?

**A:** The 5G SBA replaces the point-to-point interfaces of EPC with a service-based model where network functions (NFs) expose standardized APIs. NFs communicate through HTTP/2-based service interfaces, enabling a microservices-like architecture. Key NFs include AMF (access and mobility management), SMF (session management), UPF (user plane function), PCF (policy control), UDM (unified data management), and NRF (NF repository function).

The NRF enables NF discovery—when one NF needs to communicate with another, it queries the NRF to find available instances. This dynamic discovery enables elastic scaling and redundancy without manual configuration.

The SBA decouples software from hardware through network function virtualization (NFV) and containerization (CNF—Cloud Native NFs). This enables operators to deploy, scale, and update individual functions independently, reducing time-to-market for new services and enabling the network slicing capabilities that differentiate 5G.

## Q20: What is the UPF in 5G?

**A:** The User Plane Function (UPF) is the 5G core network element that handles user data forwarding, routing, and packet inspection. It is the anchor point for mobility, connecting the RAN to external data networks. The UPF performs traffic steering based on policies received from the SMF, and can apply QoS enforcement, traffic usage reporting, and lawful intercept.

Multiple UPFs can be chained to create specific data paths for different services. For URLLC, a local UPF can be deployed at the network edge (MEC—Multi-access Edge Computing) to minimize latency by processing traffic close to the user without traversing the entire core network.

The UPF is a key enabler of network slicing, as each slice can have its own UPF instances with dedicated resources. It is typically implemented as a cloud-native function running on commodity hardware, using technologies like DPDK or eBPF for high-performance packet processing.

## Q21: What is Multi-access Edge Computing (MEC)?

**A:** MEC brings compute and storage resources to the network edge, closer to end users. In 5G, MEC platforms are deployed alongside gNodeBs or at aggregation points, enabling applications to run within the operator's network rather than in distant cloud data centers. This reduces end-to-end latency to single-digit milliseconds.

MEC is critical for latency-sensitive applications: autonomous driving (V2X processing), industrial IoT (real-time control loops), AR/VR (rendering), and cloud gaming. It also enables data sovereignty by keeping sensitive data within the operator's network.

The ETSI MEC framework defines standardized APIs for application developers to discover and use edge resources. In 5G, MEC integration with the UPF allows traffic to be diverted to local applications without traversing the core network, enabling a "local breakout" architecture.

## Q22: What is Carrier Aggregation (CA) in LTE/5G?

**A:** Carrier Aggregation combines multiple component carriers (CCs) to increase the aggregate bandwidth available to a single UE. In LTE-A, up to 5 CCs of 20 MHz each can be aggregated for 100 MHz total bandwidth. LTE-A Pro extends this to 32 CCs, and 5G NR supports up to 16 CCs.

CA can be intra-band (all CCs in the same frequency band) or inter-band (CCs in different bands). Intra-band CA can be contiguous (CCs are adjacent) or non-contiguous (CCs have a frequency gap). Inter-band CA allows combining, for example, low-band coverage with mid-band capacity.

Each CC has its own HARQ entity and can be independently scheduled. The UE decodes a Physical Downlink Control Channel (PDCCH) on each CC to learn its resource assignments. This transparent aggregation increases peak and average throughput without requiring changes to higher-layer protocols.

## Q23: What is the role of HSS and UDM?

**A:** The Home Subscriber Server (HSS) in LTE and the Unified Data Management (UDM) in 5G are the central subscriber databases. They store subscriber profiles including authentication credentials, allowed services, QoS profiles, and mobility restrictions. The HSS/UDM generates authentication vectors used by the MME/AMF to authenticate UE during initial access.

The HSS is a monolithic database with proprietary interfaces (S6a diameter to MME). UDM in 5G adopts the SBA approach, exposing HTTP/2 APIs and separating the data layer (UDR—Unified Data Repository) from the business logic. This enables multiple network functions to access subscriber data through standardized APIs.

The evolution from HSS to UDM reflects the broader trend toward cloud-native, service-based architectures. UDM supports network slicing by providing slice-specific subscriber policies and can instantiate per-slice logical instances from a single physical deployment.

## Q24: What is the difference between LTE and 5G core networks?

**A:** The LTE EPC uses a 3GPP-specified architecture with point-to-point interfaces (S1, S5, S8, S11) between specific network elements. It is a flat, all-IP architecture but still relies on proprietary interfaces and purpose-built hardware. The control and user planes are separated (MME for control, S-GW/P-GW for user plane).

The 5G core (5GC) adopts a service-based architecture where NFs communicate via HTTP/2 RESTful APIs through a common service bus. It introduces new functions like the NSSF (Network Slice Selection Function), NEF (Network Exposure Function), and NWDAF (Network Data Analytics Function). The 5GC is designed for cloud-native deployment using containers.

The 5GC enables true network slicing, edge computing integration, and native support for non-3GPP access (Wi-Fi, wired). It also separates the access network from the core more cleanly, supporting多种 access types (NG-RAN, non-3GPP) through the common core.

## Q25: What is handover measurement in LTE?

**A:** In LTE, the UE continuously measures the reference signal received power (RSRP) and reference signal received quality (RSRQ) of serving and neighboring cells. The eNodeB configures measurement events (A1-A6, B1-B2) that trigger measurement reports based on thresholds and offsets. Event A3, for example, triggers when a neighbor becomes offset-better than the serving cell.

The measurement report includes the measured RSRP/RSRQ values and the Physical Cell Identity (PCI) of the neighbor cells. The eNodeB uses this information to make handover decisions, considering factors like load balancing, cell priority, and hysteresis to prevent ping-pong handovers.

Measurement gaps are configured when the UE cannot measure neighbors on its serving frequency (e.g., in inter-frequency measurements). During measurement gaps, the UE temporarily tunes to the neighbor frequency, performs measurements, and returns to the serving frequency.

## Q26: What is the RACH procedure in LTE/5G?

**A:** The Random Access Channel (RACH) procedure is how a UE initiates communication with the network. In the contention-based procedure, the UE sends a Random Access Preamble on PRACH, the eNodeB responds with a Random Access Response (RAR) containing timing advance and initial uplink grant, the UE transmits a scheduled message (MSG3), and the network resolves contention if multiple UEs selected the same preamble.

The preamble is selected from a set of 64 available sequences (Zadoff-Chu sequences in LTE, shorter sequences in 5G). The PRACH configuration determines the time-frequency resources available for preamble transmission, which affects the maximum number of simultaneous access attempts.

In 5G NR, the RACH procedure is enhanced with support for smaller cell sizes (shorter preamble sequences), beam failure recovery (the UE can select a preamble associated with a specific beam), and two-step RACH (MSG1+MSG2 combined, reducing latency for simple access scenarios).

## Q27: What is latency in cellular networks?

**A:** Latency in cellular networks has multiple components. User-plane latency is the time for a packet to travel between the UE and the core network (or edge server). Control-plane latency is the time to transition from idle to connected state. In LTE, user-plane latency is typically 10-20 ms, and control-plane latency is ~100 ms.

5G NR targets three latency tiers: eMBB with <4 ms user-plane latency, URLLC with <1 ms user-plane latency, and mMTC with relaxed latency requirements. Achieving ultra-low latency requires shorter transmission time intervals (mini-slots of 2 or 7 OFDM symbols vs. LTE's 14-symbol subframe), faster RACH procedures, and edge computing to reduce backhaul delay.

Latency is also affected by HARQ retransmissions, scheduling delays, and protocol processing. 5G NR reduces HARQ feedback delay with faster turnaround times and supports grant-free uplink transmission for URLLC, eliminating the scheduling request round-trip.

## Q28: What is Dual Connectivity (DC) in LTE/5G?

**A:** Dual Connectivity allows a UE to simultaneously connect to two base stations (master and secondary) on different carriers. In LTE, this is called EN-DC (E-UTRAN NR Dual Connectivity), where the LTE eNodeB is the master and the NR gNodeB is the secondary. This enables 5G NR deployment without a standalone 5G core.

In EN-DC, the MNG (Master Node Group) handles control plane signaling via the master eNodeB, while user plane data is split between the two nodes. The secondary gNodeB provides additional throughput on NR carriers. The Xx interface (X2 or Xn) between the nodes handles data forwarding and coordination.

DC is a key feature for NSA 5G deployment, allowing operators to add 5G NR capacity to their existing LTE networks. NR-DC (NR as master, LTE as secondary) and NE-DC (NR as master, E-UTRA as secondary) provide additional deployment flexibility in later 3GPP releases.

## Q29: What is massive MIMO in 5G?

**A:** Massive MIMO uses large antenna arrays (typically 64-256 elements) at the gNodeB to serve multiple users simultaneously through spatial multiplexing. The large number of antennas creates highly focused beams, increasing spectral efficiency by a factor proportional to the number of antenna pairs.

The key benefits include: array gain (coherent combining of signals from many antennas increases SNR), spatial multiplexing (serving multiple users on the same time-frequency resource), and interference suppression (nulling interference to unintended users). A 64T64R massive MIMO system can serve 16 or more users simultaneously on the same resource block.

Practical challenges include channel estimation overhead (the gNodeB needs accurate channel state information for beamforming), pilot contamination (pilot sequences from neighboring cells interfere), and hardware complexity/cost. FDD massive MIMO requires downlink pilot transmission and uplink CSI feedback, while TDD massive MIMO can exploit channel reciprocity with uplink pilots only.

## Q30: What is Non-Terrestrial Network (NTN) in 5G?

**A:** 5G NTN extends cellular connectivity to satellites, high-altitude platforms (HAPs), and drones. 3GPP Release 17 introduced NTN support, enabling standard 5G NR devices to communicate with satellites that act as gNodeBs. This provides coverage in remote areas, maritime, and aviation where terrestrial networks are impractical.

Key challenges include large propagation delays (LEO satellites at 600 km altitude have ~4 ms one-way delay, GEO satellites ~130 ms), Doppler shift due to satellite mobility, and limited power/spectrum on the satellite. NTN introduces timing advance compensation, Doppler pre-compensation, and modified HARQ procedures to address these.

NTN supports both transparent and regenerative payload architectures. In transparent mode, the satellite simply relays RF signals to a ground gateway. In regenerative mode, the satellite processes NR signals onboard, reducing round-trip delay and enabling standalone satellite connectivity.

## Q31: What is network slicing resource allocation?

**A:** Network slice resource allocation involves distributing physical network resources (spectrum, compute, storage) among different slices based on Service Level Agreements (SLAs). Resources can be statically pre-allocated (guaranteed but potentially underutilized) or dynamically shared (statistical multiplexing gain but risk of contention).

Three allocation approaches exist: isolated resources (each slice gets dedicated resources, providing strict isolation), shared resources (all slices share a common pool with QoS prioritization), and hybrid (dedicated minimum resources with shared burst capacity). The choice depends on slice requirements—URLLC slices often need isolated resources for guaranteed latency.

The NSSAI (Network Slice Selection Assistance Information) identifies slices using SST (Slice/Service Type) and SD (Slice Differentiator). Standard SSTs include eMBB (1), URLLC (2), MIoT (3), V2X (4), and custom (5-127). The AMF uses NSSAI to route requests to appropriate slice instances.

## Q32: What is Network Function Virtualization (NFV) in cellular networks?

**A:** NFV decouples network functions from dedicated hardware, running them as software instances on commercial off-the-shelf (COTS) servers. Instead of proprietary appliances for MME, S-GW, or HSS, operators deploy virtual machines (VMs) or containers running virtualized network functions (VNFs/CNFs).

NFV enables rapid scaling (spin up new instances during traffic peaks), faster service deployment (instantiate new functions in minutes vs. months for hardware), and cost reduction through hardware consolidation. The ETSI NFV framework defines the NFVI (NFV Infrastructure), VIM (Virtualized Infrastructure Manager), and MANO (Management and Orchestration) stack.

In practice, NFV adoption has been uneven. While virtualized EPC functions are widespread, the performance overhead of virtualization can challenge latency-sensitive functions. Container-based CNFs (5G core) offer lighter-weight virtualization with faster startup and better resource efficiency.

## Q33: What is load balancing in cellular networks?

**A:** Load balancing distributes user traffic across cells and carriers to maximize system capacity and prevent congestion. Techniques include: cell range expansion (biasing UEs to connect to smaller cells even when they have slightly lower signal), inter-frequency load balancing (steering UEs to less loaded carriers), and inter-RAT load balancing (moving UEs between 4G and 5G).

The eNodeB/gNodeB monitors cell load through metrics like PRB utilization, number of connected users, and throughput. When a cell exceeds a load threshold, it adjusts handover parameters (cell individual offsets) to redirect new UEs to neighboring cells. This is transparent to users but can temporarily reduce their data rates during the transition.

In heterogeneous networks (HetNets), load balancing is critical because pico and femto cells have much smaller capacity than macro cells. Enhanced ICIC (eICIC) and further ICIC (feICIC) techniques coordinate transmission between macro and pico cells to manage interference during load balancing.

## Q34: What is LTE-LAA and its role in 5G?

**A:** Licensed Assisted Access (LAA) allows LTE to use the unlicensed 5 GHz band as a secondary carrier, supplementing licensed spectrum. LAA uses carrier aggregation, with the licensed band as the primary cell for control plane and the unlicensed band as the secondary cell for additional user plane capacity.

LAA implements Listen-Before-Talk (LBT) to share the unlicensed spectrum fairly with Wi-Fi. Before transmitting, the eNodeB performs a clear channel assessment (CCA); if the channel is busy, it backs off randomly. This prevents LTE from monopolizing the spectrum.

LAA evolved to MulteFire, which runs entirely in unlicensed spectrum without requiring a licensed anchor. In 5G, NR-U (NR in Unlicensed spectrum) extends these concepts with more efficient LBT procedures and supports both standalone and licensed-assisted operation in unlicensed bands.

## Q35: What is the role of the BSC in GSM?

**A:** The Base Station Controller (BSC) manages multiple BTSs in GSM networks, handling radio resource management, frequency hopping, handover control, and power control. The BSC allocates channels to calls, manages the GSM air interface (Um interface), and coordinates handovers between BTSs under its control.

The BSC connects to the BTS via the Abis interface (carrying voice and data) and to the MSC via the A interface. It performs the distribution function for voice traffic, multiplexing/demultiplexing voice channels onto the A interface.

The BSC also handles codec selection and rate adaptation, compressing voice from 13 kbps (EFR) or 12.2 kbps (AMR) to 64 kbps PCM for the PSTN. In GPRS/EDGE, the BSC additionally manages packet data through the PCU (Packet Control Unit).

## Q36: What is the purpose of IMS in LTE/5G?

**A:** The IP Multimedia Subsystem (IMS) provides a framework for delivering IP-based multimedia services over LTE/5G. IMS enables VoLTE (Voice over LTE), ViLTE (Video over LTE), RCS (Rich Communication Services), and VoNR (Voice over 5G NR). It uses SIP (Session Initiation Protocol) for session establishment and management.

IMS is architected as a set of network functions: P-CSCF (Proxy-Call Session Control Function) as the UE's SIP entry point, I-CSCF (Interrogating-CSCF) for subscriber lookup, and S-CSCF (Serving-CSCF) for session control and service logic. The HSS provides subscriber data for authentication and service authorization.

Without IMS, LTE would be a data-only network with no native voice service. VoLTE provides high-definition voice (using AMR-WB codec) with simultaneous data connectivity, replacing the circuit-switched fallback (CSFB) approach that drops the UE to 2G/3G for voice calls.

## Q37: What is Circuit-Switched Fallback (CSFB)?

**A:** CSFB is a transitional solution that allows LTE devices to make voice calls by temporarily falling back to 2G/3G circuit-switched networks. Since early LTE networks were packet-only without IMS/VoLTE, CSFB provided a path for voice service while VoLTE infrastructure was being deployed.

When a CSFB call arrives, the MME instructs the eNodeB to redirect the UE to a 2G/3G cell. The UE tunes to the circuit-switched frequency, establishes the call, and after hangup, returns to LTE. This process introduces additional call setup delay (2-5 seconds) and data interruption during the fallback.

CSFB is defined in 3GPP with two options: RRC Release with redirection (simpler but slower) and PS Handover (faster but more complex). Most operators have now migrated to VoLTE/VoNR, making CSFB increasingly obsolete, though it remains important in regions with limited VoLTE deployment.

## Q38: What is QoS in LTE/5G?

**A:** QoS in LTE is implemented through Evolved Packet System (EPS) bearers, each associated with a QoS Class Identifier (QCI). QCIs define packet delay budget, error rate, and traffic type. For example, QCI 1 (Conversational Voice) has 100 ms delay budget and 10^-3 error rate, while QCI 9 (best effort) has 300 ms delay and 10^-6 error rate.

In 5G, QoS is more granular, using QoS Flows identified by QFI (QoS Flow Identifier). Each QFI maps to specific forwarding treatment (scheduling, queue management, rate shaping). 5G defines new QoS characteristics including maximum packet error rate, maximum latency, and maximum burst size.

The PCF (Policy Control Function) in 5G core dynamically manages QoS policies based on service requirements, network conditions, and subscriber profiles. This enables per-application, per-slice, and per-user QoS differentiation.

## Q39: What is the difference between RSRP, RSRQ, and RSSI?

**A:** Reference Signal Received Power (RSRP) measures the average power of LTE reference signals across the channel bandwidth. It is the primary metric for cell selection and handover decisions, reported in dBm. Typical values range from -80 dBm (excellent) to -120 dBm (poor).

Reference Signal Received Quality (RSRQ) is the ratio of RSRP to the total received power (RSSI) measured over the same bandwidth, expressed in dB. RSRQ accounts for interference and noise, providing a quality metric independent of signal strength. It ranges from -3 dB (excellent) to -20 dB (poor).

Received Signal Strength Indicator (RSSI) is the total power measured across the entire channel bandwidth, including the desired signal, interference, and noise. RSSI is less useful for LTE because it includes pilot power, data power, and interference, making it harder to isolate the signal of interest.

## Q40: What is inter-RAT handover?

**A:** Inter-RAT (Radio Access Technology) handover is the process of transferring a UE from one radio access technology to another, such as from LTE to 3G UMTS or from 5G NR to LTE. This occurs when the serving technology's coverage is insufficient or for load balancing purposes.

The source RAT configures measurements of neighboring RAT cells (e.g., LTE measuring UMTS cells via compressed mode). When the target RAT's signal exceeds a threshold, the source RAT initiates handover. For LTE-to-3G, the MME coordinates with the 3G RNC via the Iu interface to prepare resources in the target RAT.

Inter-RAT handover is more complex than intra-RAT handover due to different air interfaces, protocol stacks, and core network elements. In 5G, inter-RAT handover between NR and LTE is common in NSA deployments, and the N26 interface between AMF and MME enables efficient handover between 5G SA and LTE.

## Q41: What is the C-RAN architecture?

**A:** C-RAN (Cloud RAN or Centralized RAN) separates the baseband processing from the radio heads. The Remote Radio Head (RRH) at the cell site handles RF transmission/reception, while the Baseband Unit (BBU) is centralized in a data center or hub site. They are connected via high-speed fronthaul (fiber carrying CPRI/eCPRI signals).

C-RAN enables pooling of baseband resources across multiple cells, improving utilization through statistical multiplexing. It also facilitates coordinated multipoint (CoMP) and coordinated scheduling since BBUs can share information with low latency over the fronthaul network.

The evolution from C-RAN to vRAN (virtualized RAN) runs BBU functions as software on general-purpose servers (O-RAN architecture). Open RAN (O-RAN) further disaggregates the RAN into interoperable components from different vendors, using open interfaces and standardized specifications.

## Q42: What is the CPRI and eCPRI interface?

**A:** Common Public Radio Interface (CPRI) is the standardized fronthaul interface between RRH and BBU. It carries digitized IQ (In-phase/Quadrature) samples in a synchronous serial stream. CPRI requires high bandwidth (e.g., ~1 Gbps per 20 MHz LTE carrier per antenna direction), making it fiber-hungry for massive MIMO deployments.

eCPRI (enhanced CPRI) is the evolution designed to reduce fronthaul bandwidth requirements. It uses packet-based transport and allows functional splits between the RRH and BBU, reducing bandwidth by up to 75% compared to CPRI. eCPRI supports Ethernet-based fronthaul, enabling statistical multiplexing and use of standard networking equipment.

The 3GPP functional split defines which baseband functions run at the RRH vs. BBU. Split 7.2x (used in O-RAN) performs FFT/IFFT and beamforming at the RRH, while higher-layer functions remain in the BBU, balancing fronthaul bandwidth and processing distribution.

## Q43: What is Network Energy Saving in 5G?

**A:** 5G networks consume significantly more energy than 4G due to massive MIMO, higher bandwidth, and denser deployments. Network energy saving techniques are critical for operational cost and sustainability. Key approaches include: cell sleep modes (turning off PA/RRH during low-traffic periods), symbol/slot shutdown (disabling specific time-domain resources), and carrier shutdown (deactivating entire carriers when not needed).

Advanced techniques use AI/ML to predict traffic patterns and proactively adjust cell configurations. The NWDAF (Network Data Analytics Function) in 5G core collects network data and provides analytics for energy optimization decisions. Machine learning models can predict traffic hotspots and configure sleep schedules accordingly.

Massive MIMO beamforming inherently saves energy by focusing power toward active users rather than broadcasting omnidirectionally. Studies show that 5G massive MIMO can be 10-15x more energy-efficient per bit than LTE, despite higher absolute power consumption.

## Q44: What is the Non-Access Stratum (NAS) protocol?

**A:** NAS is the protocol layer that handles signaling between the UE and the core network (MME in LTE, AMF in 5G), passing through the access network (eNodeB/gNodeB) transparently. NAS messages manage mobility (attach, detach, tracking area updates), session management (PDN connectivity, bearer establishment), and security (authentication, ciphering).

NAS messages are encapsulated in RRC messages for transmission over the air. They are integrity-protected and ciphered using keys derived during authentication, providing end-to-end security between the UE and core network regardless of the access network.

NAS procedures include: Attach (initial registration), TAU (tracking area update when the UE moves to a new TA), Service Request (for originating/receiving data), and Detach (deregistration). In 5G, NAS procedures are enhanced for slice selection, RRCInactive state, and deregistration with re-registration.

## Q45: What is Radio Resource Control (RRC)?

**A:** RRC is the protocol layer in the UE and eNodeB/gNodeB that manages radio resources and connection states. RRC handles system information broadcast, paging, connection establishment/release, mobility procedures (measurement configuration, handover), and radio bearer configuration.

In LTE, the UE has three RRC states: RRC_CONNECTED (active communication, network knows UE location at cell level), RRC_IDLE (no active connection, UE monitors paging, network knows UE at tracking area level), and RRC_INACTIVE (new in 5G—UE context stored in gNodeB and core, UE can quickly resume without full re-establishment).

5G RRC introduces RRC_INACTIVE state as a power-saving feature between CONNECTED and IDLE. The UE maintains its context but stops data transmission, allowing quick wake-up. RRC Resume procedure transitions from INACTIVE to CONNECTED with lower latency than a fresh RRC Setup.

## Q46: What is ProSe (Proximity Services) in LTE/5G?

**A:** ProSe enables direct device-to-device (D2D) communication between nearby UEs without routing through the network. In LTE, ProSe was introduced in Release 12 for public safety (emergency services) and commercial applications. UEs can communicate directly when within range, using sidelink radio resources.

ProSe includes two modes: ProSe Direct Communication (for data) and ProSe Direct Discovery (for finding nearby devices). Discovery usesPeriodic Announcement or Request-Response patterns. Communication uses resource allocation modes: Mode 1 (network-scheduled, eNodeB assigns resources) and Mode 2 (UE autonomous, using sensing-based selection).

In 5G, sidelink (PC5 interface) is enhanced for V2X (vehicle-to-everything) communication with support for higher data rates, lower latency, and HARQ feedback. NR sidelink supports both licensed and unlicensed spectrum, and can operate without network coverage (autonomous mode).

## Q47: What is public safety communication in cellular networks?

**A:** Public safety (PS) networks provide mission-critical voice and data for first responders (police, fire, EMS). Traditional PS networks used dedicated narrowband systems (P25, TETRA). LTE/5G broadband PS uses commercial cellular technology with dedicated priority features: Preemption Priority and Preemption Vulnerability, Dedicated Bearers, and Grant Priority.

Key features include: Proximity Services (D2D sidelink for when network infrastructure is damaged), Group Communication (one-to-many voice/data using MCPTT—Mission Critical Push-to-Talk), and Emergency Alerting (cell broadcast for public warnings).

FirstNet (US) is a dedicated PS LTE network built by AT&T, operating on Band 14 (700 MHz). It provides priority and preemption for first responders, with dedicated core network slicing. Similar networks are deployed globally (ESN in UK, SafeNet in South Korea).

## Q48: What is the purpose of the PCU in GSM/GPRS?

**A:** The Packet Control Unit (PCU) handles packet data in GSM/GPRS/EDGE networks. It manages GPRS/EDGE radio resources, performs packet scheduling, handles RLC/MAC layer functions for packet data, and interfaces between the BSC and the SGSN (Serving GPRS Support Node) via the Gb interface.

The PCU performs air interface scheduling for packet data, which is bursty and variable-rate unlike circuit-switched voice. It implements uplink and downlink TBF (Temporary Block Flow) establishment, ARQ (Automatic Repeat Request) for reliable delivery, and power control for packet transmissions.

In EDGE (Enhanced Data rates for GSM Evolution), the PCU supports higher modulation schemes (8PSK) and adaptive modulation and coding, increasing packet data throughput to 473 kbps per carrier.

## Q49: What is the Gb, Gn, and Gi interface?

**A:** The Gb interface connects the BSC (via PCU) to the SGSN in GSM/GPRS networks. It carries packet data using Frame Relay or IP transport, and supports both user plane data and control plane signaling (BSSGP protocol). The Gb interface enables GPRS packet data connectivity.

The Gn interface connects the SGSN to the GGSN (Gateway GPRS Support Node) within the same PLMN. It uses GTP (GPRS Tunneling Protocol) to tunnel user data and carry control signaling. GTP-C (control) handles tunnel management, while GTP-U (user plane) carries the actual data packets.

The Gi interface connects the GGSN to external packet data networks (the Internet, corporate networks). It is essentially an IP interface where the GGSN performs NAT, DHCP, and firewall functions. The Gi interface is the exit point from the cellular network to the public Internet.

## Q50: What is IMSI and TMSI?

**A:** The International Mobile Subscriber Identity (IMSI) is a globally unique 15-digit number stored on the SIM card that identifies the subscriber. The IMSI consists of MCC (Mobile Country Code, 3 digits), MNC (Mobile Network Code, 2-3 digits), and MSIN (Mobile Subscriber Identification Number). The IMSI is used for authentication, routing, and billing.

For security, the IMSI is rarely transmitted over the air after initial attach. Instead, the network assigns a Temporary Mobile Subscriber Identity (TMSI), a 32-bit random number that identifies the UE within a location area (LA) or tracking area (TA). The TMSI is reallocated periodically and when the UE moves to a new area, preventing IMSI tracking.

In 5G, the SUPI (Subscription Permanent Identifier, equivalent to IMSI) is encrypted using the home network's public key before transmission, creating an SUCI (Subscription Concealed Identifier). This protects subscriber privacy against passive eavesdroppers, addressing a known vulnerability in 2G/3G/LTE.

## Q51: What is CDMA2000 and its evolution path?

**A:** CDMA2000 is the 3G evolution of the IS-95 (cdmaOne) family, standardized by 3GPP2. CDMA2000 1xRTT provides 1.25 MHz channel bandwidth and 153 kbps peak data rate. CDMA2000 EV-DO (Evolution-Data Optimized) introduced a separate 1.25 MHz carrier dedicated to data, using adaptive modulation and scheduling to achieve 2.4 Mbps (Rev 0) and 3.1 Mbps (Rev A) peak downlink rates.

CDMA2000 EV-DO uses time-division multiplexing on the downlink—the base station schedules one user per time slot with the best channel conditions, exploiting multiuser diversity. The uplink uses CDMA. EV-DO Rev B aggregated multiple carriers for higher throughput.

CDMA2000 evolved through Rev 0, Rev A, Rev B, and Rev C (UMB—Ultra Mobile Broadband). However, UMB was never commercially deployed as Qualcomm and most CDMA2000 operators migrated to LTE instead.

## Q52: What is the difference between TDD and FDD?

**A:** Frequency Division Duplex (FDD) uses separate frequency bands for uplink and downlink, allowing simultaneous transmission. It requires paired spectrum and a duplex filter to separate the bands. FDD is preferred for symmetric traffic (voice) and wide-area coverage, providing consistent performance in both directions.

Time Division Duplex (TDD) uses the same frequency for uplink and downlink, alternating in time. TDD requires unpaired spectrum and can dynamically adjust the uplink/downlink ratio based on traffic demand. This asymmetry is advantageous for data-heavy applications (more downlink than uplink).

TDD has inherent latency advantages since there is no need to switch between frequencies. However, TDD requires precise time synchronization across base stations to prevent inter-cell interference, and has lower spectral efficiency for symmetric traffic. 5G NR supports both FDD and TDD, with TDD being dominant in mid-band deployments (C-band, 2.5 GHz).

## Q53: What is NOMA in 5G?

**A:** Non-Orthogonal Multiple Access (NOMA) serves multiple users on the same time-frequency resource by superimposing their signals with different power levels. The transmitter assigns higher power to users with weaker channels and lower power to users with stronger channels. The receiver uses Successive Interference Cancellation (SIC) to decode and remove the stronger signal first, then decode the weaker signal.

NOMA provides higher spectral efficiency than orthogonal schemes (OFDMA) by exploiting the power domain in addition to time and frequency. It also improves fairness by allowing cell-edge users (with weak channels) to share resources with cell-center users.

Candidate NOMA waveforms for 5G included SCMA (Sparse Code Multiple Access), MUSA (Multi-User Shared Access), and IDMA (Interleave Division Multiple Access). However, 3GPP ultimately did not standardize NOMA in 5G NR, favoring advanced MU-MIMO as the primary spectral efficiency enhancement technique.

## Q54: What is the SDAP protocol in 5G?

**A:** Service Data Adaptation Protocol (SDAP) is a new layer in the 5G NR user plane that maps QoS flows to data radio bearers (DRBs). SDAP operates between the PDCP layer and the RLC layer, providing a flexible mapping between the rich QoS framework of the 5G core (QFI-based) and the limited number of DRBs available over the air interface.

SDAP header includes a QFI field (6 bits) and a reflector indicator. The reflector enables the UE to mirror the QoS-to-DRB mapping learned from downlink traffic when transmitting uplink, reducing signaling overhead.

Multiple QoS flows can be mapped to a single DRB (multiplexing), or a single QoS flow can use multiple DRBs. This flexibility is essential for network slicing, where different slices may have different QoS requirements but share the same radio resources.

## Q55: What is beam management in 5G mmWave?

**A:** Beam management is the process of establishing, maintaining, and recovering directional beam pairs between the gNodeB and UE in mmWave frequencies. Since mmWave signals suffer severe path loss, directional transmission with high-gain antennas is essential for establishing link budget.

The beam management procedure includes: Beam Sweeping (gNodeB transmits SSBs—Synchronization Signal Blocks in different directions using predefined beam patterns), Beam Measurement (UE measures RSRP/RSRQ for each SSB beam), Beam Reporting (UE reports best beam indices to gNodeB), and Beam Tracking (continuous monitoring to adapt beams as UE moves).

For initial access, the gNodeB periodically transmits SSB bursts with up to 64 beams. The UE scans these beams and selects the best one. After connection, the gNodeB can use CSI-RS (Channel State Information Reference Signals) for finer beam refinement. Beam failure can occur due to blockage; the UE detects this via beam failure detection and initiates beam recovery using random access with beam-specific preambles.

## Q56: What is the RLC layer in LTE/5G?

**A:** The Radio Link Control (RLC) layer sits between PDCP and MAC, providing segmentation, reassembly, and error correction services. RLC operates in three modes: Transparent Mode (TM—no overhead, used for broadcast), Unacknowledged Mode (UM—segmentation/reassembly without retransmission, used for real-time services), and Acknowledged Mode (AM—segmentation with ARQ for reliable delivery).

In AM, the receiver detects missing RLC PDUs through sequence numbers and requests retransmission via NAK (Negative Acknowledgment) messages. The transmitter maintains a retransmission buffer until positive acknowledgment is received. This provides high reliability but adds latency.

5G NR RLC is simplified compared to LTE. The reordering functionality moved from RLC to PDCP, reducing RLC buffer requirements. The RLC also supports status reporting based on polling and triggered by buffer status, improving retransmission efficiency.

## Q57: What is the PDCP layer's role?

**A:** The Packet Data Convergence Protocol (PDCP) layer handles header compression (using ROHC—Robust Header Compression), ciphering, integrity protection, and reordering/repetition detection. PDCP operates on RLC service data units (SDUs) and delivers to upper layers.

PDCP maintains separate entity instances for each radio bearer (DRB). For each bearer, it applies the security functions (encryption and integrity protection) using keys derived from the authentication process. ROHC compresses IP/UDP/RTP headers from ~40 bytes to 2-4 bytes, significantly improving spectral efficiency for voice and video.

During handover, PDCP performs packet forwarding (forwarding unacknowledged PDUs from source to target gNodeB) and reordering (ensuring correct sequence after handover). In 5G, PDCP duplication allows transmitting the same PDCP PDU on multiple DRBs for reliability in URLLC scenarios.

## Q58: What is HARQ and how does it work?

**A:** Hybrid Automatic Repeat Request (HARQ) is the fast retransmission mechanism at the MAC layer. When a transport block is received with errors, the receiver requests retransmission via NACK. The transmitter sends additional redundancy (incremental redundancy) or a copy (chase combining) of the failed transmission. The receiver combines the retransmission with previous attempts to improve decoding probability.

HARQ operates at the MAC layer with very fast turnaround (typically 8-10 ms in LTE, ~4 ms in 5G). Each HARQ process maintains a circular buffer of transmitted and received blocks. The number of HARQ processes determines the pipeline depth—for LTE FDD, 8 processes; for 5G, up to 16.

Soft combining combines the received signal from multiple transmission attempts. Chase Combining (CC) retransmits the identical codeword, and the receiver combines them at symbol level. Incremental Redundancy (IR) retransmits different parity bits, providing additional coding gain. IR is preferred as it achieves higher throughput with fewer retransmissions.

## Q59: What is the MAC layer's role in LTE/5G?

**A:** The Medium Access Control (MAC) layer handles multiplexing/demultiplexing of logical channels, HARQ retransmission, random access, and scheduling (in the UE). The MAC layer maps logical channels (DCCH, DTCH) to transport channels (DL-SCH, UL-SCH), which are then mapped to physical channels.

Key MAC functions include: UL scheduling (the gNodeB sends Uplink Grants specifying which resources the UE can use), DL scheduling (the gNodeB schedules downlink resources and signals via PDCCH), buffer status reporting (UE reports its buffer status to enable efficient scheduling), and power headroom reporting (UE reports available transmit power).

In 5G, the MAC layer supports mini-slot scheduling (2, 4, or 7 OFDM symbols) for low latency, configurable HARQ timing, and grant-free uplink for URLLC. The MAC also handles the BSR (Buffer Status Report) and SR (Scheduling Request) procedures.

## Q60: What is SDN in the context of cellular networks?

**A:** Software-Defined Networking (SDN) decouples the control plane from the user plane in network infrastructure. In cellular networks, SDN principles apply to both the transport/backhaul network and the mobile core. SDN controllers centrally manage routing, traffic engineering, and network policies, replacing distributed routing protocols.

For the mobile backhaul, SDN enables dynamic path selection, traffic slicing, and quality of service enforcement across the transport network connecting base stations to the core. This is critical for C-RAN/fronthaul networks where latency and jitter requirements are stringent.

In the mobile core, SDN integrates with NFV to orchestrate network functions and their interconnections. The 5G SBA architecture aligns with SDN principles, using centralized orchestration for network function deployment and service chaining. Open RAN also adopts SDN principles for RAN intelligent control.

## Q61: What is the difference between 3GPP and 3GPP2?

**A:** 3GPP (3rd Generation Partnership Project) develops standards for GSM, UMTS, LTE, and 5G NR. It is the dominant standards body, with member organizations from Europe, Asia, and the Americas. 3GPP specifications are organized into releases (Rel-99 through Rel-18+), each introducing new features.

3GPP2 (3rd Generation Partnership Project 2) developed standards for CDMA-based systems: IS-95 (cdmaOne), CDMA2000, and EV-DO. 3GPP2 was more influential in North America, South Korea, and Japan where CDMA was deployed. However, the industry converged on 3GPP technologies for 4G/5G.

The competition between 3GPP and 3GPP2 was significant in the 2000s, with different operators and vendors backing each camp. The decisive shift to LTE (a 3GPP standard) ended this bifurcation, and 3GPP2 has become largely inactive for new development.

## Q62: What is a Tracking Area in LTE?

**A:** A Tracking Area (TA) is a grouping of cells used for UE paging and location management in LTE. When a UE in RRC_IDLE state moves to a new TA, it performs a Tracking Area Update (TAU) to inform the network. The MME maintains a list of TAs in a Tracking Area List (TAL) assigned to each UE.

The TAL can include multiple TAs, reducing TAU frequency for UEs at TA boundaries. The MME pages the UE in all cells of its registered TAs when a downlink packet arrives. Smaller TAs reduce paging load (fewer cells to page per TA) but increase TAU signaling; larger TAs have the opposite effect.

In 5G, the concept extends to Radio Access Networks with Registration Areas. The AMF assigns a list of Registration Areas, and the UE performs Registration Area Update when moving between areas. 5G also introduces the RRC_INACTIVE state, where the UE monitors paging in a subset of cells (RAN-based paging area).

## Q63: What is CoMP in LTE-Advanced?

**A:** Coordinated Multipoint (CoMP) is a set of techniques where multiple geographically separated transmission/reception points coordinate their transmissions to improve cell-edge performance and overall system throughput. CoMP types include: Joint Transmission (multiple points transmit the same data simultaneously), Dynamic Point Selection (selecting the best point per TTI), and Coordinated Scheduling (coordinating scheduling decisions across points).

Joint Transmission combines signals from multiple eNodeBs, creating constructive interference at the UE. This turns inter-cell interference into useful signal. Dynamic Point Selection switches the serving point rapidly based on channel conditions. Coordinated Scheduling avoids simultaneous transmission to cell-edge users on the same resources.

CoMP requires low-latency backhaul between coordinating points and accurate channel state information. In practice, CoMP complexity and backhaul requirements limited its deployment. 5G enhances this concept through network MIMO and distributed MIMO with tighter coordination.

## Q64: What is HetNet (Heterogeneous Network)?

**A:** A HetNet combines multiple layers of cells with different sizes and capabilities: macro cells for wide-area coverage, micro cells for urban hotspots, pico cells for indoor/venue coverage, and femto cells for home/small business. This hierarchical deployment increases capacity where needed while maintaining coverage.

HetNets introduce challenges: interference between layers (macro-to-pico interference), uneven load distribution (macro cells may be overloaded while pico cells are underutilized), and complex mobility (handover between different cell layers).

Solutions include enhanced ICIC (eICIC) using Almost Blank Subframes (ABS) where macro cells reduce transmission power during specific subframes to protect pico cell transmissions. Cell Range Expansion (CRE) biases UEs to connect to pico cells even when macro signal is stronger, balancing load at the cost of increased interference.

## Q65: What is the difference between cell selection and cell reselection?

**A:** Cell selection occurs when the UE powers on or recovers from out-of-service. The UE scans all supported frequencies, reads system information blocks (SIBs), and selects a cell based on signal quality (RSRP > threshold) and suitable PLMN. The selection uses S-criteria: RSRP > Qrxlevmin + Qoffset, where Qrxlevmin is the minimum required level and Qoffset accounts for cell barring and offsets.

Cell reselection occurs when the UE is camped on a cell in RRC_IDLE state. The UE continuously monitors serving and neighbor cell quality using measurements. The reselection uses ranking criteria: the UE ranks cells based on R-criteria (RSRP + cell priority/offset) and selects the highest-ranked cell after a evaluation timer expires.

Cell reselection priorities are broadcast in SIB5 (inter-frequency) and can be configured by the operator for load balancing. Higher priority frequencies are always attempted first, regardless of current cell quality. In 5G, cell reselection is enhanced for NR frequencies and supportsRRC_INACTIVE state measurements.

## Q66: What is the GTP protocol?

**A:** GPRS Tunneling Protocol (GTP) tunnels user data packets between GPRS network elements. GTP-U (user plane) encapsulates user IP packets with a GTP header containing tunnel endpoint identifiers (TEIDs) that identify the specific tunnel. Each UE/bearer combination has unique TEIDs for identification.

GTP-C (control plane) manages tunnel establishment, modification, and deletion. It uses message types like Create PDP Context Request/Response, Update PDP Context, and Delete PDP Context. GTP-C also handles path management (echo request/response) and error indication.

In LTE, GTP-C operates between eNodeB and S-GW (S11 interface) and between S-GW and P-GW (S5/S8 interface). GTP-U carries user data on S1-U, S5/S8-U, and S12 interfaces. 5G continues to use GTP-U for N3 (gNodeB to UPF) and N9 (UPF to UPF) interfaces.

## Q67: What is the Diameter protocol?

**A:** Diameter is the authentication, authorization, and accounting (AAA) protocol used in LTE's EPC. It evolved from RADIUS and uses TCP/SCTP transport (vs. RADIUS's UDP). Diameter supports reliable delivery, capability negotiation, and extensibility through vendor-specific attributes.

Key Diameter interfaces in EPC: S6a (MME to HSS for authentication and subscriber data), S6d (SGSN to HSS), S13 (MME to MME/SGSN for IMEI checking), and Cx/Dx (IMS elements to HSS). Diameter is also used for policy and charging via Gx (PCRF to P-GW), Rx (PCRF to AF), and SWx (ePDG to AAA server).

5G core replaces Diameter with HTTP/2-based service interfaces, aligning with the SBA approach. However, Diameter remains in use during the transition period, particularly for interworking between 5G and legacy networks.

## Q68: What is the X2 interface?

**A:** The X2 interface connects eNodeBs in LTE, supporting handover, load management, and inter-cell interference coordination. During handover, the source eNodeB uses the X2 interface to forward buffered packets and UE context to the target eNodeB, enabling seamless continuity.

X2AP (X2 Application Protocol) defines procedures including: Handover Request, Load Information (exchange of cell load metrics), Resource Status Request/Response (periodic load reporting), and Mobility Parameters Exchange (for handover optimization).

In 5G, the Xn interface replaces X2, connecting gNodeBs and optionally eNodeBs. XnAP supports similar functions plus additional procedures for dual connectivity, RRC state management, and information exchange between NR and LTE nodes. Xn is critical for NSA 5G deployments using EN-DC.

## Q69: What is the S1 interface?

**A:** The S1 interface connects eNodeBs to the EPC in LTE. It is divided into S1-MME (control plane to MME) and S1-U (user plane to S-GW). S1AP (S1 Application Protocol) handles procedures including Initial Context Setup (establishing UE context at the eNodeB), UE Context Release, Handover (S1-based handover via MME), and Paging.

S1 flexibility is provided by S1-Flex, where an eNodeB can connect to multiple MMEs within an MME pool area. Load balancing among MMEs is achieved by distributing UE associations across available MMEs. This provides redundancy and load sharing.

In 5G, the N2 (control) and N3 (user plane) interfaces replace S1-MME and S1-U. They connect gNodeBs to the AMF and UPF respectively. The interfaces use similar protocols but with 5G-specific message sets supporting features like network slicing, dual connectivity, and RRC_INACTIVE.

## Q70: What is power control in LTE/5G?

**A:** Power control adjusts UE and eNodeB transmit power to maintain target received signal quality while minimizing interference. LTE uplink power control uses the formula: P = min(Pmax, P0 + 10log10(M) + alpha*PL + delta), where P0 is a target received power, M is allocated bandwidth, PL is path loss, and alpha is fractional power control factor.

Uplink power control serves multiple purposes: compensating for path loss variations, managing near-far interference (cells at cell edge transmit at higher power, reducing interference to neighboring cells), and reducing UE power consumption (near-cell UEs transmit at lower power).

Downlink power control is performed by the eNodeB through power boosting of reference signals and PBCH, and dynamic power allocation across resource blocks. In 5G, power control is enhanced with per-beam power allocation for massive MIMO and support for multiple power classes including high-power UE (HPUE) for extended coverage.

## Q71: What is the difference between IMSI, IMEI, and MSISDN?

**A:** IMSI (International Mobile Subscriber Identity) uniquely identifies the subscriber, stored on the SIM/UICC. It is used for network authentication, routing, and billing. The IMSI is a 15-digit number composed of MCC, MNC, and MSIN.

IMEI (International Mobile Equipment Identity) uniquely identifies the device hardware, stored in the device itself. It is a 15-digit number with TAC (Type Allocation Code, 8 digits), serial number (6 digits), and check digit (1 digit). The IMEI is used for device identification, blacklisting stolen devices, and device-specific policy enforcement.

MSISDN (Mobile Station International Subscriber Directory Number) is the phone number—the number dialed to reach the subscriber. It is a separate database entry in the HSS/HLR, as a subscriber may have multiple MSISDNs (for voice, fax, data). The mapping between IMSI and MSISDN is maintained in the subscriber profile.

## Q72: What is Single-RAN (SRAN)?

**A:** Single-RAN allows multiple radio access technologies (2G, 3G, 4G, 5G) to coexist on the same hardware platform. Instead of separate equipment for each generation, operators deploy one set of equipment supporting all technologies. This reduces site footprint, power consumption, and operational complexity.

SRAN base stations share the same rack, power supply, cooling, and backhaul connection. They may use separate or shared RF modules depending on frequency bands. The software is upgradeable to support new technologies without hardware replacement—for example, enabling 5G NR on existing 4G equipment through software updates.

SRAN facilitates smooth technology migration. Operators can gradually shift traffic from 2G/3G to 4G/5G while maintaining legacy support. When a generation is retired, software deactivation releases resources for other technologies.

## Q73: What is the NB-IoT technology?

**A:** Narrowband Internet of Things (NB-IoT) is a low-power wide-area (LPWA) technology standardized in 3GPP Release 13. It uses a single 180 kHz LTE resource block (or standalone carrier) optimized for IoT applications requiring deep indoor coverage, long battery life, and massive connection density.

NB-IoT provides ~20 dB link budget improvement over LTE through repetition (transmitting the same data multiple times), lower data rate (250 kbps peak), and simplified protocol stack. It supports three deployment modes: standalone (dedicated spectrum), in-band (within an LTE carrier), and guard-band (in the LTE guard band).

NB-IoT is optimized for small, infrequent data transmissions (e.g., smart meters, sensors). Devices can enter deep sleep (PSM—Power Saving Mode) for months or years, waking periodically to transmit data. It targets 10-15 year battery life with 2 AA batteries.

## Q74: What is the difference between LTE-M and NB-IoT?

**A:** LTE-M (LTE Cat-M1) is a low-cost, low-power LTE variant with 1 Mbps peak data rate and 1.4 MHz bandwidth. It supports voice (VoLTE), mobility (handover), and full-duplex communication. LTE-M retains LTE protocol structure, enabling simpler device development and faster time-to-market.

NB-IoT has lower data rate (250 kbps), narrower bandwidth (180 kHz), and does not support voice or handover. NB-IoT provides better link budget (+20 dB over LTE-M) for deeper coverage. Both target IoT but serve different use cases.

LTE-M is suitable for applications requiring mobility and moderate data rates: asset tracking, wearables, point-of-sale terminals. NB-IoT suits stationary applications with minimal data: smart meters, environmental sensors, agricultural monitoring. Both use licensed spectrum, providing reliability and QoS guarantees compared to unlicensed LPWA technologies like LoRa.

## Q75: What is network energy efficiency in 5G?

**A:** 5G improves energy efficiency per bit transmitted through several mechanisms. Massive MIMO beamforming concentrates transmit power toward intended users, reducing wasted energy. Advanced sleep modes turn off circuit components during idle periods—micro-sleep (symbol-level), deep-sleep (carrier-level), and hibernation (site-level).

AI-driven energy management uses the NWDAF to analyze traffic patterns and predict optimal sleep schedules. Machine learning models can turn off cell layers during low-traffic periods, adjust Massive MIMO beams to reduce PA power consumption, and coordinate sleep across neighboring cells to prevent coverage gaps.

The O-RAN Alliance's Energy Savings use case defines closed-loop automation for energy optimization. The RAN Intelligent Controller (RIC) collects RAN metrics, trains optimization models, and applies energy-saving actions in near-real-time (xApps) and non-real-time (rApps).

## Q76: What is the O-RAN architecture?

**A:** Open RAN (O-RAN) disaggregates the traditional RAN into interoperable components using open interfaces. The architecture separates the Radio Unit (RU), Distributed Unit (DU), and Centralized Unit (CU). The CU further splits into CU-CP (Control Plane) and CU-UP (User Plane). These components can be from different vendors, connected via open interfaces (E2, A1, O1, Open Fronthaul).

The RAN Intelligent Controller (RIC) provides programmability. The Near-RT RIC runs xApps that control RAN functions at 10-1000 ms timescales (beam management, scheduling assistance). The Non-RT RIC runs rApps for optimization at >1 second timescales (energy savings, mobility optimization, network slicing).

O-RAN enables operators to avoid vendor lock-in, mix best-of-breed components, and deploy third-party innovation (AI/ML apps). It also supports cloud-native deployment of DU/CU functions on general-purpose hardware.

## Q77: What is the N26 interface in 5G?

**A:** The N26 interface connects the 5G AMF to the 4G MME, enabling inter-system handover between 5G NR and LTE. When a UE in 5G SA moves to an area with only LTE coverage, the AMF uses N26 to transfer the UE's context (security keys, bearer information, subscriber data) to the MME, which then establishes the UE in LTE.

N26 supports both handover and idle-mode mobility (inter-system TAU). For handover, the target RAT prepares resources before the UE transitions, minimizing service interruption. For idle-mode mobility, the UE reselects to LTE and performs a TAU procedure, with the MME retrieving context via N26.

N26 is optional in 5G deployments. When N26 is not available, inter-system mobility requires full re-attachment to the target network, which increases latency and service interruption. Operators deploying 5G SA often implement N26 to ensure seamless interworking with their existing LTE networks.

## Q78: What is IMS emergency calling?

**A:** IMS emergency calling provides voice service to emergency numbers (911, 112, 999) even when the UE is not normally registered. When the UE dials an emergency number, it performs an emergency attach procedure, establishing a minimal IMS session for voice communication with the PSAP (Public Safety Answering Point).

Emergency calls use dedicated QCIs (typically QCI 1 for conversational voice) with highest priority and preemption capability. The network ensures the call reaches the correct PSAP based on the UE's location, which is more complex for VoLTE than for circuit-switched emergency calls.

E911/ELRS (Enhanced Location Reporting System) requires the UE to provide its location with the emergency call. In 5G, positioning methods (DL-TDoA, Multi-RTT) provide meter-level accuracy, addressing the FCC's requirements for indoor location accuracy.

## Q79: What is the difference between SA and NSA 5G?

**A:** Non-Standalone (NSA) 5G uses the existing 4G LTE core network (EPC) for control plane functions, while adding 5G NR carriers for user plane capacity. The most common NSA option is Option 3x, where the LTE eNodeB is the master node (handling RRC, S1-MME) and the NR gNodeB is the secondary node (providing additional data throughput via EN-DC).

Standalone (SA) 5G uses the full 5G core (5GC) with new network functions (AMF, SMF, UPF, etc.). SA enables all 5G features: network slicing, URLLC, massive MIMO optimization, edge computing integration, and reduced latency through the new core and NR air interface.

SA deployment is the end goal but requires new core network investment and coverage buildout. NSA is a transitional approach that leverages existing LTE infrastructure for faster 5G deployment. Most operators started with NSA and are gradually migrating to SA.

## Q80: What is positioning in 5G?

**A:** 5G NR supports high-accuracy positioning for applications like autonomous driving, industrial automation, and asset tracking. 3GPP Release 16 defines positioning methods achieving sub-meter accuracy in outdoor and indoor environments.

Methods include: DL-TDoA (Downlink Time Difference of Arrival) using PRS (Positioning Reference Signals) from multiple gNodeBs, Multi-RTT (Multi-Round Trip Time) measuring round-trip time to multiple gNodeBs, DL-AoD (Angle of Downlink Departure) estimating angle from gNodeB to UE, and UL-AoA (Angle of Arrival) estimating angle from UE to gNodeB.

5G positioning benefits from wider bandwidth (higher time resolution), massive MIMO (better angle estimation), and higher carrier frequencies (shorter wavelength for compact antenna arrays). Release 17 adds carrier phase positioning for centimeter-level accuracy.

## Q81: What is the role of the MME in LTE?

**A:** The Mobility Management Entity (MME) is the primary control plane node in the LTE EPC. It handles NAS signaling with UEs, manages authentication (coordinating with HSS), performs bearer management (establishing/modifying/deleting EPS bearers), and controls mobility (handover decisions, tracking area management).

The MME processes initial attach requests, performs authentication using vectors from HSS, allocates globally unique temporary identities (GUTIs), and manages security contexts. During handover, the MME coordinates resource preparation in the target eNodeB and manages the handover execution.

In the EPC architecture, the MME interfaces with: S-GW (S11 for bearer management), HSS (S6a for subscriber data), eNodeB (S1-MME for RAN signaling), and SGs (for CSFB to 2G/3G). The MME also handles S1-flex, distributing UE associations across multiple eNodeBs in pool areas.

## Q82: What is the Serving Gateway (S-GW) role?

**A:** The Serving Gateway (S-GW) is the user plane anchor in LTE EPC, routing and forwarding IP packets between the eNodeB and PDN Gateway. The S-GW acts as the mobility anchor for inter-eNodeB handovers, maintaining the user plane connection as the UE moves between cells.

For downlink data, the S-GW buffers packets when the UE is in idle state, triggering the MME to page the UE. For uplink data, the S-GW forwards packets to the P-GW. The S-GW also performs lawful intercept, packet inspection for usage reporting, and QoS enforcement.

S-GW selection is based on UE location and proximity. The MME selects the S-GW during attach based on the UE's TAI. S-GW relocation occurs when the UE moves to a new tracking area, but this is transparent to the UE as the user plane is maintained through tunnel endpoint updates.

## Q83: What is the PDN Gateway (P-GW) role?

**A:** The PDN Gateway (P-GW) connects the LTE network to external packet data networks (the Internet, corporate networks, IMS). It performs IP address allocation (via DHCP or static assignment), packet filtering (firewall, deep packet inspection), and policy enforcement (QoS, charging).

The P-GW is the policy enforcement point for EPS bearers, applying QoS parameters (QCI, MBR, GBR) to user traffic. It also performs traffic shaping, rate limiting, and content filtering based on policies from the PCRF (Policy and Charging Rules Function).

In 5G, the P-GW functionality is split between the SMF (control plane session management) and UPF (user plane forwarding). This separation enables more flexible deployment—UPFs can be distributed to the edge while SMF remains centralized.

## Q84: What is the PCRF in LTE?

**A:** The Policy and Charging Rules Function (PCRF) is the policy decision point in the LTE EPC. It determines QoS policies and charging rules for each subscriber and service. The PCRF receives information from the AF (Application Function) via Rx interface and from the P-GW via Gx interface.

Based on service requirements and subscriber profiles, the PCRF generates PCC (Policy and Charging Control) rules: which QCI to assign, what MBR/GBR to apply, and how to charge (online or offline). These rules are installed in the P-GW via Gx, which enforces them on the user plane.

In 5G, the PCRF is replaced by the PCF (Policy Control Function), which operates within the SBA framework. The PCF uses standardized APIs and integrates with other network functions for dynamic policy decisions. The 5G PCF supports slice-specific policies, application-aware QoS, and enhanced charging integration.

## Q85: What is the difference between GBR and non-GBR bearers?

**A:** Guaranteed Bit Rate (GBR) bearers reserve dedicated bandwidth that is guaranteed for the lifetime of the bearer. GBR bearers are used for real-time services like voice (QCI 1), video conferencing (QCI 2), and real-time gaming (QCI 3). The network reserves resources at the radio interface and core network to ensure the guaranteed rate.

Non-GBR bearers do not reserve dedicated bandwidth; they share available resources with other non-GBR bearers. Non-GBR bearers are used for best-effort services like web browsing (QCI 8/9), email, and social media. The actual throughput depends on current load and available resources.

In 5G, the distinction extends to QoS flows. GBR QoS flows have guaranteed resources, while Non-GBR flows share available capacity. 5G introduces Delay-Critical GBR (DC-GBR) for URLLC services that require both guaranteed bandwidth and low latency.

## Q86: What is the CSFB procedure in detail?

**A:** When an incoming call arrives for a CSFB-capable UE, the MSC pages the UE via the SGs interface to the MME. The MME sends a Paging message to the UE. If the UE is in RRC_IDLE, it establishes a connection and receives the Extended Service Request containing CSFB indication.

The eNodeB then initiates redirection or handover to a 2G/3G cell. For redirection, the eNodeB releases the RRC connection with a redirectCarrierInfo IE specifying the target frequency. For handover, the eNodeB performs Inter-RAT handover preparation with the target RAN.

The UE tunes to the 2G/3G frequency, performs random access, and establishes the voice call. After call termination, the UE returns to LTE, performing a TAU to re-register. The entire process adds 2-5 seconds to call setup time compared to VoLTE.

## Q87: What is the meaning of QCI values?

**A:** QCI values define standardized QoS characteristics for EPS bearers. QCI 1 (GBR, 100 ms delay, 10^-3 error rate) for conversational voice. QCI 2 (GBR, 150 ms, 10^-3) for conversational video. QCI 3 (GBR, 50 ms, 10^-3) for real-time gaming. QCI 4 (GBR, 300 ms, 10^-6) for non-conversational video (buffered streaming).

Non-GBR QCIs: QCI 5 (Non-GBR, 100 ms, 10^-6) for IMS signaling. QCI 6 (Non-GBR, 300 ms, 10^-6) for TCP-based services (email, chat, file transfer). QCI 7 (Non-GBR, 100 ms, 10^-3) for voice, video, interactive streaming. QCI 8 (Non-GBR, 300 ms, 10^-6) for interactive video. QCI 9 (Non-GBR, 300 ms, 10^-6) for best-effort data.

In 5G, QFI (QoS Flow Identifier) replaces QCI with additional parameters: maximum packet delay, maximum packet error rate, maximum burst size, and traffic handling priority. 5G QoS is more granular and application-aware.

## Q88: What is the purpose of SIBs in LTE?

**A:** System Information Blocks (SIBs) broadcast cell-specific parameters that UEs need for network access. SIB1 contains cell selection parameters, scheduling information for other SIBs, and PLMN identity. SIB2 contains radio resource configuration (RACH config, paging, uplink power control).

SIB3 contains intra-frequency and inter-frequency cell reselection parameters. SIB4/5 provide neighbor cell lists for intra/inter-frequency reselection. SIB6/7/8 carry ETWS (Earthquake and Tsunami Warning System) and CMAS (Commercial Mobile Alert System) messages.

SIBs are broadcast on DL-SCH, mapped to PBCH (MIB) or PDSCH (SIBs). The acquisition information is provided in MIB and SIB1, allowing UEs to decode subsequent SIBs. SIB transmission is periodic, with configurable periodicity (80 ms to 560 ms).

## Q89: What is the purpose of SRS in LTE/5G?

**A:** Sounding Reference Signals (SRS) are uplink reference signals transmitted by the UE to enable the eNodeB/gNodeB to estimate uplink channel quality across the bandwidth. SRS is used for uplink scheduling (assigning resource blocks where the UE has good channel conditions), antenna switching (determining which antenna ports provide the best uplink), and uplink beamforming.

SRS is transmitted periodically or aperiodically on the last symbol(s) of a slot. The eNodeB configures SRS parameters: bandwidth, comb offset, cyclic shift, and periodicity. The eNodeB can sound different parts of the bandwidth over time to cover the full system bandwidth.

In 5G NR, SRS is enhanced for massive MIMO with support for more antenna ports, aperiodic SRS for on-demand channel estimation, and uplink beam management. SRS is also used for uplink channel reciprocity-based beamforming in TDD systems.

## Q90: What is the meaning of EIRP and EIRPD?

**A:** EIRP (Equivalent Isotropically Radiated Power) is the total power that a theoretical isotropic antenna would need to radiate to produce the same peak power density as the actual antenna in its direction of maximum gain. EIRP = Transmit Power + Antenna Gain - Cable Losses (in dB). It represents the maximum effective power radiated in any direction.

EIRPD (Equivalent Isotropically Radiated Power Density) is EIRP per unit bandwidth, typically expressed in dBm/Hz or dBm/MHz. It accounts for the signal bandwidth and is important for regulatory compliance, as spectrum regulators often set limits in dBm/100 kHz or dBm/MHz.

In 5G NR, especially for mmWave, EIRP can be very high due to massive MIMO beamforming gain. A 64-element antenna array provides ~18 dBi gain, and with 30 dBm transmit power, the EIRP can reach ~48 dBm (63 W) per beam. Regulatory limits (FCC, ETSI) define maximum EIRP for each band.

## Q91: What is the difference between SRB0, SRB1, and SRB2?

**A:** Signaling Radio Bearers (SRBs) carry RRC and NAS messages between the UE and network. SRB0 uses the CCCH (Common Control Channel) for initial RRC messages during connection setup, before security is activated. SRB0 uses the same MAC header as DRBs but with a CCCH logical channel.

SRB1 carries RRC messages (including NAS messages piggybacked on RRC) after security is activated. SRB1 is established during the RRC Connection Setup procedure and uses the DCCH (Dedicated Control Channel). Integrity protection and ciphering are applied to SRB1 messages.

SRB2 carries NAS messages dedicated to EMM/ESM (LTE) or 5GMM/5GSM (5G). SRB2 is established after security activation and runs parallel to SRB1 but with lower priority. NAS messages on SRB2 are ciphered but not integrity-protected at RRC level (NAS handles its own integrity).

## Q92: What is the meaning of TTI bundling?

**A:** TTI (Transmission Time Interval) bundling transmits the same transport block across multiple consecutive TTIs without waiting for HARQ feedback between each TTI. In LTE, TTI bundling sends 4 consecutive subframes with different redundancy versions, allowing the receiver to soft-combine all transmissions for improved reception.

TTI bundling is used at cell edge where the UE is power-limited and a single TTI transmission may not provide sufficient received quality. By bundling multiple TTIs, the UE achieves a coverage gain of approximately 2-3 dB compared to a single TTI transmission with HARQ retransmissions.

In 5G NR, TTI bundling is replaced by PUSCH repetition (Type A and Type B). PUSCH repetitions provide similar coverage enhancement but with more flexibility in number of repetitions (1-256) and resource allocation.

## Q93: What is the role of the SGs interface?

**A:** The SGs interface connects the MME to the MSC/VLR in the circuit-switched core network, enabling CSFB and SMS services. For CSFB, the SGs interface carries paging messages from the MSC to the MME and location area information from the MME to the MSC.

For SMS, the SGs interface carries SMS messages between the UE (via NAS) and the MSC, allowing SMS delivery over LTE without falling back to 2G/3G. The UE sends SMS via NAS messages to the MME, which forwards them to the MSC via SGs.

The SGs interface also supports combined attach/detach procedures, where the UE registers with both the packet-switched (via MME) and circuit-switched (via MSC) networks simultaneously. This enables the network to page the UE for circuit-switched services via LTE.

## Q94: What is VoNR and how does it differ from VoLTE?

**A:** Voice over New Radio (VoNR) is voice service delivered natively over 5G NR without falling back to LTE. VoNR uses the same IMS framework as VoLTE but with NR as the access technology. The NR air interface provides lower latency and higher quality for voice packets compared to LTE.

VoNR benefits from NR's lower latency (mini-slot scheduling reduces voice packet delay), improved spectral efficiency (massive MIMO provides better SNR), and native 5G QoS (5QI-based QoS flows provide more granular voice quality control). VoNR supports enhanced voice codecs like EVS (Enhanced Voice Services) for super-wideband voice.

VoNR requires SA 5G deployment with IMS support. NSA 5G uses VoLTE since the control plane runs on LTE. VoNR is a key requirement for operators completing their SA 5G migration, as it eliminates the need for LTE fallback.

## Q95: What is the difference between RLC ARQ and HARQ?

**A:** HARQ operates at the MAC/physical layer with very fast turnaround (4-10 ms). HARQ uses soft combining (chase combining or incremental redundancy) to improve decoding probability on retransmission. HARQ operates on transport blocks and provides the first layer of error correction.

RLC ARQ operates at the RLC layer with slower turnaround (typically 40-80 ms). RLC ARQ operates on RLC PDUs and provides the second layer of error correction when HARQ retransmissions fail. RLC ARQ uses selective repeat, retransmitting only the specific PDUs that were not correctly received.

The combination of HARQ (fast, inner loop) and RLC ARQ (slower, outer loop) provides both high throughput (HARQ's fast retransmission) and high reliability (RLC ARQ's guaranteed delivery). In 5G, the RLC ARQ functionality was simplified with reordering moved to PDCP, reducing latency.

## Q96: What is the role of SIB1 in cell selection?

**A:** SIB1 contains the critical parameters for cell selection and reselection. It includes: cell access related information (PLMN identity, cell barred status, cell reserved for operator use), cell selection parameters (Qrxlevmin, Qrxlevminoffset, Qqualmin), and scheduling information (scheduling info list with SIB mapping and periodicity).

SIB1 also carries the UE-TimersAndConstants (T300, T301, T304, T311, T319 for various RRC procedures) and frequency band indicator. For inter-frequency reselection, SIB1 provides theFrequencyInfo with EUTRA-FrequencyList.

SIB1 is transmitted on PDSCH with a fixed periodicity of 80 ms, with repetition within each 80 ms window. UEs must acquire SIB1 before attempting random access, as it provides the RACH configuration parameters needed for initial access.

## Q97: What is the meaning of capacity and coverage trade-off?

**A:** The capacity-coverage trade-off in cellular networks means that increasing coverage per cell reduces the total system capacity, and vice versa. Higher transmit power extends cell radius (better coverage) but increases inter-cell interference, reducing capacity. Smaller cells with lower power increase capacity through frequency reuse but require more base stations for coverage.

This trade-off is managed through cell planning, power control, and interference management. Macro cells provide blanket coverage, while small cells add capacity in hotspots. The optimal deployment balances coverage gaps against capacity requirements.

In 5G, the trade-off is addressed through massive MIMO (focused beams provide both coverage and capacity), network densification (many small cells for capacity), and spectrum strategy (low-band for coverage, mid-band for balanced, mmWave for capacity).

## Q98: What is the NG interface in 5G?

**A:** The NG interface connects gNodeBs to the 5G core network, split into NG-C (control plane to AMF) and NG-U (user plane to UPF). NGAP (NG Application Protocol) carries procedures including Initial UE Message (forwarding NAS messages), PDU Session Resource Setup/Release, and Handover.

NG-U uses GTP-U to tunnel user data between the gNodeB and UPF, similar to the S1-U interface. The NG interface supports network slicing, where different gNodeBs can connect to different AMFs and UPFs for different slices.

The NG-RAN (Next-Generation RAN) includes gNodeBs connected via NG to the 5GC, and optionally eNodeBs connected via NG-C to AMF for LTE interworking. The N26 interface between AMF and MME enables inter-system handover between 5G and LTE.

## Q99: What is the role of the NRF in 5G SBA?

**A:** The NF Repository Function (NRF) is the service discovery mechanism in the 5G SBA. It maintains profiles of available NF instances and their services. When an NF needs to communicate with another NF, it queries the NRF to discover available instances, their capabilities, and their status.

The NRF enables dynamic, decentralized architecture where NFs can be instantiated, scaled, and terminated without manual configuration. NFs register with the NRF when they come online and deregister when they go offline. The NRF provides APIs for NF registration, discovery, and subscription to NF status changes.

NRF supports slice-specific discovery, allowing NFs to find slice-specific instances of other NFs. For example, a slice-specific SMF can discover the slice-specific UPF through NRF. This is essential for the scalability and flexibility of network slicing.

## Q100: What are the key differences between LTE and 5G NR physical layer?

**A:** LTE uses fixed 15 kHz subcarrier spacing with 14 OFDM symbols per subframe (1 ms). 5G NR supports scalable numerology with subcarrier spacings of 15, 30, 60, 120, and 240 kHz, enabling flexible slot durations (0.5-0.125 ms). This flexibility supports diverse deployment scenarios from sub-6 GHz to mmWave.

LTE uses QPSK, 16QAM, and 64QAM modulation. 5G NR adds 256QAM for higher peak rates and uses LDPC codes (vs. LTE's Turbo codes) for better performance at high code rates. 5G also uses Polar codes for control channels, which outperform LTE's tail-biting convolutional codes.

The frame structure differs: LTE has fixed 10 ms frames with 10 subframes. 5G NR has 10 ms frames but configurable slot structure supporting mini-slots for URLLC, bandwidth parts for partial bandwidth reception, and flexible uplink/downlink slot configuration in TDD. These differences enable 5G NR to achieve 10-100x higher throughput and 10x lower latency than LTE.
