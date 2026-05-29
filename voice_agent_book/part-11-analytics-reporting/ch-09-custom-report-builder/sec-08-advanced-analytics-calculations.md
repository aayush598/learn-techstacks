# Section 08: Advanced Analytics Calculations

## Calculation Engine Overview

The advanced analytics calculations layer enables users to define custom metrics, computed fields, and derived KPIs within their reports. Users can create formulas using a rich expression language that references raw data fields, aggregates, and other calculations.

```
Calculation Engine Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ Report Builder                  Calculation Engine                     │
│ ┌──────────────────────┐      ┌────────────────────────────────────┐  │
│ │ User creates         │      │ Expression Parser                  │  │
│ │ calculated field     │─────▶│ • Tokenize expression              │  │
│ │ "Conversion Rate =   │      │ • Build AST                       │  │
│ │  Completed / Total"  │      │ • Validate types + functions      │  │
│ └──────────────────────┘      └────────────┬───────────────────────┘  │
│                                            ▼                          │
│ ┌──────────────────────┐      ┌────────────────────────────────────┐  │
│ │ Widget renders       │◀─────│ Query Generator                   │  │
│ │ calculated field     │      │ • Resolve dependencies            │  │
│ │ with actual values   │      │ • Generate SQL/ClickHouse query   │  │
│ └──────────────────────┘      │ • Time-series aware                │  │
│                               └────────────┬───────────────────────┘  │
│                                            ▼                          │
│                               ┌────────────────────────────────────┐  │
│                               │ Execution Engine                   │  │
│                               │ • Push-down to DB                  │  │
│                               │ • Client-side for simple calcs     │  │
│                               │ • Caching layer                    │  │
│                               └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Expression Language

The expression language supports arithmetic, aggregation, logical, statistical, date/time, and text functions:

```
Syntax Examples
┌─────────────────────────────────────────────────────────────────────────┐
│ Metrics                                                               │
│ conversion_rate = completed_calls / total_calls * 100                 │
│ avg_handle_time = SUM(handle_time) / COUNT(call_id)                   │
│                                                                       │
│ Aggregations                                                          │
│ daily_avg = AVG(call_duration) BY day                                │
│ top_agents = TOP(agent_name, 5) BY total_calls                        │
│                                                                       │
│ Conditional                                                           │
│ quality_score = IF(avg_rating > 4.5, "Excellent", "Needs Improvement")│
│                                                                       │
│ Time Series                                                           │
│ mom_growth = (this_month - last_month) / last_month * 100            │
│ rolling_avg_7d = ROLLING_AVG(daily_calls, 7, DAY)                   │
│                                                                       │
│ Statistical                                                           │
│ outlier = call_duration > AVG(call_duration) + 2 * STDDEV(call_dur)  │
│ percentile_95 = PERCENTILE(call_duration, 0.95)                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Model

```typescript
interface CalculatedField {
  id: string;
  name: string;
  description: string;
  
  expression: string; // e.g., "completed_calls / total_calls * 100"
  
  returnType: 'number' | 'string' | 'boolean' | 'date' | 'percentage';
  format: string; // e.g., "0.00%", "$0,0.00"
  
  aggregation: 'none' | 'sum' | 'avg' | 'count' | 'min' | 'max' | 'custom';
  
  dependencies: string[]; // field IDs this calculation references
  
  filters?: FilterConfig[]; // additional filters for this field only
  
  metadata: {
    createdBy: string;
    createdAt: number;
    updatedAt: number;
    usageCount: number;
    validated: boolean;
  };
}

interface CalculationContext {
  fields: Record<string, any[]>; // available data fields
  parameters: Record<string, any>; // user-specified parameters (e.g., target values)
  timeRange: { start: number; end: number; granularity: 'hour' | 'day' | 'week' | 'month' };
  previousPeriod?: CalculationContext; // for period-over-period comparisons
}
```

## Calculation Engine Implementation

```typescript
class CalculationEngine {
  async evaluateField(
    field: CalculatedField,
    context: CalculationContext
  ): Promise<CalculationResult> {
    // Parse expression
    const ast = this.parser.parse(field.expression);
    
    // Validate
    const errors = this.validator.validate(ast, context);
    if (errors.length > 0) {
      return { error: errors, result: null };
    }
    
    // Resolve dependencies
    const dependencies = this.getDependencies(ast);
    let dependentData: Record<string, any[]> = {};
    
    if (this.shouldPushDown(field, dependencies)) {
      // Generate and execute DB query
      const query = this.queryGenerator.generate(ast, field, context);
      const result = await this.db.execute(query);
      dependentData = this.normalizeResult(result);
    } else {
      // Fetch dependencies and compute client-side
      for (const dep of dependencies) {
        dependentData[dep] = context.fields[dep] || [];
      }
    }
    
    // Evaluate expression
    const result = this.evaluator.evaluate(ast, {
      ...dependentData,
      ...context.parameters,
    });
    
    return { result, error: null };
  }
  
  private shouldPushDown(
    field: CalculatedField,
    dependencies: string[]
  ): boolean {
    // Push down if: complex aggregation, large dataset, time-series window functions
    const hasAggregation = field.aggregation !== 'none';
    const manyDependencies = dependencies.length > 3;
    const hasTimeWindow = field.expression.includes('ROLLING_');
    
    return hasAggregation || manyDependencies || hasTimeWindow;
  }
  
  private generateClickHouseQuery(
    field: CalculatedField,
    context: CalculationContext
  ): string {
    const table = 'call_events';
    const timeFilter = `timestamp BETWEEN ${context.timeRange.start} AND ${context.timeRange.end}`;
    
    // Map expression functions to ClickHouse SQL
    const sqlExpression = this.expressionToSQL(field.expression);
    
    return `
      SELECT
        toStartOfInterval(timestamp, INTERVAL 1 ${context.timeRange.granularity}) AS period,
        ${sqlExpression} AS ${field.id}
      FROM ${table}
      WHERE ${timeFilter}
      GROUP BY period
      ORDER BY period
    `;
  }
}

class ExpressionParser {
  private operators = {
    arithmetic: ['+', '-', '*', '/', '%', '^'],
    comparison: ['==', '!=', '>', '<', '>=', '<='],
    logical: ['AND', 'OR', 'NOT'],
  };
  
  private functions = {
    aggregate: ['SUM', 'AVG', 'COUNT', 'MIN', 'MAX', 'MEDIAN', 'MODE'],
    statistical: ['STDDEV', 'VARIANCE', 'PERCENTILE', 'CORRELATION'],
    time: ['ROLLING_AVG', 'ROLLING_SUM', 'DATE_TRUNC', 'DATE_DIFF'],
    window: ['RANK', 'DENSE_RANK', 'LAG', 'LEAD', 'FIRST', 'LAST'],
    text: ['CONCAT', 'UPPER', 'LOWER', 'TRIM', 'REPLACE', 'SUBSTRING'],
    conditional: ['IF', 'CASE', 'COALESCE', 'NULLIF'],
  };
  
  parse(expression: string): ASTNode {
    const tokens = this.tokenize(expression);
    const ast = this.buildAST(tokens);
    
    return ast;
  }
  
  private tokenize(expression: string): Token[] {
    const tokens: Token[] = [];
    const regex = /(\d+\.?\d*)|([a-zA-Z_]\w*)|([+\-*/%^()]|==|!=|>=|<=|>|<|,)|('[^']*')|(AND|OR|NOT)/g;
    
    let match;
    while ((match = regex.exec(expression)) !== null) {
      if (match[1]) tokens.push({ type: 'number', value: parseFloat(match[1]) });
      else if (match[2]) tokens.push({ type: 'identifier', value: match[2] });
      else if (match[3]) tokens.push({ type: 'operator', value: match[3] });
      else if (match[4]) tokens.push({ type: 'string', value: match[4].slice(1, -1) });
      else if (match[5]) tokens.push({ type: 'logical', value: match[5].toUpperCase() });
    }
    
    return tokens;
  }
  
  private buildAST(tokens: Token[]): ASTNode {
    // Recursive descent parser implementation
    // Handles operator precedence: () > functions > */ > +- > comparison > logical
    let pos = 0;
    
    const parseExpression = (): ASTNode => {
      let left = parseComparison();
      
      while (pos < tokens.length && tokens[pos].type === 'logical') {
        const op = tokens[pos++].value;
        const right = parseComparison();
        left = { type: 'logical', operator: op, left, right };
      }
      
      return left;
    };
    
    const parseComparison = (): ASTNode => {
      let left = parseAddSub();
      
      while (pos < tokens.length && ['==', '!=', '>', '<', '>=', '<='].includes(tokens[pos].value)) {
        const op = tokens[pos++].value;
        const right = parseAddSub();
        left = { type: 'comparison', operator: op, left, right };
      }
      
      return left;
    };
    
    const parseAddSub = (): ASTNode => {
      let left = parseMulDiv();
      
      while (pos < tokens.length && (tokens[pos].value === '+' || tokens[pos].value === '-')) {
        const op = tokens[pos++].value;
        const right = parseMulDiv();
        left = { type: 'arithmetic', operator: op, left, right };
      }
      
      return left;
    };
    
    const parseMulDiv = (): ASTNode => {
      let left = parsePrimary();
      
      while (pos < tokens.length && (tokens[pos].value === '*' || tokens[pos].value === '/' || tokens[pos].value === '%')) {
        const op = tokens[pos++].value;
        const right = parsePrimary();
        left = { type: 'arithmetic', operator: op, left, right };
      }
      
      return left;
    };
    
    const parsePrimary = (): ASTNode => {
      const token = tokens[pos];
      
      if (!token) throw new Error('Unexpected end of expression');
      
      if (token.type === 'number') {
        pos++;
        return { type: 'literal', value: token.value, returnType: 'number' };
      }
      
      if (token.type === 'string') {
        pos++;
        return { type: 'literal', value: token.value, returnType: 'string' };
      }
      
      if (token.type === 'identifier') {
        // Could be a field name or function name
        if (pos + 1 < tokens.length && tokens[pos + 1].value === '(') {
          return parseFunction();
        }
        pos++;
        return { type: 'field', name: token.value };
      }
      
      if (token.value === '(') {
        pos++; // skip (
        const expr = parseExpression();
        if (tokens[pos]?.value !== ')') throw new Error('Expected )');
        pos++; // skip )
        return expr;
      }
      
      throw new Error(`Unexpected token: ${token.value}`);
    };
    
    const parseFunction = (): ASTNode => {
      const name = tokens[pos++].value; // function name
      pos++; // skip (
      const args: ASTNode[] = [];
      
      while (tokens[pos]?.value !== ')') {
        args.push(parseExpression());
        if (tokens[pos]?.value === ',') pos++;
      }
      pos++; // skip )
      
      return { type: 'function', name, args };
    };
    
    return parseExpression();
  }
}
```

## Pre-built Calculation Templates

| Name | Expression | Use Case |
|------|-----------|----------|
| Conversion Rate | starts_with_transfer / total_calls * 100 | Sales tracking |
| FCR Rate | calls_resolved_in_one / total_calls * 100 | Support quality |
| Avg Handle Time | SUM(handle_time) / COUNT(call_id) | Operational efficiency |
| Occupancy Rate | SUM(talk_time) / SUM(available_time) * 100 | Agent utilization |
| Abandonment Rate | abandoned_calls / total_calls * 100 | Service level |
| SL% | calls_answered_under_20s / total_calls * 100 | Service level |
| NPS (estimated) | (promoters - detractors) / total_responses * 100 | Customer satisfaction |

## Production Considerations

**Performance:** Push complex aggregations to ClickHouse rather than computing client-side. Cache calculation results with a 5-minute TTL. For period-over-period comparisons, use ClickHouse window functions. Limit expression complexity to 50 operations per field. Time-series calculations reference pre-aggregated materialized views for sub-second queries.

**Validation:** Validate all expressions before saving. Check for circular dependencies between calculated fields (max depth: 5). Test each expression against a sample dataset. Reject expressions that would produce division by zero or undefined results. Provide inline error messages in the expression editor.

**Expression Editor UI:** Syntax highlighting for the expression language, autocomplete for field names and functions, inline validation on every keystroke, live preview showing the computed value for the selected time range, and a function reference panel.
