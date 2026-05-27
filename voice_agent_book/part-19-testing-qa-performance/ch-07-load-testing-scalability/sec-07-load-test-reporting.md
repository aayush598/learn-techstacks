# Section 07: Load Test Reporting

## Overview

Load test reporting transforms raw metrics into actionable insights. Reports combine performance data, infrastructure metrics, and pass/fail status into comprehensive summaries. Reports are auto-generated after each test run and published to dashboards, Slack, and email. They include executive summaries, baseline comparisons, bottleneck analysis, and recommendations.

## Design Decisions

- **Automated Generation**: Reports generated automatically after test completion
- **Multi-Audience Views**: Different views for different stakeholders
- **Baseline Comparison**: Key metrics compared against historical baselines
- **Visualizations**: Charts for latency distributions, throughput, resource usage

## Implementation Approach

```typescript
class LoadTestReporter {
  generateReport(testRun: LoadTestRun): LoadTestReport {
    return {
      summary: {
        testName: testRun.config.name, timestamp: testRun.completedAt,
        duration: testRun.duration, overallStatus: this.determineStatus(testRun),
        passRate: testRun.metrics.call_success_rate.rate,
      },
      performance: {
        responseTime: { p50: testRun.metrics.http_req_duration.values['p(50)'], p95: testRun.metrics.http_req_duration.values['p(95)'] },
        throughput: { avg: testRun.metrics.http_reqs.rate, max: testRun.metrics.http_reqs.values.max },
        voicePipeline: {
          sttLatency: { p50: testRun.metrics.stt_latency_ms.values['p(50)'], p95: testRun.metrics.stt_latency_ms.values['p(95)'] },
          llmLatency: { p50: testRun.metrics.llm_latency_ms.values['p(50)'], p95: testRun.metrics.llm_latency_ms.values['p(95)'] },
          ttsLatency: { p50: testRun.metrics.tts_latency_ms.values['p(50)'], p95: testRun.metrics.tts_latency_ms.values['p(95)'] },
        },
      },
      thresholds: {
        passed: testRun.thresholds.filter(t => t.passed).length,
        failed: testRun.thresholds.filter(t => !t.passed).length,
      },
      recommendations: this.generateRecommendations(testRun),
    };
  }
  async publish(report: LoadTestReport): Promise<void> {
    await this.storage.save(`reports/${report.testName}-${Date.now()}.json`, report);
    await this.slack.send({ channel: '#load-testing', blocks: this.formatSlackMessage(report) });
  }
}
```

## Integration Points

- **Slack**: Summary notifications
- **Grafana**: Dashboard annotations
- **S3/Blob Storage**: Report archive

## Open-Source Tools

- **k6-reporter** (MIT): HTML report generation
- **Handlebars** (MIT): Report template engine
- **Chart.js** (MIT): Embedded charts

## Production Considerations

- **Report Size**: Include summary by default; detailed data on demand
- **Storage Costs**: Archive old reports to cold storage
