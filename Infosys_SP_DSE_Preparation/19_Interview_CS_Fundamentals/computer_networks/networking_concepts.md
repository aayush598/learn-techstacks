# Computer Networks Concepts for Infosys SP DSE Interview

## Table of Contents
1. [OSI Model](#osi-model)
2. [TCP/IP Model](#tcpip-model)
3. [TCP vs UDP](#tcp-vs-udp)
4. [HTTP vs HTTPS](#http-vs-https)
5. [DNS Resolution](#dns-resolution)
6. [IP Addressing](#ip-addressing)
7. [Subnetting Basics](#subnetting-basics)
8. [TCP Handshake](#tcp-handshake)
9. [Socket Programming](#socket-programming)
10. [REST API Basics](#rest-api-basics)
11. [Common Interview Questions](#common-interview-questions)

---

## OSI Model

```
Layer 7  ─── Application    ─── User interface (HTTP, FTP, SMTP, DNS)
Layer 6  ─── Presentation   ─── Data formatting, encryption (SSL/TLS)
Layer 5  ─── Session        ─── Session management (NetBIOS, RPC)
Layer 4  ─── Transport      ─── End-to-end delivery (TCP, UDP)
Layer 3  ─── Network        ─── Routing, IP addressing (IP, ICMP, Router)
Layer 2  ─── Data Link      ─── Frame, MAC address (Ethernet, Switch)
Layer 1  ─── Physical       ─── Bits on wire (Cables, Hubs, Signals)
```

### Detailed Layer Functions

| Layer | PDU | Protocols/Devices | Key Functions |
|-------|-----|-------------------|---------------|
| 7. Application | Data | HTTP, FTP, SMTP, DNS, DHCP | User interface, network services |
| 6. Presentation | Data | SSL/TLS, JPEG, ASCII | Data format, encryption, compression |
| 5. Session | Data | NetBIOS, RPC, PPTP | Session establishment, maintenance |
| 4. Segment | Segment | TCP, UDP | Port numbers, reliability, flow control |
| 3. Network | Packet | IP, ICMP, ARP, Router | Logical addressing, routing |
| 2. Data Link | Frame | Ethernet, MAC, Switch | Physical addressing, error detection |
| 1. Physical | Bit | Cables, Hubs, NIC | Bit transmission, electrical signals |

### Data Encapsulation

```
Layer 7:     [Data]
Layer 6:     [Data]
Layer 5:     [Data]
Layer 4:     [TCP Header | Data]           = Segment
Layer 3:     [IP Header | TCP Header | Data] = Packet
Layer 2:     [Frame Header | IP Header | ... | Frame Trailer] = Frame
Layer 1:     10101010101010101010101010101010 (bits)
```

---

## TCP/IP Model

```
┌─────────────────────────────────┐
│         Application             │  (HTTP, FTP, DNS, SMTP)
├─────────────────────────────────┤
│         Transport               │  (TCP, UDP)
├─────────────────────────────────┤
│         Internet                │  (IP, ICMP, ARP)
├─────────────────────────────────┤
│      Network Access             │  (Ethernet, Wi-Fi)
└─────────────────────────────────┘
```

### OSI vs TCP/IP

| OSI | TCP/IP | Focus |
|-----|--------|-------|
| 7 layers | 4 layers | TCP/IP is practical implementation |
| Theory model | Working model | OSI is reference model |
| Separate Presentation/Session | Combined into Application | TCP/IP simplifies |
| Strict layer separation | Layers more flexible | TCP/IP allows layer skipping |

---

## TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best-effort delivery |
| Order | Maintains order | No order guarantee |
| Speed | Slower (overhead) | Faster (minimal overhead) |
| Header size | 20-60 bytes | 8 bytes |
| Flow control | Yes (sliding window) | No |
| Error checking | Checksum + ACK | Checksum only |
| Broadcast | No | Yes |
| Use cases | Web, email, file transfer | Gaming, streaming, DNS, VoIP |

### TCP Header Structure
```
┌────────────────────────────────────────────────────┐
│ Source Port (16 bits) │ Destination Port (16 bits) │
├────────────────────────────────────────────────────┤
│              Sequence Number (32 bits)             │
├────────────────────────────────────────────────────┤
│           Acknowledgment Number (32 bits)          │
├──────┬───────┬──────────────────────────────────────┤
│Header│Flags  │           Window Size (16 bits)      │
│Length│SYNACK │                                      │
├──────┴───────┴──────────────────────────────────────┤
│             Checksum (16 bits)  │ Urgent Pointer   │
├────────────────────────────────────────────────────┤
│                  Options (variable)                 │
└────────────────────────────────────────────────────┘
```

### UDP Header Structure
```
┌────────────────────────────────────┐
│ Source Port (16 bits)              │
│ Destination Port (16 bits)         │
├────────────────────────────────────┤
│ Length (16 bits) │ Checksum (16)   │
└────────────────────────────────────┘
```

---

## HTTP vs HTTPS

| Feature | HTTP | HTTPS |
|---------|------|-------|
| Port | 80 | 443 |
| Security | Unencrypted | Encrypted (TLS/SSL) |
| URL prefix | http:// | https:// |
| Certificate | Not required | Required |
| Speed | Faster | Slightly slower |
| SEO | Lower ranking | Higher ranking |
| Use case | Non-sensitive data | Banking, login, payments |

### HTTPS Handshake
```
1. Client Hello → (supported ciphers, TLS version)
2. Server Hello ← (chosen cipher, certificate)
3. Client verifies certificate with CA
4. Key Exchange → (pre-master secret encrypted with server's public key)
5. Both generate session keys
6. Encrypted communication begins
```

### HTTP Methods
```
GET     - Retrieve data (read)
POST    - Create new resource
PUT     - Update/replace resource
PATCH   - Partial update resource
DELETE  - Remove resource
HEAD    - Same as GET but no body
OPTIONS - Describe communication options
```

---

## DNS Resolution

```
User types: www.example.com

Step 1: Browser cache → found? Use it
Step 2: OS cache → found? Use it
Step 3: Router cache → found? Use it
Step 4: ISP DNS cache → found? Use it
Step 5: Recursive DNS query:

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client   │───→│Resolver │───→│  Root    │───→│   TLD    │
│           │    │  (ISP)   │    │  Server  │    │  Server  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                      │                                │
                      │                                │
                      ▼                                ▼
                 ┌──────────┐                    ┌──────────┐
                 │  Local   │                    │Auth DNS  │
                 │  DNS     │                    │ Server   │
                 └──────────┘                    └──────────┘
                                                        │
                                                        ▼
                                                   ┌──────────┐
                                                   │  IP      │
                                                   │ Address  │
                                                   └──────────┘

DNS Record Types:
A       - IPv4 address
AAAA    - IPv6 address
CNAME   - Canonical name (alias)
MX      - Mail exchange
NS      - Name server
TXT     - Text record
PTR     - Reverse lookup
SOA     - Start of authority
```

---

## IP Addressing

### IPv4
```
Format: 32 bits (4 octets)
Example: 192.168.1.1
Binary: 11000000.10101000.00000001.00000001

Classes:
Class A: 1.0.0.0    to 126.255.255.255   (Network.Host.Host.Host)
Class B: 128.0.0.0  to 191.255.255.255   (Network.Network.Host.Host)
Class C: 192.0.0.0  to 223.255.255.255   (Network.Network.Network.Host)
Class D: 224.0.0.0  to 239.255.255.255   (Multicast)
Class E: 240.0.0.0  to 255.255.255.255   (Reserved)

Private IP ranges:
10.0.0.0    - 10.255.255.255    (Class A)
172.16.0.0  - 172.31.255.255    (Class B)
192.168.0.0 - 192.168.255.255   (Class C)

Special:
127.0.0.1   - Loopback (localhost)
0.0.0.0     - Default route
255.255.255.255 - Broadcast
```

### IPv6
```
Format: 128 bits (8 groups of 4 hex digits)
Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

Simplification rules:
- Leading zeros in group: 2001:0db8 → 2001:db8
- Consecutive zero groups: :: (once only)
- 2001:0000:0000:0000:0000:0000:0000:0001 → 2001::1

IPv6 advantages:
- Larger address space (2^128 vs 2^32)
- No NAT needed
- Built-in security (IPsec)
- Better QoS support
- Simpler header format
```

---

## Subnetting Basics

```
IP Address: 192.168.1.0
Subnet Mask: 255.255.255.0 (/24)

Number of hosts = 2^(32-24) - 2 = 254 hosts
(The -2 is for network and broadcast addresses)

Subnetting 192.168.1.0/24 into 4 subnets:
Need 2 more bits (2^2 = 4 subnets)
New mask: /26 (255.255.255.192)
Hosts per subnet: 2^(32-26) - 2 = 62

Subnets:
192.168.1.0/26    (192.168.1.1   - 192.168.1.62)
192.168.1.64/26   (192.168.1.65  - 192.168.1.126)
192.168.1.128/26  (192.168.1.129 - 192.168.1.190)
192.168.1.192/26  (192.168.1.193 - 192.168.1.254)

Quick Reference:
/24 = 255.255.255.0   = 254 hosts
/25 = 255.255.255.128 = 126 hosts
/26 = 255.255.255.192 = 62 hosts
/27 = 255.255.255.224 = 30 hosts
/28 = 255.255.255.240 = 14 hosts
/29 = 255.255.255.248 = 6 hosts
/30 = 255.255.255.252 = 2 hosts (point-to-point)
```

### CIDR Notation
```
IP/Prefix = Network + Subnet mask bits
192.168.1.0/24 means:
- Network: 192.168.1
- Hosts: 0-255
- Mask: 255.255.255.0

Calculate number of addresses: 2^(32 - prefix)
/24 → 2^8 = 256 addresses
/20 → 2^12 = 4096 addresses
```

---

## TCP Handshake

### Three-Way Handshake (Connection Establishment)

```
Client                          Server
  │                               │
  │──── SYN (seq=x) ────────────→│  Step 1: Client wants to connect
  │                               │
  │←── SYN-ACK (seq=y,ack=x+1) ──│  Step 2: Server agrees
  │                               │
  │──── ACK (ack=y+1) ──────────→│  Step 3: Client confirms
  │                               │
  │      Connection Established    │
```

### Four-Way Handshake (Connection Termination)

```
Client                          Server
  │                               │
  │──── FIN (seq=u) ────────────→│  Step 1: Client wants to close
  │                               │
  │←── ACK (ack=u+1) ───────────│  Step 2: Server acknowledges
  │                               │
  │      Server may still send    │
  │      data...                  │
  │                               │
  │←── FIN (seq=w) ──────────────│  Step 3: Server ready to close
  │                               │
  │──── ACK (ack=w+1) ──────────→│  Step 4: Client acknowledges
  │                               │
  │      Connection Closed        │
```

### Why Three-Way, Not Two-Way?
- Prevents old duplicate connections from being accepted
- Ensures both sides agree on initial sequence numbers
- The third ACK confirms server received SYN-ACK

### TCP States
```
CLOSED → LISTEN → SYN_RCVD → ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
    ↘                    ↘                        ↘
   SYN_SENT → ESTABLISHED   CLOSE_WAIT → LAST_ACK → CLOSED
```

---

## Socket Programming

### TCP Client-Server Example

```python
# Server
import socket

def tcp_server():
    host = 'localhost'
    port = 12345

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind and listen
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive data
        data = client_socket.recv(1024).decode()
        print(f"Received: {data}")

        # Send response
        response = f"Echo: {data}"
        client_socket.send(response.encode())

        client_socket.close()

# tcp_server()
```

```python
# Client
import socket

def tcp_client():
    host = 'localhost'
    port = 12345

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((host, port))

    # Send data
    message = "Hello, Server!"
    client_socket.send(message.encode())

    # Receive response
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    client_socket.close()

# tcp_client()
```

### UDP Example

```python
# UDP Server
import socket

def udp_server():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP Server listening on {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")
        server_socket.sendto(b"Echo: " + data, addr)
```

```python
# UDP Client
import socket

def udp_client():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "Hello, UDP Server!"
    client_socket.sendto(message.encode(), (host, port))

    response, addr = client_socket.recvfrom(1024)
    print(f"Server response: {response.decode()}")
    client_socket.close()
```

---

## REST API Basics

### REST Principles
```
1. Client-Server: Separation of concerns
2. Stateless: Each request contains all info needed
3. Cacheable: Responses can be cached
4. Uniform Interface: Consistent resource access
5. Layered System: Client can't tell if connected directly
6. Code on Demand (optional): Execute code on server
```

### RESTful Endpoints
```
Base URL: https://api.example.com/v1

GET    /users          → List all users
GET    /users/123      → Get user 123
POST   /users          → Create new user
PUT    /users/123      → Update user 123 (full)
PATCH  /users/123      → Update user 123 (partial)
DELETE /users/123      → Delete user 123

Nested resources:
GET    /users/123/orders    → Get orders for user 123
POST   /users/123/orders    → Create order for user 123
```

### HTTP Status Codes
```
1xx: Informational
  100 Continue

2xx: Success
  200 OK
  201 Created
  204 No Content

3xx: Redirection
  301 Moved Permanently
  304 Not Modified

4xx: Client Error
  400 Bad Request
  401 Unauthorized
  403 Forbidden
  404 Not Found
  405 Method Not Allowed
  409 Conflict
  422 Unprocessable Entity
  429 Too Many Requests

5xx: Server Error
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
  504 Gateway Timeout
```

### REST API Example Request/Response

```python
# Flask REST API
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.update(data)
    return jsonify(user), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "Deleted"}), 204
```

### REST API Design Best Practices
```
1. Use nouns, not verbs: /users (not /getUsers)
2. Use plural: /users (not /user)
3. Version your API: /v1/users
4. Filter with query params: /users?role=admin&page=2
5. Use proper HTTP methods
6. Return proper status codes
7. Use HATEOAS (Hypermedia links)
8. Paginate large responses
9. Use consistent error format
```

---

## Common Interview Questions

### Q1: What is the difference between TCP and UDP?
**Answer:** TCP is connection-oriented, reliable, ordered, and slower. UDP is connectionless, unreliable, unordered, and faster. TCP for web/email; UDP for gaming/streaming/DNS.

### Q2: Explain TCP 3-way handshake.
**Answer:** SYN → SYN-ACK → ACK. Client sends SYN, server responds with SYN-ACK, client confirms with ACK. Ensures both sides agree on sequence numbers and prevents old duplicate connections.

### Q3: What happens when you type a URL in the browser?
**Answer:**
1. DNS resolution (URL → IP)
2. TCP handshake (3-way)
3. TLS handshake (if HTTPS)
4. HTTP request sent
5. Server processes request
6. HTTP response returned
7. Browser renders HTML
8. Additional resources loaded (CSS, JS, images)
9. TCP connection closed (4-way)

### Q4: What is the difference between HTTP and HTTPS?
**Answer:** HTTPS uses TLS/SSL encryption for secure communication. HTTP sends data in plaintext. HTTPS uses port 443, HTTP uses port 80. HTTPS requires a certificate.

### Q5: What is DNS?
**Answer:** Domain Name System translates domain names (google.com) to IP addresses. Uses hierarchical structure: root → TLD → authoritative servers. Supports caching at multiple levels.

### Q6: What is a subnet mask?
**Answer:** Divides IP address into network and host portions. /24 = 255.255.255.0 means first 24 bits are network, last 8 are host. Determines how many hosts can be on a network.

### Q7: What is NAT?
**Answer:** Network Address Translation maps private IPs to public IP. Allows multiple devices to share one public IP. Uses port numbers to track connections.

### Q8: What is ARP?
**Answer:** Address Resolution Protocol maps IP addresses to MAC addresses. When a device knows the IP but needs the MAC address for local communication, it broadcasts an ARP request.

### Q9: What is the difference between a hub and a switch?
**Answer:** Hub broadcasts to all ports (layer 1). Switch forwards to specific port using MAC addresses (layer 2). Switch is more efficient and secure.

### Q10: What is a load balancer?
**Answer:** Distributes incoming network traffic across multiple servers. Improves availability and reliability. Types: round-robin, least connections, IP hash. Can operate at L4 (transport) or L7 (application).

### Q11: What is CORS?
**Answer:** Cross-Origin Resource Sharing allows restricted resources to be requested from another domain. Server returns Access-Control-Allow-Origin header. Prevents malicious sites from accessing APIs.

### Q12: What is the difference between a GET and POST request?
**Answer:** GET retrieves data, is idempotent, parameters in URL, can be cached. POST submits data, is not idempotent, parameters in body, not cached.

---

## Quick Reference Cheat Sheet

| Topic | Key Points |
|-------|-----------|
| OSI Model | 7 layers: Physical → Data Link → Network → Transport → Session → Presentation → Application |
| TCP/IP Model | 4 layers: Network Access → Internet → Transport → Application |
| TCP | Connection-oriented, reliable, ordered, slower |
| UDP | Connectionless, unreliable, faster, no overhead |
| TCP Handshake | SYN → SYN-ACK → ACK |
| TCP Termination | FIN → ACK → FIN → ACK |
| HTTP/HTTPS | Port 80/443, HTTPS encrypted with TLS |
| DNS | Domain → IP translation, hierarchical caching |
| IPv4 | 32-bit, dotted decimal (192.168.1.1) |
| IPv6 | 128-bit, hex notation (2001:db8::1) |
| Subnetting | /24 = 254 hosts, /25 = 126, /26 = 62 |
| REST API | Stateless, HTTP methods, JSON, status codes |
| Socket | Endpoint for communication (IP:Port) |
| MAC Address | 48-bit, physical address (permanent) |
| IP Address | 32/128-bit, logical address (changeable) |
| ARP | IP → MAC resolution |
| DHCP | Automatic IP assignment |
| NAT | Private → Public IP translation |
| Load Balancer | Distributes traffic across servers |
