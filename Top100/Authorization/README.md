# Authorization Interview Questions and Answers

## Q1: What is Authorization?
**A:** Authorization is the process of determining what resources a user or system can access and what operations they can perform after their identity has been authenticated. It enforces access control policies based on roles, permissions, or attributes.

## Q2: What is the difference between Authentication and Authorization?
**A:** Authentication verifies **who** you are (identity). Authorization verifies **what** you are allowed to do (permissions). Authentication precedes authorization — you must prove your identity before access rights are checked.

## Q3: What is Role-Based Access Control (RBAC)?
**A:** RBAC is an authorization model where permissions are assigned to roles, and users are assigned to those roles. Instead of managing permissions for each user individually, administrators manage roles. For example, an "Admin" role has full access, while a "Viewer" role has read-only access.

## Q4: What is Attribute-Based Access Control (ABAC)?
**A:** ABAC uses attributes (user attributes, resource attributes, environment conditions) to determine access. Policies are expressed as boolean rules evaluating these attributes. For example, "Allow access if user.department == resource.ownerDept AND time between 9 AM and 5 PM."

## Q5: What is Discretionary Access Control (DAC)?
**A:** DAC allows the owner of a resource to decide who can access it and what permissions they have. Each resource has an Access Control List (ACL) specifying authorized users and their permissions. File systems often use DAC (e.g., Unix file permissions).

## Q6: What is Mandatory Access Control (MAC)?
**A:** MAC enforces access control based on a central policy set by the system administrator. Users cannot change permissions on resources. It uses labels (e.g., classification levels like Top Secret, Secret, Confidential) and clearances. SELinux and NSA enforce MAC.

## Q7: What is an Access Control List (ACL)?
**A:** An ACL is a list of permissions attached to an object specifying which users or system processes have access and what operations they can perform. Each entry in an ACL defines a subject (user/group) and the allowed operations (read, write, execute).

## Q8: What is a capability-based security model?
**A:** In a capability-based model, access is granted by possessing an unforgeable token (capability) that confers specific rights to an object. Unlike ACLs (where access is based on identity), capabilities focus on what token you hold. Amoeba OS and some microkernels use this model.

## Q9: What is the Principle of Least Privilege?
**A:** The Principle of Least Privilege (PoLP) states that a user or system should be granted only the minimum permissions needed to perform their tasks. This limits the potential damage from errors, attacks, or misuse. It applies to both human users and service accounts.

## Q10: What is Privilege Escalation?
**A:** Privilege escalation is an attack where a user gains higher-level permissions than originally assigned. **Vertical escalation** means gaining higher privileges (user to admin). **Horizontal escalation** means accessing another user's resources at the same privilege level.

## Q11: What is vertical privilege escalation?
**A:** Vertical privilege escalation occurs when a user with limited privileges gains elevated access, such as a regular user becoming an administrator. Common vectors include exploiting application vulnerabilities, misconfigured permissions, or OS kernel exploits.

## Q12: What is horizontal privilege escalation?
**A:** Horizontal privilege escalation occurs when a user accesses resources belonging to another user at the same privilege level. For example, User A accessing User B's profile by manipulating an ID parameter in the URL (`/user/123` changed to `/user/456`).

## Q13: What is an Insecure Direct Object Reference (IDOR)?
**A:** IDOR is a vulnerability where an application exposes direct references to internal objects (like database IDs or file paths) without proper access control checks. For example, changing `invoice_id=1001` to `invoice_id=1002` in a URL to view another user's invoice.

## Q14: How do you prevent IDOR vulnerabilities?
**A:** (1) Use indirect object references (random UUIDs instead of sequential IDs). (2) Always verify authorization on every request, not just once at login. (3) Use parameterized queries. (4) Implement server-side access control checks before returning data. (5) Use random, non-predictable identifiers.

## Q15: What is the difference between authorization and access control?
**A:** Authorization is the broader concept of determining what a user can do. Access control is the mechanism by which authorization policies are enforced. Authorization defines the "what" and "who," while access control implements the "how."

## Q16: What is a permission in authorization?
**A:** A permission is the right to perform a specific action on a specific resource. Examples include `read:documents`, `write:documents`, `delete:users`, or `admin:system`. Permissions are the atomic unit of authorization and are typically assigned to roles rather than individual users.

## Q17: What is a policy in authorization?
**A:** A policy is a rule or set of rules that define access decisions. Policies combine subjects (who), actions (what), resources (which), and conditions (when/where). Policies can be evaluated locally or centrally using a Policy Decision Point (PDP).

## Q18: What is Policy-Based Access Control (PBAC)?
**A:** PBAC centralizes authorization decisions by separating policy management from application code. Policies are written declaratively (e.g., "Allow managers to view reports of their direct reports") and evaluated by a policy engine. Open Policy Agent (OPA) is a popular PBAC implementation.

## Q19: What is Open Policy Agent (OPA)?
**A:** OPA is an open-source, general-purpose policy engine that decouples policy decisions from application code. Policies are written in Rego, a declarative language. OPA evaluates queries against policies and data to produce authorization decisions. It's widely used in cloud-native environments.

## Q20: What is Rego in the context of OPA?
**A:** Rego is the declarative policy language used by Open Policy Agent. It is inspired by Datalog and allows expressing complex policies concisely. Rego policies define rules that evaluate to "allow" or "deny" based on input data (user, action, resource) and external data sources.

## Q21: What is a Policy Decision Point (PDP)?
**A:** A PDP is the system component that evaluates authorization policies and makes access decisions. It receives requests with attributes (user, action, resource, context) and returns a decision (Allow/Deny). It is distinct from the Policy Enforcement Point (PEP).

## Q22: What is a Policy Enforcement Point (PEP)?
**A:** A PEP is the component that intercepts access requests and enforces decisions made by the PDP. It sits at the boundary of the protected resource, sends requests to the PDP, and either allows or blocks access based on the decision. API gateways often act as PEPs.

## Q23: What is a Policy Administration Point (PAP)?
**A:** A PAP is the component that manages and defines authorization policies. It provides an interface for administrators to create, update, and delete policies. Changes made in the PAP are typically propagated to the PDP for evaluation.

## Q24: What is a Policy Information Point (PIP)?
**A:** A PIP is the component that provides external attribute data needed for policy evaluation. For example, a PIP might fetch a user's department from an HR system, current time from a time service, or device security posture from MDM software.

## Q25: What is Relationship-Based Access Control (ReBAC)?
**A:** ReBAC makes authorization decisions based on relationships between entities. For example, "A user can view a document if they are a member of a team that owns the document." Google's Zanzibar (used by Google Drive) popularized ReBAC.

## Q26: What is Google Zanzibar?
**A:** Zanzibar is Google's global authorization system that handles billions of access control checks daily. It uses a relationship-based model where access is determined by graph traversal. It inspired open-source projects like Ory Keto, SpiceDB, and Topaz.

## Q27: What is SpiceDB?
**A:** SpiceDB is an open-source, Zanzibar-inspired authorization database. It uses a graph-based relationship model and provides consistent, low-latency authorization checks. It supports concepts like namespaces, relations, and subjects to model complex permission systems.

## Q28: What is Ory Keto?
**A:** Ory Keto is an open-source access control server implementing Google Zanzibar-inspired concepts. It supports RBAC, ABAC, and ReBAC models. It provides a gRPC and REST API for managing relationships and performing access checks.

## Q29: What is Casbin?
**A:** Casbin is an open-source authorization library supporting multiple access control models (ACL, RBAC, ABAC). It uses a configuration file to define the model and a policy file to define rules. It is available for many programming languages including Go, Java, Python, and Node.js.

## Q30: What is a claim in authorization?
**A:** A claim is a statement about a subject (user or entity) that can be used for authorization. In JWT, claims are key-value pairs in the payload (e.g., `"role": "admin"`, `"department": "engineering"`). Claims are verified by the authorization system to make access decisions.

## Q31: How does JWT handle authorization?
**A:** JWTs can include authorization claims in their payload, such as `roles`, `permissions`, or `scopes`. The server verifies the JWT signature, then extracts these claims to determine what the user is allowed to do. This enables stateless authorization without database lookups.

## Q32: What is a scope in authorization?
**A:** A scope defines a specific permission or access level. In OAuth 2.0, scopes are requested by the client and granted by the user. Examples: `read:profile`, `write:posts`, `admin:users`. Scopes provide granular control over what an application can do on behalf of a user.

## Q33: What is delegated authorization?
**A:** Delegated authorization allows a user to grant an application limited access to their resources without sharing their password. OAuth 2.0 is the primary framework for delegated authorization. The user authorizes the application, and the application receives a limited access token.

## Q34: What is the difference between delegated authorization and impersonation?
**A:** Delegated authorization grants limited, scoped access — the app acts on behalf of the user with specific permissions. Impersonation gives the app full access as if it were the user. Delegation is more secure because it limits what the app can do.

## Q35: What is an authorization server?
**A:** An authorization server issues access tokens to clients after authenticating the resource owner and obtaining authorization. It exposes endpoints for authorization, token exchange, and token revocation. Examples include Auth0, Okta, Keycloak, and custom OAuth servers.

## Q36: What is a resource server?
**A:** A resource server hosts the protected resources and accepts access tokens from clients. It validates tokens (verifying signature, expiration, and scopes) before serving the requested data. APIs are resource servers. They do not handle authentication directly — they trust the authorization server.

## Q37: What is the OAuth 2.0 Authorization Code flow?
**A:** The Authorization Code flow involves the client receiving an authorization code after user authentication, which is then exchanged for an access token via a secure back-channel. It is the most secure OAuth flow as the token exchange happens server-to-server.

## Q38: What is the Client Credentials flow used for?
**A:** The Client Credentials flow is used for server-to-server authorization where no user is involved. The client authenticates with its own credentials and receives an access token. This is commonly used for backend services, cron jobs, and API integrations.

## Q39: What is the Device Authorization flow (Device Code flow)?
**A:** The Device Authorization flow is designed for devices with limited input capabilities (smart TVs, IoT devices). The device displays a code and URL; the user visits the URL on another device to authenticate and authorize. The device polls until authorization is complete.

## Q40: What is the difference between OAuth 2.0 and OAuth 2.1?
**A:** OAuth 2.1, published in 2023, consolidates best practices and deprecates insecure flows. Key changes: Implicit flow is removed, ROPC flow is removed, PKCE is required for all public clients, refresh token rotation is recommended, and absolute token expiration is enforced.

## Q41: What is UMA (User-Managed Access)?
**A:** UMA is an OAuth-based protocol that allows a resource owner to control access to their resources across multiple sites. It extends OAuth 2.0 with a claims-based authorization framework and asynchronous authorization flows. It is used in healthcare and personal data management.

## Q42: What is fine-grained authorization?
**A:** Fine-grained authorization allows access decisions based on specific attributes of users, resources, and context — not just roles. For example, "A user can edit only their own documents" vs. RBAC's "Any editor can edit any document." ABAC, ReBAC, and policy engines enable fine-grained control.

## Q43: What is coarse-grained authorization?
**A:** Coarse-grained authorization makes broad access decisions based on high-level attributes like user roles or groups. For example, "All admins can access the admin panel." It is simpler to implement but less flexible than fine-grained authorization.

## Q44: What is an authorization middleware?
**A:** An authorization middleware is a software component that intercepts requests before they reach the application handler and enforces access control. In Express.js, this might be a function that checks user roles before allowing access to routes. It sits between the authentication middleware and the route handler.

## Q45: How do you implement authorization in a REST API?
**A:** (1) Authenticate the user (get the identity). (2) Extract user claims/roles from the token. (3) Use middleware to check permissions before each route handler. (4) Check authorization at the resource level (ownership checks). (5) Return 403 Forbidden for unauthorized requests.

## Q46: What is a 401 vs 403 status code?
**A:** 401 Unauthorized means the user is not authenticated (not logged in or token invalid). 403 Forbidden means the user is authenticated but does not have permission to access the resource. 401 asks for authentication; 403 denies access after authentication.

## Q47: What is the `@PreAuthorize` annotation in Spring Security?
**A:** `@PreAuthorize` is a Spring Security annotation that allows method-level authorization using SpEL (Spring Expression Language). Example: `@PreAuthorize("hasRole('ADMIN')")` ensures only users with the ADMIN role can execute the method.

## Q48: What is `@PostAuthorize` in Spring Security?
**A:** `@PostAuthorize` evaluates authorization after the method executes, allowing checks based on the return value. Example: `@PostAuthorize("returnObject.owner == authentication.name")` ensures the user can only access their own resources.

## Q49: What is Spring Security's Filter Chain?
**A:** The Spring Security Filter Chain is a sequence of filters that process HTTP requests. Each filter handles a specific security concern (authentication, authorization, CSRF, CORS, etc.). The `FilterSecurityInterceptor` at the end of the chain makes the final authorization decision.

## Q50: What is a SecurityContext in Spring Security?
**A:** The SecurityContext holds the security information of the currently authenticated user. It contains an Authentication object with the principal, credentials, and granted authorities. It is stored in a thread-local holder (SecurityContextHolder) and is available throughout the request lifecycle.

## Q51: What is the expression `hasRole()` vs `hasAuthority()` in Spring Security?
**A:** `hasRole('ADMIN')` checks for the role `ROLE_ADMIN` (prefix added automatically). `hasAuthority('PERMISSION_WRITE')` checks for the exact authority without any prefix. Roles represent high-level groupings; authorities represent specific permissions.

## Q52: What is method-level security vs URL-level security?
**A:** URL-level security intercepts HTTP requests based on URL patterns (configured globally). Method-level security applies annotations on individual methods, providing finer-grained control. Method-level annotations (`@Secured`, `@PreAuthorize`) are evaluated after URL-level checks.

## Q53: What is role hierarchy in authorization?
**A:** Role hierarchy defines parent-child relationships between roles where a parent role inherits all permissions of its child roles. For example, `ROLE_ADMIN > ROLE_MODERATOR > ROLE_USER`. An admin automatically has all permissions of moderators and regular users.

## Q54: What is a session-based authorization?
**A:** Session-based authorization stores user permissions in the server-side session after login. On each request, the server retrieves the session, extracts the user's roles/permissions, and checks them against the required permissions for the requested resource.

## Q55: What is token-based authorization?
**A:** Token-based authorization embeds user permissions within a token (typically JWT). The server validates the token signature and extracts permissions from the token payload. This is stateless — no server-side session storage is needed, making it more scalable.

## Q56: What is attribute-based authorization in APIs?
**A:** Attribute-based authorization evaluates policies based on attributes of the user (department, clearance), the resource (classification, owner), and the environment (time, location, device). For example, "Allow access if user.clearance >= resource.classification AND user.location == 'office'."

## Q57: What is a permission bundle?
**A:** A permission bundle (or permission set) is a collection of individual permissions grouped together for convenient assignment. For example, a "Document Editor" bundle might include `read:documents`, `write:documents`, and `comment:documents`.

## Q58: What is a deny-override model?
**A:** In a deny-override model, if any policy denies access, the final decision is Deny regardless of any allow policies. This is the most restrictive and secure approach, commonly used as the default stance. It follows the principle: "Deny unless explicitly allowed."

## Q59: What is an allow-override model?
**A:** In an allow-override model, if any policy allows access, the final decision is Allow regardless of any deny policies. This is more permissive. Most security systems use deny-override for sensitive resources and may use allow-override for less critical ones.

## Q60: What is RBAC vs ABAC vs ReBAC comparison?
**A:** RBAC assigns roles to users; simple but can lead to role explosion. ABAC uses fine-grained attributes; flexible but complex to manage. ReBAC uses relationships between entities; natural for social/collaboration apps. Each suits different use cases; hybrid approaches are common.

## Q61: What is role explosion in RBAC?
**A:** Role explosion occurs when the number of roles grows unmanageably large because each unique combination of permissions requires a new role. For example, "Manager-DeptA", "Manager-DeptB", "Manager-DeptC". ABAC or attribute-based approaches can solve this.

## Q62: What is a permission check at the database level?
**A:** Database-level permission checking (row-level security) enforces access control within database queries. For example, adding `WHERE user_id = ?` to all queries. PostgreSQL Row-Level Security (RLS) allows defining policies directly in the database.

## Q63: What is PostgreSQL Row-Level Security (RLS)?
**A:** PostgreSQL RLS enables access control at the row level within the database. Policies are defined using `CREATE POLICY` and automatically applied to all queries. For example: `CREATE POLICY user_policy ON documents FOR SELECT USING (owner_id = current_user_id())`.

## Q64: What is a priviledged access management (PAM)?
**A:** PAM (or privileged identity management) refers to systems that manage and monitor accounts with elevated permissions (administrators, root accounts). It includes just-in-time access, session recording, credential rotation, and approval workflows. CyberArk is a leading PAM solution.

## Q65: What is just-in-time (JIT) access?
**A:** JIT access grants elevated permissions only when needed and for a limited duration. Instead of always having admin rights, a user requests temporary elevation that expires automatically. This reduces the attack surface and follows least privilege principles.

## Q66: What is time-based access control?
**A:** Time-based access control restricts access to specific time windows. For example, "Access to payment system only allowed between 9 AM and 5 PM on weekdays." This is an example of environmental/contextual attribute in ABAC.

## Q67: What is location-based access control?
**A:** Location-based access control restricts access based on geographic location (IP geolocation, GPS). For example, "Access to company data only allowed from the office network" or "Block access from countries on the sanctions list."

## Q68: What is device-based access control?
**A:** Device-based access control checks device attributes (managed vs. unmanaged, OS version, encryption status, jailbreak status) before granting access. Mobile device management (MDM) and conditional access policies in Azure AD enforce device-based controls.

## Q69: What is conditional access?
**A:** Conditional access is a risk-based authorization approach that evaluates signals (user, device, location, behavior) to enforce policies. For example, "Require MFA if logging in from a new device" or "Block access if the device is non-compliant." Azure AD Conditional Access is a prominent implementation.

## Q70: What is the Azure AD Authorization model?
**A:** Azure AD (now Microsoft Entra ID) uses a claims-based authorization model. Applications receive tokens containing claims about the user. The application evaluates these claims against its own authorization logic. Azure AD also supports RBAC, ABAC, and conditional access policies.

## Q71: What is AWS IAM Authorization?
**A:** AWS IAM uses policy-based authorization. Policies are JSON documents that specify allowed or denied actions on resources (ARNs). Policies can be attached to users, groups, roles, or directly to resources. IAM evaluates policies based on explicit deny, allow, and default deny.

## Q72: What is an AWS IAM Policy?
**A:** An IAM Policy is a JSON document specifying permissions. It includes: Effect (Allow/Deny), Action (e.g., `s3:GetObject`), Resource (e.g., `arn:aws:s3:::my-bucket/*`), and Condition (optional, e.g., IP address restriction). AWS evaluates all policies to make authorization decisions.

## Q73: What is an IAM Role in AWS?
**A:** An IAM Role is an identity with permissions that can be assumed by trusted entities (users, services, or federated identities). Unlike users (long-term credentials), roles provide temporary security credentials via AWS STS (Security Token Service).

## Q74: What is AWS STS (Security Token Service)?
**A:** AWS STS is a service that generates temporary, limited-privilege credentials for IAM roles or federated users. Credentials have configurable expiration (15 minutes to 36 hours). STS is used for cross-account access, role assumption, and federated user access.

## Q75: What is a service control policy (SCP) in AWS?
**A:** SCPs are AWS Organizations policies that define the maximum permissions for member accounts. They do not grant permissions (IAM still does that) but set permission boundaries. Even if IAM allows an action, an SCP denying it will block it.

## Q76: What is GCP IAM authorization?
**A:** GCP IAM uses roles (predefined or custom) that contain permission sets. Policies bind members (users, groups, service accounts) to roles at a resource hierarchy level (organization, folder, project, resource). Roles are more coarse-grained than AWS's action-level policies.

## Q77: What is Kubernetes RBAC?
**A:** Kubernetes RBAC controls access to the Kubernetes API. It uses Roles and ClusterRoles (sets of rules defining allowed verbs on resources) bound to subjects (users, groups, service accounts) via RoleBindings and ClusterRoleBindings.

## Q78: What is a ClusterRole vs Role in Kubernetes?
**A:** A Role grants permissions within a specific namespace. A ClusterRole is cluster-scoped (not tied to a namespace) and can grant access to cluster-level resources (nodes, namespaces) or be used across all namespaces. Both are used with RoleBinding or ClusterRoleBinding.

## Q79: What is a RoleBinding vs ClusterRoleBinding in Kubernetes?
**A:** RoleBinding grants permissions defined in a Role (same namespace) or ClusterRole (namespace-scoped) to subjects within a specific namespace. ClusterRoleBinding grants cluster-wide access from a ClusterRole to subjects across all namespaces.

## Q80: What is an authorization bypass?
**A:** An authorization bypass is a security vulnerability where an attacker accesses protected resources without proper authorization. Common causes include missing access control checks, IDOR, path traversal, HTTP method tampering, and client-side access control that can be bypassed.

## Q81: What is path traversal in authorization?
**A:** Path traversal (directory traversal) exploits insufficient path validation to access files or resources outside the intended directory. Example: `../../etc/passwd` or using URL encoding to bypass filters. Proper input validation and using allowlists of resources prevent this.

## Q82: What is HTTP method tampering?
**A:** HTTP method tampering occurs when an application only checks authorization for standard methods (GET, POST) but not others (PUT, DELETE, PATCH, OPTIONS). Attackers may bypass checks by switching methods. Always enforce authorization regardless of HTTP method.

## Q83: What is mass assignment vulnerability?
**A:** Mass assignment (or auto-binding) occurs when an application automatically binds request parameters to internal objects, allowing attackers to modify fields they shouldn't. For example, setting `role=admin` during registration. Mitigations include allowlists of safe fields and DTOs.

## Q84: What is a confused deputy problem?
**A:** A confused deputy problem occurs when a privileged component is tricked by a less-privileged entity into performing unauthorized operations. In authorization, this often relates to CSRF — the browser (deputy) is confused into sending an authenticated request on behalf of an attacker.

## Q85: What is authorization caching and its trade-offs?
**A:** Authorization caching stores permission check results to improve performance. Trade-offs: stale permissions (a user's role changes but cached decisions persist), increased complexity in cache invalidation, and potential security gaps if cache is not properly invalidated.

## Q86: What is a permission matrix?
**A:** A permission matrix is a table mapping roles (rows) to permissions (columns). It provides a visual representation of who can do what. Example: Admin has Create/Read/Update/Delete on all resources; Editor has Read/Update on posts; Viewer has Read only.

## Q87: What is attribute-based policy evaluation?
**A:** Attribute-based policy evaluation evaluates rules against a set of attributes without predefined roles. For example: "If user.clearance >= document.classification AND user.country == document.country, allow access." Policies are evaluated at runtime for each access request.

## Q88: What is a policy engine?
**A:** A policy engine is software that evaluates authorization policies against input data and returns decisions. Popular policy engines include OPA, Casbin, and Amazon Cedar (used by AWS Verified Permissions). They support various policy languages and integration patterns.

## Q89: What is Amazon Cedar?
**A:** Amazon Cedar is an open-source policy language and evaluation engine used by AWS Verified Permissions and Amazon Verified Permissions. It enables fine-grained, attribute-based authorization with a human-readable policy language. Cedar policies are written as structured statements.

## Q90: What is AWS Verified Permissions?
**A:** AWS Verified Permissions is a managed service for fine-grained authorization. It uses the Cedar policy language. Developers define policies specifying who can access what, and the service evaluates access requests. It integrates with Cognito, IAM, and custom identity sources.

## Q91: What is a signed authorization token?
**A:** A signed authorization token (like a JWT) contains claims about the user and is cryptographically signed to prevent tampering. The server verifies the signature to trust the claims. This allows stateless authorization — the token encodes authorization information.

## Q92: What is opaque token vs structured token for authorization?
**A:** Opaque tokens are random strings that require server-side lookup (database/Redis) to retrieve authorization information. Structured tokens (JWTs) contain self-encoded authorization claims. Opaque tokens are revocable by deletion; structured tokens can't be revoked until expiration.

## Q93: What is a permission group?
**A:** A permission group is a collection of users sharing the same authorization profile. Instead of assigning permissions to each user, users are added to groups, and permissions are assigned to groups. This simplifies management at scale. Groups can also be nested.

## Q94: What is a superuser?
**A:** A superuser (root, administrator) is a user account with unrestricted access to all resources and operations. Superusers bypass standard authorization checks. While useful for system administration, superuser accounts pose significant security risks and should be tightly controlled.

## Q95: How do you handle authorization in microservices?
**A:** Approaches include: (1) API Gateway as central PEP — gateway validates tokens and forwards claims to services. (2) Decentralized — each service validates tokens and enforces its own policies with a shared PDP. (3) Sidecar pattern — authorization logic runs in a sidecar proxy (e.g., Istio with OPA).

## Q96: What is the API Gateway pattern for authorization?
**A:** In the API Gateway pattern, the gateway acts as a central Policy Enforcement Point. It authenticates requests, extracts user information, checks basic authorization, and forwards requests to downstream services with verified identity headers. This centralizes security logic.

## Q97: What is a SaaS authorization model (multi-tenant)?
**A:** Multi-tenant authorization isolates data and permissions between different customers (tenants). Each tenant's users can only access their own data. Implementations include tenant ID in tokens, row-level security with tenant filters, and separate databases per tenant.

## Q98: What is tenant isolation in authorization?
**A:** Tenant isolation ensures that one tenant's users cannot access another tenant's data. Levels include: (1) Shared database with tenant ID column (most common); (2) Separate schemas per tenant; (3) Separate databases per tenant. Authorization must enforce the tenant boundary at every layer.

## Q99: How do you audit authorization decisions?
**A:** Authorization audit logs should capture: who (user ID), what (action), which resource, when (timestamp), where (IP/device), decision (allow/deny), and why (policy/rule used). Logs should be immutable, centrally collected, and regularly reviewed. Splunk, ELK, and cloud audit trails are common tools.

## Q100: What is the future of authorization?
**A:** Authorization is moving toward: (1) Policy-as-code (OPA, Cedar) separating policy from application logic. (2) Distributed authorization with Zanzibar-like systems. (3) Real-time, context-aware policies (conditional access). (4) Zero-trust architectures where authorization is checked continuously, not just at login boundary.
