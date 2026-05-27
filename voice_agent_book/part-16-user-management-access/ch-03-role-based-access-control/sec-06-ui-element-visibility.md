# UI Element Visibility

## Overview

UI element visibility ensures users only see interface components they have permission to access. This encompasses component-level permission checks, menu filtering, action button visibility, and conditional rendering patterns that create a seamless, secure user experience.

## Component-Level Permission Pattern

```
[User Session] → [Permission Context Provider]
                      │
            ┌─────────┼──────────┐
            ▼         ▼          ▼
    [Sidebar]   [Toolbar]   [DataTable]
      (menu)    (actions)   (row actions)
            │         │          │
            ▼         ▼          ▼
    [Permission Hook] → Render / Hide
```

## React Permission Hook

```typescript
import { useCallback, useMemo } from 'react';
import { useSession } from 'next-auth/react';
import { usePermissionEngine } from '@/hooks/usePermissionEngine';

interface PermissionCheckOptions {
  action: string;
  resource: string;
  resourceId?: string;
  fallback?: boolean; // What to show when we can't check yet (loading)
}

interface UsePermissionResult {
  allowed: boolean;
  loading: boolean;
  check: (action: string, resource: string, resourceId?: string) => boolean;
}

export function usePermission(): UsePermissionResult {
  const { data: session } = useSession();
  const engine = usePermissionEngine();
  const [loading, setLoading] = useState(true);
  const [cache, setCache] = useState<Map<string, boolean>>(new Map());

  const check = useCallback(
    (action: string, resource: string, resourceId?: string): boolean => {
      const key = `${action}:${resource}:${resourceId || '*'}`;

      // Check local cache
      if (cache.has(key)) return cache.get(key)!;

      // Optimistic: if user is admin, skip engine call
      if (session?.user?.roles?.includes('admin')) {
        const newCache = new Map(cache);
        newCache.set(key, true);
        setCache(newCache);
        return true;
      }

      // Async check via engine
      engine
        .check({
          userId: session!.user.id,
          tenantId: session!.user.tenantId,
          action,
          resource,
          resourceId,
        })
        .then(result => {
          const newCache = new Map(cache);
          newCache.set(key, result.allowed);
          setCache(newCache);
        });

      // Default to false while loading
      return false;
    },
    [session, engine, cache]
  );

  return { allowed: session?.user !== undefined, loading: !session, check };
}
```

## Component Guards

```typescript
// Wrapper component
interface CanProps {
  action: string;
  resource: string;
  resourceId?: string;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

function Can({ action, resource, resourceId, fallback = null, children }: CanProps) {
  const { check } = usePermission();
  const [allowed, setAllowed] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const result = check(action, resource, resourceId);
    setAllowed(result);
    setLoading(false);
  }, [action, resource, resourceId, check]);

  if (loading) return fallback;
  return allowed ? <>{children}</> : <>{fallback}</>;
}

// Usage in components
function AgentListPage() {
  return (
    <div>
      <Can action="create" resource="agents">
        <Button onClick={handleCreateAgent}>Create Agent</Button>
      </Can>

      <table>
        <tbody>
          {agents.map(agent => (
            <tr key={agent.id}>
              <td>{agent.name}</td>
              <td>
                <Can action="edit" resource="agents" resourceId={agent.id}>
                  <button onClick={() => editAgent(agent.id)}>Edit</button>
                </Can>
                <Can action="delete" resource="agents" resourceId={agent.id}>
                  <button onClick={() => deleteAgent(agent.id)}>Delete</button>
                </Can>
                <Can action="deploy" resource="agents" resourceId={agent.id}>
                  <button onClick={() => deployAgent(agent.id)}>Deploy</button>
                </Can>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Sidebar Menu Filtering

```typescript
interface MenuItem {
  label: string;
  path: string;
  icon: React.ComponentType;
  permission?: { action: string; resource: string };
  children?: MenuItem[];
}

const ALL_MENU_ITEMS: MenuItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: DashboardIcon },
  { label: 'Agents', path: '/agents', icon: AgentIcon, permission: { action: 'read', resource: 'agents' } },
  { label: 'Calls', path: '/calls', icon: CallIcon, permission: { action: 'read', resource: 'calls' } },
  { label: 'Campaigns', path: '/campaigns', icon: CampaignIcon, permission: { action: 'read', resource: 'campaigns' } },
  {
    label: 'Admin',
    path: '/admin',
    icon: AdminIcon,
    permission: { action: 'read', resource: 'admin' },
    children: [
      { label: 'Users', path: '/admin/users', icon: UserIcon, permission: { action: 'read', resource: 'users' } },
      { label: 'Billing', path: '/admin/billing', icon: BillingIcon, permission: { action: 'read', resource: 'billing' } },
      { label: 'Settings', path: '/admin/settings', icon: SettingsIcon, permission: { action: 'read', resource: 'settings' } },
    ],
  },
];

function useFilteredMenu(): MenuItem[] {
  const { check } = usePermission();

  return useMemo(() => {
    function filterMenuItems(items: MenuItem[]): MenuItem[] {
      return items
        .filter(item => {
          if (!item.permission) return true; // No permission required
          return check(item.permission.action, item.permission.resource);
        })
        .map(item => ({
          ...item,
          children: item.children ? filterMenuItems(item.children) : undefined,
        }));
    }

    return filterMenuItems(ALL_MENU_ITEMS);
  }, [check]);
}
```

## Conditional Rendering Strategies

```typescript
// Strategy 1: Server-side props (Next.js)
export async function getServerSideProps(context) {
  const session = await getSession(context);
  const permissionEngine = new PermissionEngine();

  const permissions = {
    canCreateAgent: await permissionEngine.check({
      userId: session.user.id, tenantId: session.user.tenantId,
      action: 'create', resource: 'agents',
    }),
    canDeleteAgent: await permissionEngine.check({
      userId: session.user.id, tenantId: session.user.tenantId,
      action: 'delete', resource: 'agents',
    }),
  };

  return { props: { permissions } };
}

// Strategy 2: Render props / slot pattern
interface ActionSlotProps {
  name: string;
  resource: string;
  resourceId?: string;
  render: (props: { onClick: () => void }) => React.ReactNode;
  fallback?: React.ReactNode;
}

function ActionSlot({ name, resource, resourceId, render, fallback }: ActionSlotProps) {
  const { check } = usePermission();
  const allowed = check(name, resource, resourceId);

  if (!allowed) return <>{fallback}</>;
  return render({ onClick: () => handleAction(name, resource, resourceId) });
}

// Usage
<ActionSlot
  name="delete"
  resource="agents"
  resourceId={agent.id}
  render={({ onClick }) => <DeleteButton onClick={onClick} />}
  fallback={<span className="text-gray-400">No permission</span>}
/>
```

## Data Table Row Filtering

```typescript
function AgentDataTable({ agents }: { agents: Agent[] }) {
  const { check } = usePermission();
  const columns = useMemo(() => {
    const cols: Column[] = [
      { key: 'name', label: 'Name' },
      { key: 'status', label: 'Status' },
      { key: 'phone', label: 'Phone' },
    ];

    // Conditionally add columns based on permissions
    if (check('read', 'billing')) {
      cols.push({ key: 'cost', label: 'Cost per Call' });
    }
    if (check('read', 'analytics')) {
      cols.push({ key: 'performance', label: 'Performance' });
    }

    return cols;
  }, [check]);

  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={col.key}>{col.label}</th>)}</tr>
      </thead>
      <tbody>
        {agents.map(agent => (
          <tr key={agent.id}>
            {columns.map(col => (
              <td key={col.key}>
                <ColumnRenderer column={col} agent={agent} />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Open-Source Tools

- **casbin** (Apache 2.0) — Available as React hook via @casbin/react
- **@casbin/react** (MIT) — React binding for Casbin permission checks
- **react-access-control** (MIT) — Declarative access control components

## Production Considerations

- Never rely solely on client-side permission checks; always enforce on server
- Pre-fetch user permissions on page load to avoid flickering UI elements
- Cache permission checks at the component level with memoization
- Handle permission loading state with skeleton placeholders
- Log permission denials at the UI level for debugging user access issues
- Provide custom 403 page component for routes that are entirely blocked
- Use permission-based feature flags for gradual feature rollout alongside access control
