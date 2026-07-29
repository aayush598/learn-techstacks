# Robotics Consulting: ROS, Automation Systems, Industrial Robotics

## Overview

Robotics consulting integrates mechanical, electrical, and software engineering. As automation accelerates across industries, robotics consultants are in high demand.

This guide covers how to freelance as a robotics consultant, what services command premium rates, and how to find clients.

## Why Robotics Consulting Pays Well

1. **Interdisciplinary**: Requires software + hardware + systems thinking
2. **Growing demand**: Automation is accelerating across all industries
3. **High stakes**: Robots can cause physical damage or injury
4. **Ongoing need**: Robotics systems need continuous improvement and maintenance
5. **Capital-intensive**: Companies investing in automation have budget for consultants

### Rate Reality

| Service | Junior (2-4yr) | Mid (4-7yr) | Senior (7-12yr) | Expert (12yr+) |
|---------|---------------|-------------|-----------------|----------------|
| ROS/ROS2 Development | $80-120/hr | $120-175/hr | $175-250/hr | $250-400/hr |
| Robot Software Architecture | $100-150/hr | $150-225/hr | $225-300/hr | $300-450/hr |
| Industrial Automation | $100-150/hr | $150-225/hr | $225-325/hr | $325-500/hr |
| Robotics Perception/CV | $100-150/hr | $150-225/hr | $225-325/hr | $325-500/hr |
| Motion Planning | $100-150/hr | $150-225/hr | $225-325/hr | $325-450/hr |
| Robotics Systems Integration | $100-150/hr | $150-200/hr | $200-300/hr | $300-450/hr |

## Service Offerings

### Service 1: ROS/ROS2 Development

**What you do**: Build robot software using Robot Operating System (ROS/ROS2).

**ROS is the de facto standard for robot software** — most robotics companies use it.

**Services**:
- ROS/ROS2 node development (sensor drivers, controllers, planners)
- Custom message and service definitions
- Launch file and parameter configuration
- ROS2 migration (from ROS1 — many companies still need this)
- Hardware drivers for sensors, actuators, cameras
- Simulation setup (Gazebo, Ignition, Webots)
- Multi-robot systems

**Pricing**:
- Simple ROS node/package: $5-15K
- Robot software architecture (full system): $30-100K
- ROS1 to ROS2 migration: $20-60K
- Simulation environment: $10-40K

### Service 2: Robot Software Architecture

**What you do**: Design the software architecture for a robot.

**Architecture components**:
- Hardware abstraction layer
- Sensor fusion pipeline
- Perception pipeline (camera, LIDAR, IMU, etc.)
- State estimation (localization, mapping)
- Planning (path, motion, task)
- Control (low-level motor control)
- Communication (internal and external)
- Safety monitoring
- Diagnostics and logging
- OTA update mechanism

**Deliverables**:
- Architecture diagrams (component, deployment, data flow)
- Technology stack recommendation
- Hardware-software interface specification
- Development roadmap

**Pricing**: $15-50K for architecture design

### Service 3: Perception and Computer Vision

**What you do**: Build the perception systems that let robots understand their environment.

**Applications**:
- Object detection and recognition (YOLO, DETR, custom)
- 3D perception (LIDAR, depth cameras, stereo vision)
- SLAM (Simultaneous Localization and Mapping)
- Visual odometry
- People tracking and detection
- Pick-and-place vision
- Quality inspection

**Tools**: OpenCV, PCL (Point Cloud Library), PyTorch/TensorFlow, ROS perception stack, AprilTag/ArUco

**Pricing**: $20-80K for perception system

### Service 4: Motion Planning and Control

**What you do**: Make robots move smoothly, safely, and efficiently.

**Components**:
- Path planning (MoveIt, OMPL, custom)
- Trajectory optimization
- Inverse kinematics
- Collision avoidance
- Force/torque control (for assembly, polishing, etc.)
- Visual servoing

**Pricing**: $15-60K for motion planning system

### Service 5: Industrial Automation Consulting

**What you do**: Help factories and warehouses automate with robots.

**Services**:

**Automation feasibility study** ($10-30K)
- Which processes can be automated?
- ROI analysis
- Robot selection (arm type, payload, reach)
- Integration requirements

**Robot cell design** ($20-60K)
- Workcell layout
- Safety system design (light curtains, fencing, scanners)
- Gripper and tooling selection
- Programming (offline + online)

**System integration** ($30-100K)
- Robot programming (FANUC, ABB, KUKA, Universal Robots)
- PLC integration
- Vision system integration
- Conveyor tracking
- HMI/MES integration

**Pricing**:
- Feasibility study: $10-30K
- Cell design: $20-60K
- Integration: $50-200K

### Service 6: Mobile Robot Development

**What you do**: Build autonomous mobile robots (AMRs).

**Applications**:
- Warehouse logistics
- Delivery robots
- Cleaning robots
- Inspection robots
- Agricultural robots

**Components**:
- Chassis integration (motors, encoders, IMU)
- Localization (LIDAR SLAM, visual SLAM, UWB)
- Navigation (global + local planners)
- Obstacle avoidance
- Fleet management system
- Docking/charging

**Pricing**: $50-200K for AMR development

### Service 7: Robotic Arm Programming

**What you do**: Program industrial robotic arms for specific tasks.

**Robot brands**: FANUC, ABB, KUKA, Universal Robots, Yaskawa/Motoman, Epson, Denso

**Applications**:
- Pick and place
- Machine tending
- Welding
- Painting
- Assembly
- Palletizing
- Inspection

**Pricing**:
- Simple application (pick and place): $10-25K
- Complex application (welding, assembly): $25-60K
- Multi-robot cell: $50-150K

## Client Acquisition

### Where Robotics Clients Come From

**1. Manufacturing companies** (40%)
- Automotive, electronics, food & beverage, pharmaceutical manufacturers
- **Find**: Industry trade shows (Automate, IMTS, Hannover Messe)

**2. Robotics startups** (25%)
- Companies building new robot hardware
- **Find**: Robotics startup accelerators, VC portfolios, LinkedIn

**3. Logistics and warehousing** (15%)
- Amazon, Walmart, DHL, FedEx — and the companies that automate for them
- **Find**: Logistics industry events, MODEX, ProMat

**4. Research labs** (10%)
- University labs, government labs (NASA, DARPA, national labs)
- **Find**: Conference networking, academic publications

**5. Agriculture and construction** (10%)
- Precision agriculture, autonomous construction equipment
- **Find**: Industry-specific trade shows

### Ideal Client Profile

- Company investing in automation (manufacturing, logistics, or agriculture)
- Building a robot or robotic system that needs software
- Team has mechanical/electrical expertise but needs software help
- Budget: $30-500K for robotics development

### Outreach Script

```
Subject: Robotics software for [Project]

Hi [Name],

I'm a robotics software consultant specializing in
ROS/ROS2, perception, and motion planning.

I noticed [Company] is working on [robot/project].
Most robotics projects struggle with software —
it's the hardest part.

I help companies:
- Design robot software architecture
- Implement ROS/ROS2 systems
- Build perception and navigation
- Integrate hardware and software

Recent project: [Brief example with result]

If you could use robotics software expertise,
I'd love to discuss.

Best,
[Your Name]
[Link to robotics portfolio/GitHub]
```

## Technical Skills Required

### Core Robotics Skills

**Programming**:
- C++ (primary — most robotics is C++)
- Python (for prototyping, ML, tools)
- ROS/ROS2 (must know — industry standard)

**Software**:
- Linux (Ubuntu — primary robotics OS)
- Real-time systems basics
- Git, CI/CD for robotics
- Docker for robotics (growing)

**Mathematics**:
- Linear algebra (essential)
- Geometry and transforms (quaternions, rotation matrices)
- Kinematics (forward and inverse)
- Dynamics (mass, inertia, torque)
- Control theory (PID, LQR, MPC — at least concepts)

**Perception**:
- OpenCV (essential)
- Point Cloud Library (PCL)
- SLAM (gmapping, cartographer, ORB-SLAM, RTAB-Map)
- Object detection (YOLO, etc.)
- Camera calibration

**Hardware**:
- Sensors: LIDAR, cameras, IMU, encoders, force/torque
- Actuators: motors, servos, steppers
- Microcontrollers (STM32, ESP32) for low-level control
- Communication: CAN bus, EtherCAT, Ethernet, serial, I2C, SPI

### Nice-to-Have (Differentiators)

1. **Industrial robot programming**: FANUC TP, ABB RAPID, KUKA KRL, Universal Robots URScript
2. **PLC programming**: ladder logic, structured text (for manufacturing integration)
3. **Embedded systems**: for low-level robot controllers
4. **Machine learning**: for advanced perception and control
5. **Simulation**: Gazebo, Isaac Sim, MuJoCo, Webots
6. **Fleet management**: multi-robot coordination
7. **Safety standards**: ISO 10218, ISO/TS 15066 (robot safety)

### Certifications That Matter

| Certification | Value | Notes |
|-------------|-------|-------|
| FANUC Certification | Medium | For industrial robot programming |
| Universal Robots | Medium | Growing ecosystem, easy to learn |
| AWS RoboMaker | Low | Being deprecated, avoid |
| No specific ROS cert | N/A | Experience > certifications in robotics |

**Most important**: Demonstrated projects. Build a robot or participate in open-source robotics (ROS2, MoveIt, etc.).

## Robotics Software Stack

### Common Architecture

```
┌──────────────────────────────┐
│      Task Planning AI        │
├──────────────────────────────┤
│    Navigation / Motion       │
│  (Nav2, MoveIt, OMPL)       │
├──────────────────────────────┤
│     Perception / Localization│
│  (SLAM, Object Detection)   │
├──────────────────────────────┤
│       Hardware Interface     │
│  (ROS drivers, CAN, USB)    │
├──────────────────────────────┤
│    Robot Hardware / Sensors  │
└──────────────────────────────┘
```

### Popular Hardware Platforms

| Platform | Best For | Rate Premium if Expert |
|----------|---------|----------------------|
| Universal Robots | Light industrial, collaborative | +10% |
| FANUC | Heavy industrial | +15% |
| ABB | Automotive, assembly | +15% |
| KUKA | Automotive, heavy payload | +15% |
| Boston Dynamics | Research, advanced robotics | +30% |
| Clearpath/Ridgeback | Research, indoor robots | +10% |
| DJI | Drones | +10% |
| Custom (ROS-based) | Most flexible | +20% |

## Pricing Robotics Projects

### Pricing Ranges

| Project Type | Range | Duration |
|-------------|-------|----------|
| ROS node/package development | $5-20K | 2-6 weeks |
| Robot software architecture | $15-50K | 4-8 weeks |
| Perception system (CV/SLAM) | $20-80K | 8-16 weeks |
| Motion planning | $15-60K | 6-12 weeks |
| Industrial robot cell | $30-150K | 8-20 weeks |
| AMR development | $50-200K | 12-24 weeks |
| Full robot development | $100-500K+ | 6-18 months |
| Robotics audit/assessment | $10-30K | 2-4 weeks |

### Factors That Affect Price

1. **Hardware availability**: Do you have the robot to test on?
2. **Safety requirements**: Human-safe vs industrial (safety adds complexity)
3. **Environment**: Structured (factory) vs unstructured (outdoor, home)
4. **Precision requirements**: Pick-and-place (mm accuracy) vs assembly (micron accuracy)
5. **Integration complexity**: Standalone vs integrated with factory systems
6. **Existing codebase**: Greenfield vs legacy code maintenance

## Case Study Template

```
# Case Study: [Robot/System] Development

## The Challenge
[Client] needed to [task] with a robot. They had [hardware]
but needed software for [perception/navigation/manipulation].

## Our Solution
- Designed ROS2-based architecture
- Implemented [perception pipeline / motion planner]
- Integrated with [robot hardware]
- Set up simulation for testing
- Deployed and validated in [environment]

## Key Results
- Robot successfully [task] with [accuracy/speed/reliability]
- Development completed in [X] weeks
- Deployed in production at [customer site]
- Achieved [ROI/metric] for the client

## Client Quote
"[Name] brought deep robotics expertise to our project.
They designed a robust software architecture that
made our robot work reliably."
```

## Quick-Start Action Plan

### Month 1: Foundation
- [ ] Set up ROS2 development environment
- [ ] Complete ROS2 tutorials (core concepts, tools, navigation)
- [ ] Build a simulated robot in Gazebo (differential drive with LIDAR)
- [ ] Implement basic navigation (SLAM, path planning)

### Month 2: Portfolio
- [ ] Build 2-3 robotics projects (simulated or with real hardware)
- [ ] Document each with architecture, code, and demo video
- [ ] Create a robotics portfolio website
- [ ] Join ROS Discourse and contribute to discussions

### Month 3: First Client
- [ ] Reach out to 20 robotics companies and startups
- [ ] Network at robotics meetups and conferences
- [ ] Offer ROS consulting (code review, architecture review)
- [ ] Land first project ($10-30K)

### Month 4-6: Build Practice
- [ ] Complete 2-3 projects
- [ ] Build reusable ROS packages/components
- [ ] Develop testing and simulation infrastructure
- [ ] Raise rates 25%

### Month 7-12: Specialize
- [ ] Choose specialization (perception, manipulation, navigation, or industrial)
- [ ] Build expertise in 1-2 robot hardware platforms
- [ ] Speak at ROSCon, ICRA, or industry conference
- [ ] Consider creating a robotics product (ROS package, training course)

## Final Word

Robotics consulting combines the intellectual challenge of cutting-edge technology with the practical satisfaction of making things work in the real world.

The market is growing rapidly as automation spreads beyond automotive into every industry. ROS/ROS2 expertise is the most in-demand skill.

Start with simulation, then move to real hardware. Build a portfolio of working systems. Network at industry events. The robotics community is small and supportive — your reputation will travel fast.

If you can make robots work reliably, you'll never lack for clients.
