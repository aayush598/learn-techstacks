# Section 07: Reporting & Compliance

## Overview

On-call reporting tracks shift hours, SLA compliance, and overwork indicators. Reports provide visibility into team workload, individual contributions, and compliance with staffing policies. Data feeds into payroll, compliance audits, and capacity planning.

## Implementation Approach

```typescript
interface OnCallReport {
  period: TimeRange;
  teamId: string;
  members: OnCallMemberReport[];
  summary: OnCallSummary;
  slaCompliance: SLAComplianceReport;
  alerts: AlertReport;
}

interface OnCallMemberReport {
  userId: string;
  totalShifts: number;
  totalHours: number;
  ackRate: number;
  avgResponseTime: number;
  escalationsReceived: number;
  escalationsMissed: number;
  overworkScore: number;
}

class ReportingService {
  async generateReport(teamId: string, period: TimeRange): Promise<OnCallReport> {
    const [shifts, alerts, acknowledgments] = await Promise.all([
      this.scheduleService.getShifts(teamId, period),
      this.alertService.getAlerts(teamId, period),
      this.acknowledgmentService.getAcknowledgments(period),
    ]);

    const memberReports = await this.computeMemberReports(teamId, shifts, alerts, acknowledgments);

    return {
      period,
      teamId,
      members: memberReports,
      summary: this.computeSummary(memberReports),
      slaCompliance: this.computeSLACompliance(alerts, acknowledgments),
      alerts: this.computeAlertReport(alerts, acknowledgments),
    };
  }

  private async computeMemberReports(
    teamId: string,
    shifts: OnCallShift[],
    alerts: Alert[],
    acks: Acknowledgment[]
  ): Promise<OnCallMemberReport[]> {
    const team = await this.teamService.getTeam(teamId);
    const reports: OnCallMemberReport[] = [];

    for (const member of team.members) {
      const memberShifts = shifts.filter(s => s.userId === member);
      const memberAlerts = alerts.filter(a => a.assignee === member);
      const memberAcks = acks.filter(a => a.userId === member);

      const totalHours = memberShifts.reduce((h, s) => h + (new Date(s.end).getTime() - new Date(s.start).getTime()) / 3600000, 0);
      const responseTimes = memberAlerts.map(a => {
        const ack = memberAcks.find(ack => ack.alertId === a.id);
        return ack ? (new Date(ack.timestamp).getTime() - new Date(a.createdAt).getTime()) / 60000 : null;
      }).filter((t): t is number => t !== null);

      reports.push({
        userId: member,
        totalShifts: memberShifts.length,
        totalHours,
        ackRate: memberAlerts.length > 0 ? memberAcks.filter(a => memberAlerts.some(ma => ma.id === a.alertId)).length / memberAlerts.length : 0,
        avgResponseTime: responseTimes.length > 0 ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length : 0,
        escalationsReceived: memberAlerts.filter(a => a.escalationLevel > 0).length,
        escalationsMissed: memberAlerts.filter(a => a.status === 'escalated').length,
        overworkScore: this.computeOverworkScore(totalHours, shifts.length),
      });
    }

    return reports;
  }

  private computeOverworkScore(totalHours: number, shiftCount: number): number {
    // Score based on hours worked vs recommended limits
    const recommendedWeeklyHours = 40;
    const weeklyHours = totalHours / (shiftCount || 1);
    return Math.min(100, (weeklyHours / recommendedWeeklyHours) * 100);
  }

  private computeSLACompliance(alerts: Alert[], acks: Acknowledgment[]): SLAComplianceReport {
    const slaBreaches = alerts.filter(a => {
      const ack = acks.find(ack => ack.alertId === a.id);
      if (!ack) return true;
      const responseTime = (new Date(ack.timestamp).getTime() - new Date(a.createdAt).getTime()) / 60000;
      return responseTime > this.getSLATarget(a.severity);
    });

    return {
      totalAlerts: alerts.length,
      metSLAResponse: alerts.length - slaBreaches.length,
      slaBreaches: slaBreaches.length,
      complianceRate: alerts.length > 0 ? (alerts.length - slaBreaches.length) / alerts.length : 1,
      avgResponseTime: this.calculateAvgResponseTime(alerts, acks),
    };
  }

  private getSLATarget(severity: string): number {
    const targets: Record<string, number> = { critical: 15, major: 30, minor: 60, warning: 120 };
    return targets[severity] || 30;
  }

  private calculateAvgResponseTime(alerts: Alert[], acks: Acknowledgment[]): number {
    const times = alerts
      .map(a => {
        const ack = acks.find(ack => ack.alertId === a.id);
        return ack ? (new Date(ack.timestamp).getTime() - new Date(a.createdAt).getTime()) / 60000 : null;
      })
      .filter((t): t is number => t !== null);

    return times.length > 0 ? times.reduce((a, b) => a + b, 0) / times.length : 0;
  }

  private computeAlertReport(alerts: Alert[], acks: Acknowledgment[]): AlertReport {
    return {
      total: alerts.length,
      acknowledged: acks.length,
      unacknowledged: alerts.length - new Set(acks.map(a => a.alertId)).size,
      bySeverity: this.groupBy(alerts, 'severity'),
      avgTimeToAck: this.calculateAvgResponseTime(alerts, acks),
    };
  }

  private computeSummary(memberReports: OnCallMemberReport[]): OnCallSummary {
    return {
      totalShifts: memberReports.reduce((s, m) => s + m.totalShifts, 0),
      totalHours: memberReports.reduce((s, m) => s + m.totalHours, 0),
      avgAckRate: memberReports.reduce((s, m) => s + m.ackRate, 0) / memberReports.length,
      avgResponseTime: memberReports.reduce((s, m) => s + m.avgResponseTime, 0) / memberReports.length,
      overworkedMembers: memberReports.filter(m => m.overworkScore > 80).length,
    };
  }
}
```

## Integration Points

- **Payroll System**: Hours data export
- **Compliance Dashboard**: Regulatory reporting
- **Capacity Planning**: Workload distribution analysis

## Production Considerations

- **Data Retention**: Keep reports for compliance period (1-3 years)
- **Automated Reports**: Email weekly/monthly reports to team leads
- **Overwork Alerts**: Alert managers when team members exceed thresholds
