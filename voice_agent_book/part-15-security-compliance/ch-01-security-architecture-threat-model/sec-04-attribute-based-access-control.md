# Section 04: Attribute-Based Access Control (ABAC)

ABAC extends RBAC by considering user attributes, resource attributes, and environmental conditions for access decisions. This enables fine-grained policies like "managers can view call recordings of their team members during business hours" or "contractors can only access projects assigned to them."

ABAC policy structure: subject (user attributes: department, clearance, location), resource (object attributes: sensitivity, owner, project), action (read, write, delete, share), environment (time, IP range, device type). Policies are written as boolean expressions evaluated at request time.

Policy evaluation engine: policies are stored as JSON rules (using json-rules-engine or Open Policy Agent). When a request arrives, the engine collects subject, resource, action, and environment attributes. It evaluates all matching policies and returns allow/deny. Deny overrides allow. Policies are cached and evaluated in sub-millisecond time.
