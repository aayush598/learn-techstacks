# Static vs Dynamic Routing — 100 Interview Q&A

## Q1: What is static routing?
**A:** Static routing is the manual configuration of routing entries in a router's routing table. A network administrator specifies the destination network, subnet mask, and next-hop IP address or outgoing interface for each route. Static routes do not change unless the administrator manually modifies them.

Static routing is ideal for small, stable networks with few routes and predictable traffic patterns. It requires no protocol overhead, does not consume bandwidth for route exchanges, and provides deterministic forwarding behavior. However, static routes cannot adapt to network changes automatically, making them impractical for large, dynamic networks.

## Q2: What is dynamic routing?
**A:** Dynamic routing uses routing protocols to automatically exchange reachability information between routers. Routers learn about available routes, calculate the best paths, and install them in the routing table. When the network topology changes, dynamic routing protocols automatically recalculate and update routes.

Dynamic routing is essential for large, complex networks where manual route management would be impractical. Protocols like OSPF, EIGRP, and BGP provide mechanisms for routers to discover neighbors, share routing information, converge on consistent views of the network, and adapt to failures. The trade-off is increased complexity and resource consumption.

## Q3: What is a routing table?
**A:** A routing table is a data structure stored in a router or host that maps destination networks to next-hop addresses and outgoing interfaces. Each entry contains the destination prefix, prefix length, next-hop address, outgoing interface, metrics, and administrative distance. The routing table is consulted for every packet to determine how to forward it.

Routers build their routing tables from multiple sources: directly connected interfaces, statically configured routes, and routes learned dynamically through routing protocols. The table is the authoritative source for forwarding decisions and must be consulted for every packet that transits the router.

## Q4: What is the administrative distance (AD)?
**A:** Administrative distance is a value that represents the trustworthiness of a routing source. Lower AD values indicate more trustworthy sources. Directly connected routes have an AD of 0, static routes have an AD of 1 by default, and dynamic routing protocols have varying ADs such as EIGRP at 90, OSPF at 110, and RIP at 120.

When multiple routing sources provide routes to the same destination, the route with the lowest AD is installed in the routing table. This allows a router to prefer statically configured routes over dynamically learned ones, or to prefer one routing protocol over another. AD provides a mechanism for controlling route preference without modifying metrics.

## Q5: What is a default route?
**A:** A default route, also known as the gateway of last resort, is a route that matches all destinations not covered by more specific routes. It is represented as 0.0.0.0/0 in IPv4 and ::/0 in IPv6. When a packet's destination does not match any specific route, the default route is used.

Default routes are commonly used in stub networks where there is a single exit point to the Internet. They simplify routing tables by providing a catch-all entry. Default routes can be configured statically or learned dynamically through protocols like BGP or OSPF.

## Q6: What is a directly connected route?
**A:** Directly connected routes are automatically added to the routing table when an interface is configured with an IP address and the interface is in the up state. These routes represent networks that are physically attached to the router and require no manual configuration or protocol exchange.

Directly connected routes always have an administrative distance of 0, making them the most trusted route source. They are the foundation of all routing because a router can only forward packets to directly connected networks or to next hops that are reachable through some route.

## Q7: What is the difference between static and dynamic routing?
**A:** Static routing requires manual configuration of each route and does not adapt to network changes automatically. Dynamic routing uses protocols to automatically learn and update routes as the network topology changes. Static routing has zero protocol overhead while dynamic routing consumes CPU, memory, and bandwidth for protocol operations.

Static routing provides deterministic forwarding with no convergence time, while dynamic routing may experience temporary loops or black holes during convergence. Static routing is suitable for small, simple networks, while dynamic routing is essential for large, complex networks where manual management is impractical.

## Q8: What is the difference between IGP and EGP?
**A:** Interior Gateway Protocols (IGPs) are used for routing within a single autonomous system (AS). Examples include OSPF, IS-IS, EIGRP, and RIP. Exterior Gateway Protocols (EGPs) are used for routing between autonomous systems. The primary EGP in use today is BGP (Border Gateway Protocol).

IGPs focus on finding the best path within an organization's network, optimizing for metrics like bandwidth, delay, or hop count. EGPs focus on policy-based routing between organizations, considering factors like AS path length, local preference, and traffic engineering requirements. The distinction reflects the different requirements of intra-domain and inter-domain routing.

## Q9: What is administrative distance and why is it important?
**A:** Administrative distance is a numeric value assigned to each routing source to indicate its trustworthiness. When a router learns about the same destination from multiple sources, it installs the route with the lowest AD in the routing table. This provides a hierarchy of route preference independent of the metric.

AD is important because it allows network administrators to control route selection. For example, a static route (AD=1) is preferred over an OSPF-learned route (AD=110), ensuring that manually configured paths take precedence. If the static route fails, the OSPF route can be used as a backup, providing redundancy.

## Q10: What is a route metric?
**A:** A route metric is a numerical value used by routing protocols to compare the desirability of different routes to the same destination. Different protocols use different metrics. RIP uses hop count, OSPF uses cost based on bandwidth, EIGRP uses a composite metric based on bandwidth and delay, and IS-IS uses a similar cost metric.

Metrics are used within a single routing protocol to select the best route among multiple alternatives. They are not compared across different protocols; instead, administrative distance is used to choose between routes from different sources. The metric calculation varies by protocol and can be influenced by configuration.

## Q11: What is a static route?
**A:** A static route is a manually configured routing entry that specifies how to reach a particular destination network. It includes the destination network, subnet mask, and either a next-hop IP address or an outgoing interface. Static routes are added to the routing table and remain until manually removed.

Static routes are useful for default routes, stub networks, and specific paths that should not change. They are also used as backup routes with higher administrative distances. Static routes require no protocol overhead but cannot adapt to network changes without manual intervention.

## Q12: What is the role of the gateway of last resort?
**A:** The gateway of last resort is a default route that routers use when no specific route matches a packet's destination. It is typically configured as 0.0.0.0/0 pointing to a next-hop router. All traffic destined for networks not explicitly in the routing table is forwarded to this gateway.

In enterprise networks, the gateway of last resort is usually the border router connected to the Internet. In service provider networks, default routes are carefully controlled and may be learned from BGP peers. The gateway of last resort simplifies routing by providing a catch-all entry for unknown destinations.

## Q13: What is a floating static route?
**A:** A floating static route is a static route configured with a higher administrative distance than the preferred route source. It is not installed in the routing table as long as a more preferred route exists. If the primary route fails, the floating static route becomes active and takes its place.

Floating static routes provide route redundancy without dynamic routing protocols. For example, a floating static route with AD=200 can serve as a backup to an OSPF route with AD=110. When the OSPF route disappears, the floating static route is installed, maintaining connectivity.

## Q14: How does a router choose between static and dynamic routes?
**A:** A router chooses between static and dynamic routes based on administrative distance. Static routes have a default AD of 1, while dynamic routes have higher ADs such as 90 for EIGRP, 110 for OSPF, or 120 for RIP. The route with the lowest AD is installed in the routing table.

This means static routes are preferred over dynamic routes by default. However, this can be modified by changing the AD of static routes or by using route redistribution to influence how routes are compared. The AD-based selection ensures a predictable hierarchy of route sources.

## Q15: What is route summarization?
**A:** Route summarization, also known as route aggregation or supernetting, combines multiple specific routes into a single less-specific route. For example, routes to 10.1.1.0/24, 10.1.2.0/24, 10.1.3.0/24, and 10.1.4.0/24 can be summarized as 10.1.0.0/22. This reduces the size of routing tables and the number of routing updates.

Summarization is essential for scalability in large networks. It reduces the number of routes that routers must store and process, decreases the size of routing protocol updates, and limits the scope of route flapping. However, summarization must be done carefully to avoid black holes or routing loops if the summary covers destinations that are not reachable through the summarizing router.

## Q16: What are the advantages of static routing?
**A:** Static routing has several advantages: zero protocol overhead (no CPU, memory, or bandwidth consumption for routing protocols), deterministic forwarding with no convergence time, complete administrator control over path selection, no security concerns from routing protocol attacks, and simplicity in small networks.

Static routes are also predictable because they do not change unless manually modified. They provide exact control over traffic paths, which is valuable for traffic engineering, policy enforcement, and security-sensitive networks. Static routes are the foundation of all routing because even dynamic routing depends on directly connected routes, which are essentially static.

## Q17: What are the disadvantages of static routing?
**A:** Static routing has significant disadvantages: it requires manual configuration of every route, it does not adapt to network changes automatically, it cannot detect link failures without additional mechanisms like IP SLA, it does not scale to large networks, and it provides no load balancing across multiple equal-cost paths.

When a link fails, static routes continue to point to the failed next hop, causing black holes. The administrator must manually update routes to restore connectivity. In large networks with hundreds or thousands of routes, static route management becomes prohibitively complex and error-prone.

## Q18: What is the difference between a next-hop static route and a directly connected static route?
**A:** A next-hop static route specifies the IP address of the next router along the path. The router resolves the next-hop address using its routing table and forwards the packet to that address. A directly connected static route specifies the outgoing interface, and the router sends the packet out that interface.

Next-hop routes are more flexible because the next-hop router can be on any directly connected network. Directly connected routes are simpler but require the destination to be on a directly connected network. Next-hop routes can be recursive, requiring multiple lookups, while directly connected routes require a single lookup.

## Q19: What is recursive static routing?
**A:** Recursive static routing occurs when a static route specifies a next-hop IP address that is not directly connected. The router must perform an additional routing table lookup to find how to reach the next-hop address. This recursive lookup continues until the router finds a directly connected route.

Recursive lookups add processing overhead and can cause routing loops if not configured carefully. For example, if static route A points to next-hop B, and static route B points to next-hop A, a routing loop is created. Most modern routers handle recursive lookups efficiently, but they should be avoided when possible for performance reasons.

## Q20: What is a directly connected static route?
**A:** A directly connected static route specifies an outgoing interface rather than a next-hop IP address. The router forwards the packet out the specified interface. If the interface is a multi-access interface like Ethernet, the router must also determine the next-hop address using ARP or other mechanisms.

Directly connected static routes are simpler to configure and avoid recursive lookups. However, they can cause issues on multi-access interfaces because the router does not know which specific next-hop device should receive the packet. For point-to-point interfaces, directly connected routes work well because there is only one possible next hop.

## Q21: What is the role of administrative distance in route redundancy?
**A:** Administrative distance enables route redundancy by allowing multiple routes to the same destination with different AD values. The route with the lowest AD is active, while higher AD routes serve as backups. When the primary route fails, the backup route automatically takes over.

This mechanism provides failover without requiring dynamic routing protocols. For example, a static route with AD=1 can serve as the primary path, with an OSPF route with AD=110 as a backup. If the static route is removed, the OSPF route becomes active. This provides basic redundancy with minimal configuration.

## Q22: What is the difference between equal-cost and unequal-cost load balancing?
**A:** Equal-cost load balancing distributes traffic across multiple paths that have the same metric value. All routing protocols support this. Unequal-cost load balancing distributes traffic across paths with different metrics, proportionally based on the metric difference. Only EIGRP supports unequal-cost load balancing natively.

Equal-cost load balancing is simpler and more widely supported. Unequal-cost load balancing, such as EIGRP's variance feature, can utilize backup paths that would otherwise remain idle. This improves bandwidth utilization but requires careful configuration to avoid forwarding loops.

## Q23: What is route redistribution?
**A:** Route redistribution is the process of injecting routes from one routing protocol into another. For example, routes learned via OSPF can be redistributed into EIGRP, or static routes can be redistributed into OSPF. Redistribution allows different parts of a network to use different routing protocols.

Redistribution must be done carefully to avoid routing loops, suboptimal routing, and black holes. Techniques like route tags, route maps, and administrative distance manipulation are used to control redistribution. Mutual redistribution, where routes are exchanged in both directions between protocols, is particularly risky and requires careful planning.

## Q24: What is a stub network?
**A:** A stub network is a network that has only a single connection to the rest of the network. It has only one path to reach any destination outside the network. Stub networks are typically leaf networks with no transit traffic and can use a default route to reach all external destinations.

Stub networks are ideal candidates for static routing because they only need a default route to reach the rest of the network. They do not need to learn detailed routing information because there is only one path. OSPF also has a stub area concept where areas with a single exit point can use default routes instead of receiving full routing tables.

## Q25: What is the difference between classful and classless routing?
**A:** Classful routing protocols (such as RIPv1 and IGRP) do not include subnet mask information in routing updates. They assume that all routers in the network agree on the subnet mask for each classful network. This limits the ability to use variable-length subnet masking (VLSM) and route summarization.

Classless routing protocols (such as OSPF, EIGRP, RIPv2, and BGP) include subnet mask information with each route. This supports VLSM, route summarization, and more efficient use of address space. Modern networks almost exclusively use classless routing protocols.

## Q26: What is OSPF and how does it differ from static routing?
**A:** OSPF (Open Shortest Path First) is a link-state interior gateway protocol that uses Dijkstra's algorithm to calculate shortest paths. Each router builds a complete topology map of the network and calculates the best path to each destination based on interface costs. OSPF converges quickly and scales well in large networks.

Unlike static routing, OSPF automatically discovers neighbors, advertises link-state information, recalculates routes when the topology changes, and supports equal-cost multipath. OSPF uses cost as its metric, typically based on interface bandwidth. OSPF areas allow hierarchical design, reducing the scope of topology changes and the size of link-state databases.

## Q27: What is the difference between OSPF areas and route summarization?
**A:** OSPF divides the network into areas to limit the scope of link-state advertisements. Area 0 is the backbone area, and other areas connect to it. Route summarization in OSPF occurs at area boundaries, where multiple specific routes from within an area are summarized into a single summary route advertised to other areas.

Summarization at area boundaries reduces the size of routing tables and limits the impact of route flapping. For example, if a link in Area 1 flaps, the summary route from Area 1 to the backbone does not change, so routers in other areas are not affected. Proper summarization requires contiguous address allocation within areas.

## Q28: What is EIGRP and its key characteristics?
**A:** EIGRP (Enhanced Interior Gateway Routing Protocol) is a Cisco-proprietary hybrid routing protocol that combines features of distance-vector and link-state protocols. It uses the Diffusing Update Algorithm (DUAL) to calculate loop-free paths and maintains a topology table of feasible successors for rapid convergence.

EIGRP uses a composite metric based on bandwidth and delay by default, though it can also consider reliability and load. It supports unequal-cost load balancing through the variance feature. EIGRP sends partial, bounded updates only when changes occur, making it bandwidth-efficient. It uses RTP (Reliable Transport Protocol) for guaranteed delivery of updates.

## Q29: What is the difference between distance-vector and link-state routing protocols?
**A:** Distance-vector protocols (such as RIP and EIGRP) send their entire routing tables to neighbors periodically or when changes occur. Each router learns about the network indirectly through its neighbors, like a rumor. Link-state protocols (such as OSPF and IS-IS) flood link-state information to all routers in the area, allowing each router to build a complete topology map.

Distance-vector protocols are simpler but more prone to routing loops and slow convergence. Link-state protocols converge faster, scale better, and make more optimal routing decisions because each router has a complete view of the topology. The trade-off is increased complexity and resource consumption for link-state protocols.

## Q30: What is the split-horizon rule?
**A:** Split horizon is a loop-prevention mechanism that prevents a router from advertising a route back out the same interface on which it was learned. This eliminates the possibility of a two-node routing loop where two routers bounce a route back and forth.

Split horizon is implemented in distance-vector protocols like RIP and EIGRP. In some cases, split horizon must be disabled on certain interfaces, such as Frame Relay or DMVPN multipoint interfaces, where logical interfaces map to multiple physical destinations. Disabling split horizon requires other loop-prevention mechanisms like route poisoning or hold-down timers.

## Q31: What is route poisoning?
**A:** Route poisoning is a technique where a router advertises a failed route with an infinite metric (typically 16 for RIP) to indicate that the route is unreachable. This immediately notifies neighbors that the route is down, rather than waiting for the route to age out naturally.

Route poisoning is often combined with hold-down timers to prevent routers from accepting incorrect routing information about the failed route during convergence. Poison reverse, a related technique, involves advertising a route as unreachable back to the source from which it was learned, further preventing loops.

## Q32: What is a hold-down timer?
**A:** A hold-down timer is a mechanism used in distance-vector routing protocols to prevent routing loops during convergence. When a route is marked as unreachable, the router enters a hold-down period during which it ignores any updates about that route from other routers, unless the updates come from the same next hop that originally advertised the route.

Hold-down timers prevent routers from accepting stale or incorrect routing information that could cause loops. The downside is that hold-down timers can slow convergence because legitimate route changes may be ignored during the hold-down period. Modern protocols like OSPF and EIGRP use faster convergence mechanisms instead.

## Q33: What is the difference between routing and forwarding?
**A:** Routing is the process of determining the best path for a packet to travel from source to destination. It involves building and maintaining routing tables using static configuration or routing protocols. Routing is a control-plane function that happens periodically or when changes occur.

Forwarding is the process of moving a packet from an input interface to the correct output interface based on the routing table. It is a data-plane function that happens for every packet. Forwarding is typically implemented in hardware (ASICs or TCAM) for high-speed performance, while routing is implemented in software.

## Q34: What is the RIB and FIB?
**A:** The RIB (Routing Information Base) is the complete routing table maintained by the control plane. It contains routes from all sources including directly connected, static, and dynamically learned routes. The RIB is used to select the best route for each destination.

The FIB (Forwarding Information Base) is a subset of the RIB optimized for hardware-based forwarding. It contains only the best routes and is programmed into the router's forwarding hardware (TCAM). The FIB is what the data plane actually uses to forward packets. The RIB and FIB are synchronized by the control plane.

## Q35: What is the difference between a route and a forwarding entry?
**A:** A route is a complete routing information entry in the RIB, including the destination prefix, next-hop, outgoing interface, metrics, administrative distance, and route source. Routes are maintained by the control plane and may include multiple paths to the same destination.

A forwarding entry is the specific entry in the FIB that tells the data plane where to send a packet. It contains the destination prefix, next-hop, and outgoing interface, but not the full routing metadata. Forwarding entries are optimized for hardware lookup and may include additional information for features like NetFlow or ACLs.

## Q36: What is convergence in routing?
**A:** Convergence is the process by which all routers in a network agree on the current topology and have consistent routing tables. When a network change occurs such as a link failure, routers must detect the change, propagate the information, recalculate routes, and update their forwarding tables.

Convergence time is the duration from when a change occurs until all routers have consistent forwarding tables. Faster convergence is generally better because during convergence, routing tables may be inconsistent, leading to temporary loops or black holes. OSPF and EIGRP converge faster than RIP, which uses periodic updates.

## Q37: What is the difference between convergence time in OSPF and RIP?
**A:** OSPF converges much faster than RIP. OSPF uses triggered updates and incremental flooding, detecting link failures quickly and propagating changes rapidly. With BFD (Bidirectional Forwarding Detection), OSPF can detect failures in sub-second timeframes. Full convergence typically occurs within seconds.

RIP uses periodic updates every 30 seconds and has a maximum hop count of 15, which limits convergence speed and network size. RIP also uses hold-down timers and split horizon, which can further delay convergence. RIP's convergence time is typically measured in minutes, making it unsuitable for large or time-sensitive networks.

## Q38: What is BGP and its primary use case?
**A:** BGP (Border Gateway Protocol) is the exterior gateway protocol used for routing between autonomous systems on the Internet. It is a path-vector protocol that makes routing decisions based on policies, path attributes, and prefix information rather than metrics like hop count or bandwidth.

BGP's primary use case is inter-domain routing, where different organizations (autonomous systems) exchange routing information. BGP supports route filtering, policy-based routing, and complex path manipulation through attributes like AS path, local preference, MED, and communities. Within an AS, IBGP is used to distribute BGP routes to internal routers.

## Q39: What is the difference between IBGP and EBGP?
**A:** IBGP (Internal BGP) is used between BGP speakers within the same autonomous system. IBGP routes are not re-advertised to other IBGP peers (the split-horizon rule for IBGP), requiring a full mesh of IBGP sessions or route reflectors. IBGP uses the IGP next-hop for forwarding.

EBGP (External BGP) is used between BGP speakers in different autonomous systems. EBGP routes are re-advertised to all BGP peers by default. EBGP uses a default TTL of 1 (for directly connected peers) and modifies the AS path. EBGP is the foundation of Internet routing, connecting different organizations' networks.

## Q40: What is the difference between routing by policy and routing by metric?
**A:** Policy-based routing makes forwarding decisions based on administrative rules and policies rather than the shortest path. BGP is the primary protocol that uses policy-based routing, where administrators can influence path selection through attributes like local preference, AS path filters, and communities.

Metric-based routing selects the best path based on a numerical metric such as hop count, bandwidth, delay, or cost. IGP protocols like OSPF, EIGRP, and RIP use metric-based routing. The metric represents the desirability of a path, and the path with the best metric is selected. Policy-based routing overrides metric-based decisions.

## Q41: What is a route map?
**A:** A route map is a powerful tool used to match and modify routing information. It consists of a sequence of match and set statements that define conditions and actions. Route maps are used for route filtering, route redistribution, policy-based routing, and attribute manipulation.

Match conditions can include prefix lists, AS paths, communities, MED, next-hop, and other route attributes. Set actions can modify metrics, communities, local preference, weight, and other attributes. Route maps provide fine-grained control over routing behavior and are essential for implementing complex routing policies.

## Q42: What is a prefix list?
**A:** A prefix list is a filter that matches IP prefixes based on the network address and prefix length. It can match exact prefixes or ranges of prefixes. Prefix lists are used in route filtering, route redistribution, and policy-based routing to control which routes are accepted, rejected, or modified.

Prefix lists are more flexible than access lists for filtering routes because they can match both the network address and the prefix length. They support exact matches, greater-than-or-equal-to, less-than-or-equal-to, and range matching. Prefix lists are the preferred method for route filtering in modern networks.

## Q43: What is route filtering and why is it necessary?
**A:** Route filtering is the process of selectively accepting, rejecting, or modifying routing information. It is necessary for security (preventing unauthorized route advertisements), policy enforcement (controlling how traffic flows), loop prevention (blocking routes that could cause loops), and summarization (hiding specific routes).

Route filtering can be applied inbound or outbound on an interface, during route redistribution, or within routing protocol configurations. It uses tools like prefix lists, route maps, distribute lists, and AS path filters. Proper route filtering is essential for network stability and security.

## Q44: What is the difference between distribute lists and route maps?
**A:** Distribute lists are simple route filters that use access lists or prefix lists to permit or reject routes. They are applied to routing protocol updates and operate on a permit/deny basis without modifying route attributes. Distribute lists are straightforward but limited in functionality.

Route maps are more powerful and can match, permit, deny, and modify route attributes. They support sequential processing with multiple match and set statements. Route maps can be used for complex routing policies, route redistribution, and policy-based routing. For simple filtering, distribute lists are sufficient, but route maps are preferred for complex scenarios.

## Q45: What is the purpose of the maximum-paths command?
**A:** The maximum-paths command limits the number of equal-cost paths that a routing protocol will install in the routing table. By default, most protocols install only one best path. The maximum-paths command allows multiple equal-cost paths to be used for load balancing.

For example, setting maximum-paths to 4 allows up to four equal-cost paths to be installed and used for load balancing. This improves bandwidth utilization across multiple links. The actual number of paths installed depends on the protocol: OSPF supports up to 16 equal-cost paths, EIGRP supports up to 32, and RIP supports up to 16.

## Q46: What is a routing domain?
**A:** A routing domain is a collection of routers that share a common routing protocol and routing policy. It can be a single autonomous system running OSPF, a network running EIGRP, or any group of routers that exchange routing information through a common protocol. Routing domains define the scope of routing information exchange.

Routers within a routing domain share a common view of the network and can reach all destinations within the domain. Routing between domains requires route redistribution or default routes. The concept of routing domains is fundamental to network design, as it allows different parts of a network to use different routing protocols and policies.

## Q47: What is the difference between a routing domain and an autonomous system?
**A:** A routing domain is a logical grouping of routers sharing a common routing protocol. An autonomous system (AS) is a collection of networks under a single administrative control that uses a common routing policy for external routing. An AS can contain multiple routing domains running different IGP protocols.

The AS concept is fundamental to BGP and Internet routing. Each AS has a unique AS number and presents a single routing policy to the outside world. Within an AS, IGPs handle internal routing, while BGP handles routing between ASes. The distinction between routing domains and ASes reflects the difference between intra-domain and inter-domain routing.

## Q48: What is the role of the maximum-metric command in OSPF?
**A:** The maximum-metric command in OSPF sets the interface cost to a very high value (typically 65535) for OSPF advertisements. This is used to prevent a router from being used as a transit router during initial convergence or maintenance. The router still participates in OSPF but advertises its links with maximum cost.

This technique is commonly used during network maintenance or when bringing up new routers. It allows the router to learn routes without attracting traffic. After the router has fully converged and is ready to forward traffic, the maximum-metric is removed, and the router begins participating normally in OSPF routing.

## Q49: What is passive interface in routing protocols?
**A:** A passive interface is an interface on which a routing protocol does not send or receive routing updates. The interface's connected routes are still advertised, but no hello packets or routing updates are sent out the interface. This is commonly used on interfaces connected to end hosts where routing protocol exchanges are unnecessary.

Passive interfaces reduce routing protocol overhead and improve security by preventing unauthorized devices from participating in routing protocols. For example, making all access-layer interfaces passive in OSPF prevents end-user devices from forming OSPF adjacencies. The interface's connected subnets are still advertised to other OSPF routers.

## Q50: What is route redistribution and what are its challenges?
**A:** Route redistribution is the process of injecting routes from one routing protocol into another. For example, redistributing OSPF routes into EIGRP or static routes into OSPF. Redistribution allows different parts of a network to use different routing protocols while maintaining connectivity.

The main challenges of redistribution include routing loops, especially with mutual redistribution, suboptimal routing when metrics are not translated correctly, route feedback when routes are redistributed back into the source protocol, and administrative distance conflicts when the same destination is reachable via multiple redistributed routes. Careful use of route maps, route tags, and administrative distance manipulation is essential.

## Q51: What is a stub area in OSPF?
**A:** A stub area in OSPF is an area that does not receive external routes (Type 5 LSAs) from other areas. Instead, the ABR (Area Boundary Router) advertises a default route into the stub area. This reduces the size of the link-state database and routing table for routers within the stub area.

Stub areas are useful for networks with a single exit point where detailed external routing information is unnecessary. Totally stubby areas, a Cisco extension, go further by summarizing all routes into a single default route, further reducing database and table size. The restriction is that stub areas cannot have ASBRs that redistribute external routes.

## Q52: What is the difference between OSPF and IS-IS?
**A:** OSPF and IS-IS are both link-state routing protocols that use Dijkstra's algorithm. OSPF operates directly over IP (protocol 89) and uses areas with a backbone area (Area 0). IS-IS operates at the data-link layer and uses a hierarchical structure with levels instead of areas.

OSPF is more widely deployed in enterprise networks, while IS-IS is commonly used by large service providers. IS-IS is generally considered more scalable because it is protocol-independent (not bound to IP) and has simpler TLV-based encoding. OSPF has more features like stub areas, NSSAs, and virtual links, which add complexity but also flexibility.

## Q53: What is BGP path selection?
**A:** BGP path selection is a multi-step process that determines the best route when multiple paths to the same destination exist. The selection criteria in order of precedence are: highest weight (Cisco-specific), highest local preference, locally originated routes, shortest AS path, lowest origin type, lowest MED, eBGP over iBGP, lowest IGP metric to next-hop, and oldest route.

BGP path selection is policy-driven, allowing administrators to influence which paths are preferred through attribute manipulation. The default selection process can be overridden using route maps that modify attributes like local preference, AS path, and MED. This policy control is one of BGP's key strengths for inter-domain routing.

## Q54: What is the difference between BGP route reflectors and confederations?
**A:** Both route reflectors and confederations solve the IBGP split-horizon problem where IBGP routes are not re-advertised to other IBGP peers. Route reflectors designate specific routers as reflectors that can re-advertise routes received from one IBGP peer to other IBGP peers, reducing the required number of IBGP sessions.

Confederations divide a single AS into multiple sub-ASes. Within each sub-AS, a full IBGP mesh is required, but between sub-ASes, EBGP-like sessions are used. Confederations are more complex to implement but provide better scaling for very large networks. Route reflectors are simpler and more commonly deployed.

## Q55: What is the OSPF router ID and why is it important?
**A:** The OSPF router ID is a 32-bit unique identifier assigned to each OSPF router. It is used to identify the router in OSPF link-state advertisements and to elect the designated router (DR) and backup designated router (BDR) on multi-access networks. The router with the highest router ID becomes the DR.

The router ID can be configured manually or elected automatically from the highest IP address on a loopback interface, then the highest IP address on any active interface. It is important to configure stable router IDs because changing the router ID causes OSPF to restart and rebuild adjacencies, disrupting traffic.

## Q56: What is the OSPF designated router (DR) and backup designated router (BDR)?
**A:** On multi-access networks like Ethernet, OSPF elects a designated router (DR) and backup designated router (BDR) to reduce the number of OSPF adjacencies and link-state advertisements. All routers on the segment form adjacencies only with the DR and BDR, rather than with every other router.

The DR is responsible for flooding link-state advertisements on the segment and maintaining the pseudo-node representation of the network. The BDR provides redundancy in case the DR fails. DR/BDR election is based on router priority and router ID. Point-to-point networks do not require DR/BDR election.

## Q57: What is the difference between OSPF network types?
**A:** OSPF supports several network types that determine how adjacencies are formed and how LSAs are flooded. Broadcast networks (like Ethernet) use DR/BDR election. Non-broadcast multi-access (NBMA) networks (like Frame Relay) require manual neighbor configuration. Point-to-multipoint networks treat the network as a collection of point-to-point links.

Point-to-point networks form a single adjacency with the neighbor. The network type affects hello packet intervals, dead intervals, and the type of LSAs generated. Choosing the correct network type is essential for OSPF to function properly. Most modern networks use broadcast or point-to-point types.

## Q58: What is the OSPF link-state advertisement (LSA) and its types?
**A:** LSAs are the building blocks of OSPF's link-state database. They contain information about links, networks, and routes. Common LSA types include: Type 1 (Router LSA), generated by every router; Type 2 (Network LSA), generated by the DR on multi-access networks; Type 3 (Summary LSA), generated by ABRs for inter-area routes; Type 5 (External LSA), generated by ASBRs for external routes.

Understanding LSA types is essential for OSPF troubleshooting. For example, missing Type 3 LSAs indicate ABR issues, while missing Type 5 LSAs indicate ASBR problems. The LSA types define the scope and flooding domain of each advertisement, which is fundamental to OSPF's hierarchical design.

## Q59: What is the difference between EIGRP active and passive states?
**A:** In EIGRP, a route is in the passive state when it has a feasible successor, meaning a loop-free backup path is available. A route is in the active state when it does not have a feasible successor and the router must actively query neighbors to find an alternate path. Active routes cause additional network traffic and slower convergence.

The goal of EIGRP design is to keep all routes in the passive state by ensuring feasible successors are available. This is achieved by having redundant paths and appropriate metrics. When a route goes active, the router sends query packets to all EIGRP neighbors, which can propagate through the network and cause SIA (Stuck In Active) timeouts if not answered quickly.

## Q60: What is the EIGRP feasible successor?
**A:** A feasible successor in EIGRP is a backup route that satisfies the feasibility condition: the reported distance (RD) of the backup route must be less than the feasible distance (FD) of the current best route. This condition guarantees that the backup route is loop-free without requiring a full topology computation.

When the primary route fails, EIGRP immediately installs the feasible successor as the new best route without needing to query the network. This provides very fast convergence. If no feasible successor exists, EIGRP must go active and query the network to find an alternate path, which is slower.

## Q61: What is the difference between EIGRP queries and updates?
**A:** EIGRP updates contain routing information about reachable destinations. They are sent when a route changes and include metrics and path information. Updates are sent reliably using RTP and are only sent to affected neighbors, making them bandwidth-efficient.

EIGRP queries are sent when a route goes active (no feasible successor exists). They ask neighbors if they have an alternate path to the destination. Queries are sent to all EIGRP neighbors except the one that sent the original update. If no neighbor has an alternate path, the route becomes unreachable. Queries can propagate through the network and must be answered within the active time limit.

## Q62: What is route redistribution between OSPF and EIGRP?
**A:** Route redistribution between OSPF and EIGRP requires careful configuration because the metrics are incompatible. OSPF uses cost (bandwidth-based) while EIGRP uses a composite metric (bandwidth, delay, reliability, load). When redistributing, default metrics must be specified for the target protocol.

For example, when redistributing OSPF into EIGRP, you must specify the EIGRP K-values (bandwidth, delay, reliability, load) for the redistributed routes. When redistributing EIGRP into OSPF, you must specify the cost value. Failure to set correct metrics can lead to suboptimal routing or routing loops.

## Q63: What is the difference between route redistribution and mutual redistribution?
**A:** Route redistribution is a one-way injection of routes from one protocol into another. For example, redistributing OSPF routes into EIGRP. Mutual redistribution is the bidirectional exchange of routes between two protocols, where routes are redistributed in both directions.

Mutual redistribution is more complex and riskier because it can create routing loops. If routes are redistributed from OSPF to EIGRP and then back into OSPF, the same routes may exist in both protocols with different metrics. Route tags, route maps, and administrative distance manipulation are used to prevent loops in mutual redistribution scenarios.

## Q64: What is the role of the default-information originate command?
**A:** The default-information originate command in OSPF causes a router to advertise a default route (0.0.0.0/0) into the OSPF domain. This is the OSPF equivalent of a default route. The command can be used with the always keyword to advertise the default route even if the router does not have a default route in its routing table.

This command is essential for injecting a default route into OSPF, which is necessary for stub networks that need to reach external destinations. Without this command, OSPF does not automatically redistribute the default route. The advertised default route appears as a Type 5 external LSA in the OSPF database.

## Q65: What is the difference between a routing loop and a black hole?
**A:** A routing loop occurs when packets are forwarded in a circular path between routers, never reaching their destination. This consumes bandwidth and router resources without delivering packets. Routing loops are typically caused by inconsistent routing tables during convergence or misconfigured redistribution.

A black hole occurs when a packet is forwarded to a router that has no route to the destination, causing the packet to be dropped. Black holes are typically caused by missing routes, incorrect default routes, or asymmetric routing where the return path does not exist. Both loops and black holes are routing failures that disrupt connectivity.

## Q66: What is the difference between route summarization and route aggregation?
**A:** Route summarization and route aggregation are essentially the same concept: combining multiple specific routes into a single less-specific route. The terms are often used interchangeably. Route summarization is the process of reducing the number of routes by advertising a summary prefix instead of individual routes.

Route aggregation may also refer to the result of the summarization process. Both terms describe the same technique used to reduce routing table size, limit route flapping, and improve scalability. The key is that the summary must not cover unreachable destinations to avoid black holes.

## Q67: What is a route tag?
**A:** A route tag is a 32-bit value associated with a route that is used to identify and filter routes during redistribution. Route tags are not used for routing decisions but serve as markers to control how routes are redistributed between protocols. For example, routes learned from OSPF can be tagged with a specific value when redistributed into EIGRP.

When routes are redistributed back from EIGRP into OSPF, the tags can be used to prevent the same routes from being redistributed twice, which would create loops. Route tags are an essential tool for controlling route redistribution in networks with multiple routing protocols.

## Q68: What is the difference between internal and external routes in OSPF?
**A:** Internal OSPF routes are routes to destinations within the OSPF domain, learned through Type 1 and Type 2 LSAs. External OSPF routes are routes to destinations outside the OSPF domain, redistributed from other protocols or static routes, advertised through Type 5 LSAs by ASBRs.

Internal routes are preferred over external routes in OSPF path selection. External routes can be classified as E1 (where the cost includes the external cost plus the internal cost to the ASBR) or E2 (where the cost is only the external cost, default). E2 is commonly used for external routes because it provides consistent metrics regardless of where the route is injected.

## Q69: What is the OSPF NSSA (Not-So-Stubby Area)?
**A:** An NSSA is an OSPF area that can contain ASBRs that redistribute external routes but does not receive Type 5 LSAs from other areas. External routes within the NSSA are advertised as Type 7 LSAs, which are translated to Type 5 LSAs by the ABR when they leave the NSSA.

NSSAs provide a compromise between stub areas (which cannot have ASBRs) and regular areas (which receive all external routes). They are useful for branch offices that connect to the Internet through a local ISP while still using OSPF for internal routing. The NSSA ABR translates Type 7 to Type 5 LSAs, allowing external routes to be advertised to the rest of the OSPF domain.

## Q70: What is the difference between OSPF stub and totally stubby areas?
**A:** A stub area does not receive Type 5 external LSAs but does receive Type 3 summary LSAs from other areas. A totally stubby area (a Cisco extension) does not receive Type 3 summary LSAs either, except for a single default route advertised by the ABR. This makes totally stubby areas even more restrictive.

Totally stubby areas provide the maximum reduction in routing table size and database size. They are useful for stub networks with a single exit point where only a default route is needed to reach all external destinations. The limitation is that totally stubby areas cannot have ASBRs and all external reachability must go through the ABR.

## Q71: What is the difference between equal-cost multipath (ECMP) and unequal-cost multipath?
**A:** Equal-cost multipath (ECMP) distributes traffic across multiple paths that have the same metric value. All routing protocols support ECMP, and it is the most common form of load balancing. The traffic is distributed using hashing algorithms based on packet headers.

Unequal-cost multipath distributes traffic across paths with different metrics, proportionally based on the metric difference. Only EIGRP supports this natively through the variance feature, where paths within a variance multiplier of the best path are included. Unequal-cost multipath can utilize backup paths that would otherwise remain idle, improving bandwidth utilization.

## Q72: What is the role of BFD (Bidirectional Forwarding Detection) in routing?
**A:** BFD is a lightweight protocol that provides fast failure detection between adjacent routers. It runs independently of routing protocols and can detect failures in sub-second timeframes by sending rapid heartbeat packets. BFD triggers routing protocol reconvergence when it detects a failure.

Without BFD, routing protocols rely on their own hello and dead timers to detect failures, which can take 30-40 seconds or more. BFD reduces this to milliseconds, dramatically improving convergence time. BFD is supported by OSPF, EIGRP, IS-IS, and BGP, and is essential for meeting sub-second convergence requirements in modern networks.

## Q73: What is the difference between routing policy and routing metric?
**A:** A routing metric is a numerical value used to compare paths within a routing protocol, such as hop count in RIP or cost in OSPF. The metric represents the desirability of a path, and the path with the best metric is selected. Metrics are protocol-specific and not comparable across protocols.

A routing policy is an administrative rule that overrides metric-based decisions. Policies can filter routes, modify attributes, prefer certain paths, or implement traffic engineering requirements. BGP is the primary protocol that uses policy-based routing, but policies can also be applied to IGP routes through route maps and administrative distance manipulation.

## Q74: What is the impact of route flapping on routing protocols?
**A:** Route flapping occurs when a route repeatedly appears and disappears in quick succession. This causes routing protocols to constantly update their routing tables, consuming CPU, memory, and bandwidth. Flapping can cause instability across the network as routers continuously recalculate routes.

Routing protocols implement mechanisms to dampen route flapping. OSPF uses the SPF throttle timer to limit how often the SPF algorithm runs. BGP uses route dampening, which penalizes frequently flapping routes and suppresses them. EIGRP uses a hold-down timer. These mechanisms help maintain network stability during route instability.

## Q75: What is the difference between a default route and a summary route?
**A:** A default route (0.0.0.0/0) matches all destinations not covered by more specific routes. It is the ultimate catch-all route, pointing all unmatched traffic to a single next hop. Default routes are commonly used as the gateway of last resort.

A summary route combines multiple specific routes into a single less-specific route, such as summarizing 10.1.0.0/24 through 10.1.3.0/24 into 10.1.0.0/22. Summary routes match a range of specific destinations but not all destinations. Both default and summary routes reduce routing table size, but default routes are the most general while summary routes are intermediate in specificity.

## Q76: What is route dampening in BGP?
**A:** Route dampening is a BGP feature that penalizes routes that flap frequently. When a route flaps, it is assigned a penalty value. If the penalty exceeds a threshold, the route is suppressed (not advertised) until the penalty decays below a reuse threshold. This prevents unstable routes from propagating through the network.

Dampening uses four parameters: half-life (penalty decay rate), suppress-threshold (penalty at which the route is suppressed), reuse-threshold (penalty at which the route is reused), and maximum-hold-time (maximum time a route can be suppressed). Proper tuning is essential because overly aggressive dampening can suppress legitimate route changes, while insufficient dampening allows instability to propagate.

## Q77: What is the difference between BGP local preference and weight?
**A:** Local preference is a 32-bit value that is exchanged between IBGP peers to indicate the preferred exit point from an AS. Higher local preference values are preferred. It is a well-known discretionary attribute that is propagated to all IBGP peers within the AS but not across AS boundaries.

Weight is a Cisco-proprietary attribute that is local to the router. It is not exchanged with any other router. Higher weight values are preferred. Weight is used to influence path selection on a per-router basis, while local preference is used to influence path selection across all routers in an AS. Local preference is the standard mechanism for exit-point selection.

## Q78: What is the BGP AS path and its significance?
**A:** The AS path is a mandatory BGP attribute that lists the autonomous systems through which a route has passed. It is used for loop prevention (a route is rejected if the local AS is already in the path) and for path selection (shorter AS paths are generally preferred). The AS path is modified at each EBGP hop.

AS path length is one of the primary criteria in BGP path selection. Shorter paths are preferred, though this can be overridden by policy attributes like local preference. AS path prepending, where the local AS number is added multiple times to the path, is a common traffic engineering technique to make a path appear less attractive.

## Q79: What is the difference between EBGP multihop and IBGP?
**A:** EBGP multihop is used when two EBGP peers are not directly connected. By default, EBGP requires directly connected peers with a TTL of 1. The EBGP multihop command increases the TTL, allowing the BGP session to traverse multiple hops. IBGP peers are typically not directly connected and use the IGP to reach each other.

IBGP sessions use the IGP next-hop for forwarding and do not modify the AS path. EBGP sessions modify the AS path and next-hop. IBGP requires a full mesh or route reflectors because IBGP routes are not re-advertised to other IBGP peers. EBGP does not have this restriction.

## Q80: What is the OSPF shortest path first (SPF) algorithm?
**A:** The SPF algorithm, also known as Dijkstra's algorithm, calculates the shortest path from a router to all destinations in the OSPF domain. It uses the link-state database, which contains a complete topology of the network, and calculates the lowest-cost path to each destination.

The SPF algorithm starts at the root (the local router) and builds a shortest-path tree. It examines each node, adding the lowest-cost path to the next unvisited node until all nodes are visited. The result is a set of shortest paths that are installed in the routing table. SPF is computationally intensive, which is why OSPF limits the scope of link-state flooding through areas.

## Q81: What is the difference between OSPF and EIGRP convergence?
**A:** OSPF convergence involves detecting a topology change, flooding LSAs, running the SPF algorithm, and updating the routing table. The SPF algorithm must run on the entire topology database, which can be slow in large areas. OSPF uses incremental SPF and SPF throttling to improve convergence speed.

EIGRP convergence is generally faster because it maintains feasible successors (backup paths) in its topology table. When a primary route fails, EIGRP immediately installs the feasible successor without running a full computation. EIGRP also uses partial, bounded updates that only propagate changes, reducing convergence time. Without feasible successors, EIGRP must query the network, which can be slower than OSPF.

## Q82: What is the role of the routing table in the forwarding process?
**A:** The routing table is consulted for every packet that enters a router. The router performs a longest-prefix match to find the most specific route for the packet's destination. The matched route provides the next-hop IP address and outgoing interface. The router then encapsulates the packet in a frame and forwards it to the next hop.

In modern routers, the routing table (RIB) is used to build the forwarding table (FIB), which is optimized for hardware lookup. The FIB is stored in TCAM (Ternary Content-Addressable Memory) for high-speed parallel lookup. This separation of the RIB and FIB allows the control plane to operate independently of the data plane.

## Q83: What is the difference between recursive and iterative lookup?
**A:** Recursive lookup occurs when the next-hop address in the routing table is not directly connected, requiring additional lookups to find how to reach the next hop. This continues until a directly connected route is found. Recursive lookups add processing overhead.

Iterative lookup is the general process of performing multiple routing table lookups to resolve the final forwarding decision. In modern routers, recursive lookups are typically resolved during FIB construction, so the data plane only needs a single lookup. This optimization eliminates recursive lookup overhead in the forwarding path.

## Q84: What is the OSPF virtual link?
**A:** An OSPF virtual link is a logical link that connects two areas through a non-backbone area that is not directly connected to Area 0. Virtual links are used when an area cannot be directly connected to the backbone due to physical or design constraints. The virtual link appears as a point-to-point link between the two ABRs.

Virtual links are a temporary solution and should be avoided in stable network designs. They add complexity, reduce reliability, and make troubleshooting more difficult. The recommended approach is to ensure all areas are directly connected to Area 0. Virtual links are configured between two ABRs that share a common non-backbone area.

## Q85: What is the difference between OSPF neighbor and adjacency?
**A:** An OSPF neighbor is a router that has received hello packets from another router on the same network segment. Neighbors are discovered through hello packets and are listed in the neighbor table. Neighbors do not necessarily exchange routing information.

An OSPF adjacency is a formal relationship between two OSPF routers that have completed the full neighbor state machine. Adjacent routers exchange link-state advertisements and maintain synchronized link-state databases. Not all neighbors become adjacencies. On multi-access networks, routers form adjacencies only with the DR and BDR.

## Q86: What is the OSPF neighbor state machine?
**A:** The OSPF neighbor state machine defines the stages of forming an adjacency: Down, Init, 2-Way, ExStart, Exchange, Loading, and Full. In the Down state, no hello packets have been received. In Init, a hello packet has been received but the local router is not listed. In 2-Way, bidirectional communication is established.

ExStart determines the master/slave relationship and initial sequence numbers. Exchange involves exchanging database descriptions. Loading involves requesting and receiving specific LSAs. Full indicates that the link-state databases are synchronized. The state machine ensures that adjacencies are formed correctly and databases are synchronized.

## Q87: What is the purpose of the OSPF hello packet?
**A:** The OSPF hello packet is used to discover neighbors, establish adjacencies, maintain neighbor relationships, and elect the DR/BDR on multi-access networks. Hello packets are sent multicast to 224.0.0.5 (all OSPF routers) at regular intervals.

Hello packets contain the router's OSPF parameters including router ID, area ID, hello interval, dead interval, network mask, and neighbor list. Hello packets are essential for OSPF operation because they maintain the neighbor relationship and detect failures. If hello packets are not received within the dead interval, the neighbor is declared down.

## Q88: What is the difference between OSPF point-to-point and broadcast network types?
**A:** On point-to-point networks, OSPF forms an adjacency with the single neighbor on the segment. No DR/BDR election occurs. Hello packets are sent multicast to 224.0.0.5. This is the simplest and most efficient OSPF network type.

On broadcast networks, OSPF elects a DR and BDR to reduce the number of adjacencies. All routers form adjacencies only with the DR and BDR. The DR generates a Type 2 Network LSA for the segment. Hello packets are sent multicast to 224.0.0.5. Broadcast networks require DR/BDR election to prevent an O(n^2) adjacency problem.

## Q89: What is the difference between OSPF Type 1 and Type 2 external routes?
**A:** Type 1 external routes (E1) add the external cost to the internal cost to reach the ASBR. This means the total cost includes both the cost within the OSPF domain and the external cost. E1 is used when the external cost should be influenced by the internal topology.

Type 2 external routes (E2) use only the external cost, regardless of the internal cost to reach the ASBR. E2 is the default for redistributed routes. E2 is used when the external cost should be consistent regardless of where the route is injected. E2 can lead to suboptimal routing if the external cost does not reflect the true path cost.

## Q90: What is the role of the OSPF router LSA (Type 1)?
**A:** A Type 1 Router LSA is generated by every OSPF router and describes the router's links and their states. It contains information about point-to-point links, links to transit networks, stub networks, and virtual links. Router LSAs are flooded within the router's area only.

Router LSAs are the foundation of the OSPF link-state database. Every router generates at least one Router LSA, and the collection of all Router LSAs forms the topology map of the area. Router LSAs are refreshed every 30 minutes (LSRefreshTime) and have a maximum age of 60 minutes (MaxAge).

## Q91: What is the difference between OSPF SPF and SPF throttle timers?
**A:** The SPF algorithm runs when the link-state database changes. SPF throttle timers control how often the SPF algorithm can run to prevent excessive CPU utilization. The initial SPF delay is the time to wait before the first SPF calculation, the hold time is the minimum time between successive SPF calculations, and the maximum wait time is the maximum delay between calculations.

OSPF uses incremental SPF (iSPF) to recalculate only the affected parts of the shortest-path tree, reducing computation time. SPF throttle timers prevent a router from running SPF too frequently during periods of instability. Proper tuning of these timers is essential for fast convergence without overloading the CPU.

## Q92: What is the BGP community attribute?
**A:** BGP communities are 32-bit values attached to routes that are used for policy implementation. Communities are not used for routing decisions directly but serve as tags that can be matched in route maps to filter or modify routes. Communities are transitive, meaning they are propagated across AS boundaries unless explicitly removed.

Well-known communities include no-export (do not advertise outside the AS), no-advertise (do not advertise to any peer), and local-as (confederation boundary). Private communities are used within an organization for traffic engineering, route tagging, and policy enforcement. Communities are an essential tool for large-scale BGP policy implementation.

## Q93: What is the difference between BGP soft reconfiguration and route refresh?
**A:** Soft reconfiguration allows BGP to reprocess stored routes without tearing down the BGP session. Inbound soft reconfiguration re-applies inbound route maps to received routes. Outbound soft reconfiguration re-sends the outbound routing table to peers. This requires storing all received routes, consuming memory.

Route refresh (defined in RFC 2918) is a more efficient alternative that requests peers to re-send their routing tables without storing them. This reduces memory consumption and is preferred over soft reconfiguration. Both mechanisms allow policy changes to take effect without session reset, but route refresh is more scalable.

## Q94: What is the OSPF conditional default route?
**A:** A conditional default route in OSPF advertises a default route only when a specific condition is met. For example, a router might advertise a default route only if it has a default route in its own routing table from a specific source. This prevents the router from advertising a default route when it does not have valid connectivity.

The default-information originate command with the always keyword forces the router to advertise a default route unconditionally, while without always, the default route is advertised only when the router has a default route in its routing table. Conditional default routes are useful for ensuring that only routers with valid Internet connectivity advertise default routes.

## Q95: What is the impact of MTU on OSPF adjacency formation?
**A:** OSPF requires that neighbors have matching MTU values to form adjacencies. If the MTU values do not match, the routers may fail to exchange database descriptions, preventing adjacency formation. This is because OSPF database descriptions can be larger than the MTU of the link.

The MTU mismatch can cause the adjacency to get stuck in the ExStart or Exchange state. The fix is to ensure consistent MTU values across all OSPF interfaces or to use the ip ospf mtu-ignore command. This is a common issue in networks with mixed Ethernet types or tunnel interfaces that have different MTU values.

## Q96: What is the role of administrative distance in route redistribution?
**A:** When routes are redistributed from one protocol into another, they are assigned the administrative distance of the target protocol. For example, OSPF routes redistributed into EIGRP are assigned EIGRP's AD of 90 for internal routes. This can cause issues if the same destination is reachable via both protocols.

Mutual redistribution can cause loops when routes are redistributed back into the source protocol with a better AD. For example, OSPF routes redistributed into EIGRP may be redistributed back into OSPF with an AD of 110, which is less preferred than the original OSPF routes at AD 110. Route tags and route maps are used to prevent these loops.

## Q97: What is the difference between OSPF area types and their restrictions?
**A:** Regular areas accept all LSA types. Stub areas reject Type 5 external LSAs but accept Type 3 summary LSAs. Totally stubby areas reject both Type 3 and Type 5 LSAs, accepting only a default route. NSSAs accept Type 7 external LSAs from local ASBRs but reject Type 5 LSAs.

The restrictions on LSA types determine what routing information is available within the area. Stub and totally stubby areas reduce database and table size but limit connectivity options. NSSAs provide a compromise by allowing local external routes while still limiting external route flooding. The choice of area type depends on the network's connectivity requirements.

## Q98: What is the impact of asymmetric routing on network performance?
**A:** Asymmetric routing occurs when packets take different paths from source to destination than the return packets take. While not inherently problematic, asymmetric routing can cause issues with stateful devices like firewalls, NAT devices, and load balancers that expect to see both directions of a connection.

Asymmetric routing can also cause problems with QoS, as packets on different paths may receive different treatment. In networks with multiple routing protocols or route redistribution, asymmetric routing is common and must be managed through careful route filtering and policy configuration. Some applications are sensitive to asymmetric routing and may fail or perform poorly.

## Q99: What is the difference between route poisoning and route withdrawal?
**A:** Route poisoning is a technique where a router advertises a failed route with an infinite metric (e.g., 16 for RIP) to indicate that the route is unreachable. This immediately notifies neighbors that the route is down. Route poisoning is proactive and helps prevent loops during convergence.

Route withdrawal is the process of removing a route from the routing table and announcing its unavailability. In BGP, a route is withdrawn by sending a Withdrawn Routes message. In OSPF, a route is withdrawn by flushing the corresponding LSA. Route withdrawal is the mechanism by which routers communicate that they no longer have a path to a destination.

## Q100: What are the best practices for designing a routing architecture?
**A:** Best practices include: use a hierarchical design with clear separation between core, distribution, and access layers; choose appropriate routing protocols for each layer; implement route summarization at area boundaries to limit the scope of changes; use passive interfaces on access-layer links; and configure BFD for fast failure detection.

Additional practices include: design for redundancy with multiple equal-cost paths; use route filtering to prevent unauthorized route advertisements; implement consistent administrative distance policies; monitor routing table size and convergence times; use route maps for policy enforcement; and document all routing policies and configurations. Regular audits of routing tables and protocol configurations help maintain network stability and performance.
