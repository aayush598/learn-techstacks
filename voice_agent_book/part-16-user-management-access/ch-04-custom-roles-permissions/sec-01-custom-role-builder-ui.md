# Custom Role Builder UI

## Overview

The custom role builder provides a visual interface for creating and managing custom roles without engineering intervention. It features drag-and-drop permission assignment, a visual permission matrix, role configuration controls, and real-time validation feedback.

## UI Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Role Builder                                                │
├──────────────────┬──────────────────────────────────────────┤
│  Role Details     │  Permission Matrix                       │
│  ┌──────────────┐│  ┌──────────┬──────┬──────┬──────┬──────┐│
│  │ Name         ││  │ Resource │ Read │Write │Create│Delete││
│  │ Senior Agent ││  ├──────────┼──────┼──────┼──────┼──────┤│
│  │              ││  │ Agents   │  ✓   │  ✓   │  ✗   │  ✗   ││
│  │ Description  ││  │ Calls    │  ✓   │  ✓   │  ✓   │  ✗   ││
│  │ Can manage   ││  │Campaigns │  ✓   │  ✗   │  ✗   │  ✗   ││
│  │ agents+      ││  │Reports   │  ✓   │  ✓   │  ✓   │  ✗   ││
│  └──────────────┘│  │ Users    │  ✗   │  ✗   │  ✗   │  ✗   ││
│                   │  └──────────┴──────┴──────┴──────┴──────┘│
│  Base Role        │                                           │
│  [Agent ▼]        │  Scope Configuration                      │
│                   │  [Team ▼] [Sales Team ▼]                  │
│  Restrictions     │                                           │
│  ├─ Max Calls: 10 │  Advanced: Custom Conditions              │
│  └─ Duration: 2h │  + Add Condition                           │
└──────────────────┴───────────────────────────────────────────┘
```

## Component Implementation

```typescript
interface RoleBuilderState {
  name: string;
  description: string;
  baseRole: string | null;
  permissions: PermissionGrid;
  resourceScopes: ResourceScope[];
  restrictions: RoleRestriction[];
  conditions: PermissionCondition[];
  isValid: boolean;
  validationErrors: string[];
}

interface PermissionGrid {
  [resource: string]: {
    read: boolean;
    create: boolean;
    update: boolean;
    delete: boolean;
    [customAction: string]: boolean;
  };
}

function RoleBuilder() {
  const [state, dispatch] = useReducer(roleBuilderReducer, initialState);
  const [isSaving, setIsSaving] = useState(false);

  const handlePermissionToggle = useCallback((
    resource: string,
    action: string,
    value: boolean
  ) => {
    dispatch({
      type: 'TOGGLE_PERMISSION',
      payload: { resource, action, value },
    });
  }, []);

  return (
    <div className="flex gap-6">
      <RoleDetailsPanel
        name={state.name}
        description={state.description}
        baseRole={state.baseRole}
        onChange={(updates) => dispatch({ type: 'UPDATE_DETAILS', payload: updates })}
      />
      <PermissionMatrix
        permissions={state.permissions}
        allResources={AVAILABLE_RESOURCES}
        onToggle={handlePermissionToggle}
      />
      <RestrictionsPanel
        restrictions={state.restrictions}
        onChange={(r) => dispatch({ type: 'UPDATE_RESTRICTIONS', payload: r })}
      />
    </div>
  );
}
```

## Permission Matrix Component

```typescript
function PermissionMatrix({
  permissions,
  allResources,
  onToggle,
}: PermissionMatrixProps) {
  const resourceGroups = useMemo(() => groupByCategory(allResources), [allResources]);

  return (
    <div className="permission-matrix">
      <table>
        <thead>
          <tr>
            <th>Resource</th>
            <th>Read</th>
            <th>Create</th>
            <th>Update</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {resourceGroups.map(group => (
            <Fragment key={group.category}>
              <tr className="category-header">
                <td colSpan={5}>{group.category}</td>
              </tr>
              {group.resources.map(resource => (
                <tr key={resource.id}>
                  <td>{resource.label}</td>
                  {STANDARD_ACTIONS.map(action => (
                    <td key={action}>
                      <ToggleButton
                        checked={permissions[resource.id]?.[action] || false}
                        onChange={(checked) => onToggle(resource.id, action, checked)}
                        disabled={resource.immutable}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Validation Logic

```typescript
function validateRoleBuilderState(state: RoleBuilderState): ValidationResult {
  const errors: string[] = [];

  if (!state.name || state.name.trim().length < 2) {
    errors.push('Role name must be at least 2 characters');
  }

  if (state.name && state.name.length > 100) {
    errors.push('Role name must be 100 characters or less');
  }

  // Check for privilege escalation
  if (state.baseRole) {
    const basePermissions = getBaseRolePermissions(state.baseRole);
    for (const [resource, actions] of Object.entries(state.permissions)) {
      for (const [action, allowed] of Object.entries(actions)) {
        if (allowed && !basePermissions[resource]?.[action]) {
          // Exceeds base role permissions
          if (isSensitiveResource(resource, action)) {
            errors.push(`Cannot grant ${action} on ${resource} - exceeds base role "${state.baseRole}"`);
          }
        }
      }
    }
  }

  // Check for dangerous combinations
  if (state.permissions['billing']?.delete && !state.permissions['audit']?.read) {
    errors.push('Delete billing requires audit log read access');
  }

  if (state.restrictions.some(r => r.type === 'max_concurrent_calls' && r.value > 50)) {
    errors.push('Maximum concurrent calls cannot exceed 50');
  }

  return { isValid: errors.length === 0, errors };
}
```

## Open-Source Tools

- **React DnD** (MIT) — Drag-and-drop for role builder
- **React Table** (MIT) — Permission matrix table
- **Zustand** (MIT) — State management

## Production Considerations

- Debounce validation to avoid excessive computation during typing
- Show live preview of effective permissions as user configures the role
- Save drafts to localStorage to prevent losing work on navigation
- Track builder interactions (analytics) to identify confusing UX patterns
- Support keyboard navigation for accessibility
- Add undo/redo for permission changes
- Limit custom roles per tenant to prevent role sprawl (default 50)
