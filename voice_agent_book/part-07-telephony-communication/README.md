# Part 07: Telephony & Communication Infrastructure

> **Duration:** Telephony Phase (Weeks 8-14)  
> **Goal:** Build the complete telephony stack with SIP trunking, WebRTC, inbound/outbound calling, IVR, and omnichannel routing.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Telephony Fundamentals & Protocols](ch-01-telephony-fundamentals-protocols/README.md) | SIP, RTP, WebRTC, PSTN, VoIP, codecs (Opus/PCMU/PCMA), signaling vs media |
| 02 | [SIP Trunk Integration](ch-02-sip-trunk-integration/README.md) | Asterisk/FreeSWITCH setup, SIP registration, trunk provisioning, failover routing |
| 03 | [WebRTC for Browser-Based Calling](ch-03-webrtc-browser-calling/README.md) | getUserMedia, RTCPeerConnection, media negotiation, STUN/TURN servers, Janus/Mediasoup |
| 04 | [Virtual Number Provisioning](ch-04-virtual-number-provisioning/README.md) | DID numbers, number search/release, porting, local/toll-free/toll, Twilio/Telnyx APIs |
| 05 | [Inbound Call Handling](ch-05-inbound-call-handling/README.md) | Call routing, IVR navigation, ACD, skill-based routing, time-of-day routing, caller ID |
| 06 | [Outbound Dialing System](ch-06-outbound-dialing-system/README.md) | Predictive dialer, preview dialer, progressive dialer, call pacing, answer detection |
| 07 | [IVR System Builder](ch-07-ivr-system-builder/README.md) | DTMF navigation, voice menus, IVR flow builder, IVR analytics, speech-enabled IVR |
| 08 | [SMS & WhatsApp Integration](ch-08-sms-whatsapp-integration/README.md) | Twilio SMS/Messaging API, WhatsApp Business API, message templates, media messaging |
| 09 | [Omnichannel Routing Engine](ch-09-omnichannel-routing-engine/README.md) | Channel prioritization, unified queue, context preservation across channels, channel switching |
| 10 | [Carrier Redundancy & Failover](ch-10-carrier-redundancy-failover/README.md) | Multi-carrier strategy, failover detection, automatic rerouting, load balancing, SLA monitoring |

---

## Key Open-Source Tools

- **FreeSWITCH** (MPL 2.0) — Media server & softswitch
- **Asterisk** (GPL 2.0) — PBX platform
- **Janus** (GPL 3.0) — WebRTC server
- **Mediasoup** (MIT) — WebRTC SFU
- **Coturn** (BSD) — STUN/TURN server
- **Jitsi** (Apache 2.0) — Video bridge (audio focus)

---

## Learning Objectives

- Understand telephony protocols and how they apply to AI voice agents
- Set up SIP trunking with failover for carrier-grade reliability
- Implement WebRTC for browser-based calling with STUN/TURN
- Build an IVR system with both DTMF and speech recognition
- Create inbound and outbound dialing systems with proper pacing
- Integrate SMS and WhatsApp channels alongside voice
- Design an omnichannel routing engine that preserves conversation context
- Implement carrier redundancy for high availability
