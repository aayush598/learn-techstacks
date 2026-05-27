# Team Analytics & Reporting

## Overview

Team analytics provide per-team performance metrics, comparison dashboards, and department-level KPIs that enable managers to track productivity, identify coaching opportunities, and optimize team performance.

## Analytics Data Model

```typescript
interface TeamAnalytics {
  teamId: string;
  date: Date;
  period: 'daily' | 'weekly' | 'monthly';
  metrics: TeamMetrics;
  comparisons: TeamComparison[];
}

interface TeamMetrics {
  calls: {
    total: number;
    inbound: number;
    outbound: number;
    answered: number;
    missed: number;
    avgDuration: number;       // seconds
    totalDuration: number;     // seconds
  };
  agents: {
    active: number;
    online: number;
    offline: number;
    avgConcurrentCalls: number;
    avgUtilization: number;    // percentage
  };
  quality: {
    avgSatisfactionScore: number;  // 1-5
    avgSentimentScore: number;    // -1 to 1
    complianceScore: number;       // percentage
    firstCallResolutionRate: number;
  };
  productivity: {
    callsPerAgent: number;
    avgAfterCallWorkTime: number;   // seconds
    adherenceToSchedule: number;    // percentage
    overtimeHours: number;
  };
}

interface TeamComparison {
  metric: string;
  teamValue: number;
  departmentAvg: number;
  topTeamValue: number;
  percentile: number;            // 0-100
  trend: 'up' | 'down' | 'stable';
  changePercent: number;         // vs previous period
}
```

## Analytics Service

```typescript
class TeamAnalyticsService {
  async computeTeamMetrics(
    teamId: string,
    period: { start: Date; end: Date }
  ): Promise<TeamAnalytics> {
    const team = await this.teamService.getTeam(teamId);
    if (!team) throw new Error('Team not found');

    const memberIds = await this.teamService.getTeamMemberIds(teamId);

    const [callMetrics, agentMetrics, qualityMetrics, productivityMetrics] = await Promise.all([
      this.computeCallMetrics(memberIds, period),
      this.computeAgentMetrics(memberIds, period),
      this.computeQualityMetrics(memberIds, period),
      this.computeProductivityMetrics(memberIds, period),
    ]);

    const departmentId = team.departmentId;
    const departmentAvg = departmentId
      ? await this.computeDepartmentAverages(departmentId, period)
      : null;

    return {
      teamId,
      date: period.end,
      period: this.inferPeriodType(period),
      metrics: {
        calls: callMetrics,
        agents: agentMetrics,
        quality: qualityMetrics,
        productivity: productivityMetrics,
      },
      comparisons: [
        { metric: 'calls_per_agent', teamValue: productivityMetrics.callsPerAgent, departmentAvg: departmentAvg?.callsPerAgent || 0, topTeamValue: 0, percentile: 0, trend: 'stable', changePercent: 0 },
        { metric: 'avg_duration', teamValue: callMetrics.avgDuration, departmentAvg: departmentAvg?.avgDuration || 0, topTeamValue: 0, percentile: 0, trend: 'stable', changePercent: 0 },
        { metric: 'satisfaction', teamValue: qualityMetrics.avgSatisfactionScore, departmentAvg: departmentAvg?.avgSatisfactionScore || 0, topTeamValue: 0, percentile: 0, trend: 'stable', changePercent: 0 },
      ],
    };
  }

  async getTeamComparisonDashboard(departmentId: string): Promise<TeamComparisonDashboard> {
    const teams = await this.teamService.getDepartmentTeams(departmentId);
    const currentPeriod = this.getCurrentPeriod('monthly');

    const teamAnalytics = await Promise.all(
      teams.map(team => this.computeTeamMetrics(team.id, currentPeriod))
    );

    return {
      departmentId,
      period: currentPeriod,
      teams: teamAnalytics,
      rankings: {
        byCalls: this.rankTeams(teamAnalytics, 'calls.total'),
        bySatisfaction: this.rankTeams(teamAnalytics, 'quality.avgSatisfactionScore'),
        byUtilization: this.rankTeams(teamAnalytics, 'agents.avgUtilization'),
      },
      insights: this.generateInsights(teamAnalytics),
    };
  }

  private generateInsights(analytics: TeamAnalytics[]): Insight[] {
    const insights: Insight[] = [];
    const avgSatisfaction = analytics.reduce((sum, a) => sum + a.metrics.quality.avgSatisfactionScore, 0) / analytics.length;

    // Identify underperforming teams
    for (const team of analytics) {
      if (team.metrics.quality.avgSatisfactionScore < avgSatisfaction - 0.5) {
        insights.push({
          type: 'warning',
          teamId: team.teamId,
          metric: 'satisfaction',
          message: `Satisfaction score ${team.metrics.quality.avgSatisfactionScore.toFixed(1)} is below department average ${avgSatisfaction.toFixed(1)}`,
          suggestedAction: 'Review call recordings for coaching opportunities',
        });
      }
    }

    return insights;
  }
}
```

## Dashboard Components

```typescript
function TeamPerformanceCard({ teamId }: { teamId: string }) {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['teamAnalytics', teamId],
    queryFn: () => analyticsService.getTeamMetrics(teamId, { start: subDays(new Date(), 30), end: new Date() }),
  });

  if (isLoading) return <Skeleton />;

  return (
    <div className="team-performance-card">
      <div className="metric-grid">
        <MetricCard
          label="Calls"
          value={analytics.metrics.calls.total.toLocaleString()}
          trend={analytics.comparisons[0].trend}
          change={analytics.comparisons[0].changePercent}
        />
        <MetricCard
          label="Avg Duration"
          value={formatDuration(analytics.metrics.calls.avgDuration)}
          trend="stable"
        />
        <MetricCard
          label="Satisfaction"
          value={analytics.metrics.quality.avgSatisfactionScore.toFixed(2)}
          trend={analytics.comparisons[2].trend}
          badge={analytics.metrics.quality.avgSatisfactionScore >= 4.5 ? 'Excellent' : 'Needs Improvement'}
        />
        <MetricCard
          label="Utilization"
          value={`${analytics.metrics.agents.avgUtilization.toFixed(0)}%`}
          trend={analytics.comparisons[0].trend}
        />
      </div>
      <TeamComparisonChart comparisons={analytics.comparisons} />
    </div>
  );
}
```

## Open-Source Tools

- **Apache ECharts** (Apache 2.0) — Interactive chart library for dashboards
- **Recharts** (MIT) — React charting library
- **PostgreSQL** — Window functions for team comparisons and ranking

## Production Considerations

- Pre-compute daily team analytics via cron job (avoid real-time aggregation overhead)
- Cache team analytics in Redis with TTL based on update frequency
- Provide data export in CSV/PDF for team leads
- Allow custom date range selection with max 12-month lookback
- Anonymize individual agent data in team-level dashboards (privacy)
- Compare teams within same department only (cross-department comparison is misleading)
- Highlight statistically significant changes vs random variation
- Provide drill-down from team metrics to individual agent metrics
