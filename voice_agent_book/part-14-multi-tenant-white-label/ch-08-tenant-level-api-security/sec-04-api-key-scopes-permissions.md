# Section 04: API Key Scopes & Permissions

API key scopes define what actions a key can perform across the API surface. Scopes follow a hierarchical permission model: resource type (calls, agents, recordings), action (read, write, admin), and granularity (specific agent, all agents). Scopes are assigned when the key is created and encoded in the key metadata.

Scope definition uses dot-notation: calls:read (read call logs), calls:write (initiate calls), agents:admin (modify agents, delete), recordings:read (access recordings). Wildcard scopes agents:* grant all actions on agents. Service accounts may have admin scopes while integration keys have read-only scopes.

Permission enforcement checks the scope at each endpoint using a declarative middleware pattern. The middleware compares the required scope against the key's assigned scopes. Scope mismatch returns 403 Forbidden with the required scope in the response body. Scope assignment is auditable for compliance.
