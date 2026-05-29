# Section 04: Code Example Generation

## Overview

Code examples are automatically generated from the OpenAPI spec for multiple languages — TypeScript, Python, cURL, and Go. Each example includes the request configuration, authentication, and response handling. Examples are context-aware and update when the user modifies request parameters in the API explorer.

## Architecture

```
Code Example Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[OpenAPI Spec] → [Code Generator]
                     │
             ┌───────┴───────┐
             │               │
       [Template Engine]  [Language Templates]
             │               ├── typescript.mustache
             │               ├── python.mustache
             │               ├── curl.mustache
             │               └── go.mustache
             │
         [Generated Examples]
             │
     ┌───────┼───────┐
     │       │       │
   TS     Python   cURL   Go

Generated Example (List Agents):
  // TypeScript
  const client = new VoiceAgent({ apiKey: 'YOUR_API_KEY' });
  const agents = await client.agents.list({ status: 'active', limit: 20 });

  # Python
  client = VoiceAgent(api_key='YOUR_API_KEY')
  agents = client.agents.list(status='active', limit=20)

  # cURL
  curl -X GET 'https://api.voiceagent.com/v2/agents?status=active&limit=20' \
    -H 'Authorization: Bearer YOUR_API_KEY'

  // Go
  client := voiceagent.NewClient(apiKey)
  agents, err := client.Agents.List(ctx, &ListAgentsParams{
    Status: "active",
    Limit: 20,
  })
```

## Design Decisions

- **Template-Based Generation**: Mustache templates per language; easy to add new languages
- **Context-Aware**: Examples update when users change parameters in the explorer
- **Copy-to-Clipboard**: One-click copy for any code example
- **Language Detection**: Default language based on user preference or browser detection

## Implementation Approach

```typescript
// Code example generator
interface CodeGenerator {
  language: string;
  generate(operation: OperationExample): string;
}

interface OperationExample {
  method: string;
  path: string;
  baseUrl: string;
  headers: Record<string, string>;
  queryParams: Record<string, string>;
  pathParams: Record<string, string>;
  requestBody: unknown;
  responseStatus: number;
  responseBody: unknown;
}

// TypeScript generator
class TypeScriptGenerator implements CodeGenerator {
  language = 'typescript';

  generate(op: OperationExample): string {
    const lines: string[] = [];

    if (op.method === 'GET') {
      lines.push('import { VoiceAgent } from \'@voiceagent/sdk\';');
      lines.push('');
      lines.push('const client = new VoiceAgent({');
      lines.push('  apiKey: \'YOUR_API_KEY\',');
      lines.push('});');
      lines.push('');

      // Build method call
      const resource = this.getResource(op.path);
      const action = this.getAction(op.method, op.path);
      const params = this.buildParams(op);

      lines.push(`const result = await client.${resource}.${action}(${params});`);
      lines.push('console.log(result.data);');
    } else {
      lines.push('import { VoiceAgent } from \'@voiceagent/sdk\';');
      lines.push('');
      lines.push('const client = new VoiceAgent({');
      lines.push('  apiKey: \'YOUR_API_KEY\',');
      lines.push('});');
      lines.push('');

      const resource = this.getResource(op.path);
      const action = this.getAction(op.method, op.path);

      if (op.requestBody) {
        lines.push(`const result = await client.${resource}.${action}(`);
        lines.push(this.formatJson(op.requestBody, 0));
        lines.push(');');
      } else {
        lines.push(`const result = await client.${resource}.${action}();`);
      }
    }

    return lines.join('\n');
  }

  private getResource(path: string): string {
    const parts = path.split('/');
    return parts[2] || ''; // /v2/agents → agents
  }

  private getAction(method: string, path: string): string {
    if (path.includes('{')) return 'get';
    switch (method) {
      case 'GET': return 'list';
      case 'POST': return 'create';
      case 'PATCH': return 'update';
      case 'DELETE': return 'delete';
      default: return 'call';
    }
  }

  private buildParams(op: OperationExample): string {
    const params: string[] = [];

    for (const [key, value] of Object.entries(op.queryParams)) {
      if (value) params.push(`${key}: '${value}'`);
    }

    if (op.pathParams.id) {
      return `'${op.pathParams.id}'`;
    }

    if (params.length > 0) {
      return `{ ${params.join(', ')} }`;
    }

    return '';
  }

  private formatJson(data: unknown, indent: number): string {
    return JSON.stringify(data, null, 2)
      .split('\n')
      .map((line, i) => i === 0 ? line : '  '.repeat(indent + 1) + line)
      .join('\n');
  }
}

// Python generator
class PythonGenerator implements CodeGenerator {
  language = 'python';

  generate(op: OperationExample): string {
    const lines: string[] = [];

    lines.push('from voice_agent import VoiceAgent');
    lines.push('');
    lines.push('client = VoiceAgent(api_key="YOUR_API_KEY")');
    lines.push('');

    const resource = this.getResource(op.path);
    const action = this.getAction(op.method, op.path);

    if (op.method === 'GET' && Object.keys(op.queryParams).length > 0) {
      const params = Object.entries(op.queryParams)
        .filter(([, v]) => v)
        .map(([k, v]) => `${k}="${v}"`)
        .join(', ');

      lines.push(`result = client.${resource}.${action}(${params})`);
    } else if (op.method === 'POST' && op.requestBody) {
      lines.push(`result = client.${resource}.${action}(`);
      lines.push(this.formatPythonDict(op.requestBody, 1));
      lines.push(')');
    } else if (op.pathParams.id) {
      lines.push(`result = client.${resource}.${action}("${op.pathParams.id}")`);
    } else {
      lines.push(`result = client.${resource}.${action}()`);
    }

    return lines.join('\n');
  }
}

// cURL generator
class CurlGenerator implements CodeGenerator {
  language = 'curl';

  generate(op: OperationExample): string {
    const parts: string[] = [];
    parts.push(`curl -X ${op.method}`);

    const url = new URL(`${op.baseUrl}${op.path}`);
    for (const [key, value] of Object.entries(op.queryParams)) {
      if (value) url.searchParams.set(key, value);
    }

    parts.push(`'${url.toString()}'`);
    parts.push(`-H 'Authorization: Bearer YOUR_API_KEY'`);
    parts.push(`-H 'Content-Type: application/json'`);

    if (op.requestBody && op.method !== 'GET') {
      parts.push(`-d '${JSON.stringify(op.requestBody)}'`);
    }

    return parts.join(' \\\n  ');
  }
}

// Example display component
function CodeExample({ operation }: { operation: OperationExample }) {
  const [selectedLang, setSelectedLang] = useState('typescript');
  const generators = {
    typescript: new TypeScriptGenerator(),
    python: new PythonGenerator(),
    curl: new CurlGenerator(),
  };

  const code = generators[selectedLang].generate(operation);

  return (
    <div className="code-example">
      <div className="language-tabs">
        {Object.keys(generators).map(lang => (
          <button
            key={lang}
            className={selectedLang === lang ? 'active' : ''}
            onClick={() => setSelectedLang(lang)}
          >
            {lang === 'typescript' ? 'TypeScript' : lang.charAt(0).toUpperCase() + lang.slice(1)}
          </button>
        ))}
        <button
          className="copy-button"
          onClick={() => navigator.clipboard.writeText(code)}
        >
          Copy
        </button>
      </div>
      <pre><code>{code}</code></pre>
    </div>
  );
}
```

## Integration Points

- **OpenAPI Spec**: Examples generated from spec operation definitions
- **API Explorer**: Examples update in real-time as users modify parameters
- **SDK Docs**: SDK usage examples link to interactive explorer

## Production Considerations

- **Example Accuracy**: Generated examples must compile/run; test in CI
- **Language Coverage**: Prioritize TypeScript and Python; add languages based on demand
- **Authentication Handling**: Always use placeholder API keys; never embed real keys
- **Best Practices**: Generated examples follow language-specific best practices

## Open-Source Tools

- **Mustache/Handlebars**: Template engine for code generation
- **Scalar Code Example**: Built-in multi-language example generation
