# Section 02: Salesforce SOAP Integration

## Overview

Salesforce SOAP integration provides access to Salesforce functionality not available through the REST API, including metadata operations, Apex web service calls, and the Bulk API for large data volumes. The SOAP API uses XML-based messaging with WSDL-defined contracts and is supported alongside the REST API for operations where SOAP provides capabilities REST does not, or where XML processing is more appropriate than JSON.

The SOAP adapter handles Salesforce's Enterprise WSDL (org-specific, includes custom fields and objects) and Partner WSDL (org-agnostic, uses dynamic field access). The adapter supports login-based session authentication (username/password + security token or SAML assertion) and OAuth 2.0 JWT Bearer flow for server-to-server authentication. Key SOAP operations include describeGlobal (list all objects), describeSObject (get field metadata), create/update/delete/upsert for all objects, query/queryMore (for result sets beyond 2000 records), and SOAP-based Bulk API for processing 100K+ records.

## Architecture

```
                    Salesforce SOAP Integration

   +------------------+     +------------------+     +------------------+
   | SOAP Client      | --> | XML Serializer   | --> | Salesforce       |
   | (SOAP.js)        |     | • Envelope       |     | SOAP API         |
   +------------------+     | • Headers        |     +------------------+
          |                 | • Body           |
          v                 | • Attachments    |
   +------------------+     +------------------+
   | Session Manager  |
   | • Login/SAML     |     +------------------+
   | • Session cache  | --> | Parser           |
   | • Renewal        |     | • XML→JSON       |
   +------------------+     | • Type coercion  |
                            | • Error mapping  |
                            +------------------+
```

## Design Decisions

- **Partner WSDL over Enterprise WSDL for multi-tenant:** Partner WSDL is org-agnostic and works across all Salesforce orgs without customization. Enterprise WSDL must be regenerated per org if custom fields change. For a multi-tenant platform connecting to hundreds of Salesforce orgs, Partner WSDL with dynamic field access via sObject is the only practical choice. Trade-off: Partner WSDL requires more complex dynamic field handling (field names as strings rather than typed properties).

- **Session pooling with automatic renewal:** SOAP sessions expire after a configurable timeout (default 2 hours for OAuth sessions). The adapter maintains a session pool with pre-authenticated sessions. Before each SOAP call, the adapter checks session validity and transparently renews expired sessions. Session renewal uses the OAuth refresh token flow. Trade-off: session pooling adds memory overhead but eliminates re-authentication latency from the critical path.

- **Bulk API for large volume operations with batching:** The SOAP-based Bulk API supports processing 100,000+ records per job in batches of up to 10,000 records. The adapter automatically switches to Bulk API for operations with more than 200 records. Bulk API jobs run asynchronously — the adapter submits the job, polls for completion, and retrieves results. Trade-off: asynchronous processing adds complexity and requires a callback or polling mechanism for result delivery.

## Implementation Approach

```
class SalesforceSoapAdapter {
  private sessionCache: Map<string, SoapSession>;

  async executeSoapCall<T>(operation: string, args: any): Promise<T> {
    const session = await this.getSession();
    const envelope = this.buildEnvelope(operation, args, session.sessionId);
    const response = await this.soapClient.postAsync(this.config.soapEndpoint, envelope);
    const parsed = this.parseResponse(response);
    if (this.isError(parsed)) {
      if (parsed.faultCode === 'sf:INVALID_SESSION_ID') {
        this.sessionCache.delete(this.config.orgId);
        return this.executeSoapCall(operation, args); // Retry with new session
      }
      throw new SalesforceError(parsed);
    }
    return parsed;
  }

  async bulkQuery(soql: string): Promise<QueryResult> {
    const job = await this.createBulkJob('query', soql);
    const batches = await this.submitBulkBatches(job, [soql]);
    const results = [];

    for (const batch of batches) {
      await this.waitForBatchComplete(job.id, batch.id);
      const batchResults = await this.getBatchResults(job.id, batch.id);
      results.push(...this.parseBatchResults(batchResults));
    }

    return { records: results, totalSize: results.length };
  }

  private async createBulkJob(operation: string, soql: string): Promise<BulkJob> {
    const session = await this.getSession();
    const jobXml = `
      <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
        <operation>${operation}</operation>
        <object>Contact</object>
        <contentType>CSV</contentType>
      </jobInfo>`;
    const response = await this.soapClient.postAsync(
      `${this.config.instanceUrl}/services/async/58.0/job`,
      jobXml,
      { headers: { 'X-SFDC-Session': session.sessionId } }
    );
    return this.parseJobResponse(response);
  }

  private async getSession(): Promise<SoapSession> {
    const cached = this.sessionCache.get(this.config.orgId);
    if (cached && Date.now() < cached.expiry - 300000) return cached; // 5-min buffer

    const session = await this.login();
    this.sessionCache.set(this.config.orgId, session);
    return session;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **SOAP** (MIT) | Node.js | SOAP client library |
| **xml2js** (MIT) | Node.js | XML to JSON parsing |
| **jsforce** (MIT) | Salesforce | SOAP + Bulk API support |

## Production Considerations

**Scaling:** SOAP sessions are expensive to create (1-3 seconds for login). Pool sessions aggressively and reuse across requests within the same tenant. The Bulk API should be used for all operations exceeding 200 records — it's designed for scale while single-record SOAP is for real-time operations. Monitor Bulk API job queue depth to ensure jobs are processing within SLO.

**Security:** SOAP connections use TLS 1.2+ only. Session IDs are as sensitive as passwords — never log session IDs, store them encrypted, and implement automatic session invalidation on integration disable. For JWT Bearer flow, protect the private key used for assertion signing.

**Monitoring:** Track SOAP call volume vs. REST volume, SOAP session creation rate and latency, Bulk API job completion rate and duration, session cache hit rate, and XML serialization/deserialization time. Alert on Bulk API job failures, session renewal failures, and SOAP call latency exceeding 5 seconds.
