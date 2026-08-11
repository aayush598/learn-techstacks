# MOTOR RUN LOG

**Folder:** `04-MOTOR-OPERATIONS/04-Monitoring-and-Logs/`

---

## 1. PURPOSE

The Motor Run Log is the **memory of the system**. Every time the motor runs —
scheduled, event, emergency, or test — the run is written down. In a dispute,
the log is the evidence. In an audit, the log is the check. Without the log,
"facts" become whoever shouts loudest; with it, facts stay facts.

## 2. EVERY RUN IS LOGGED — WITHOUT EXCEPTION

| Type of run | Logged? |
|-------------|---------|
| Scheduled normal run | Yes |
| Scheduled event run | Yes |
| Missed-slot compensation run | Yes |
| Emergency repair test run | Yes |
| ANY run outside the schedule | Yes — and additionally reported as an irregularity (`05-Irregularities/01-Unauthorized-Turning-On.md`) |

A run that was not logged **did not happen** for the purposes of the schedule —
and a run that happened but was not logged is itself an irregularity.

## 3. THE FIELDS — WHAT MUST BE RECORDED

| Field | Example |
|-------|---------|
| Date | 14 June 2026 |
| Scheduled slot | Morning G1, 05:00–06:00 |
| Reason (scheduled/event/emergency/test) | Scheduled |
| Event/booking reference, if any | EV-2026-014 |
| Actual start time | 05:02 |
| Actual stop time | 06:01 |
| Operator name and signature | R. Kumar (duty) |
| Backup/verifying signature where applicable | — |
| Gauge at start / at stop | 3.5 bar / 3.2 bar |
| Borewell level / discharge note | Level low |
| Volume estimate (meter or flow × time) | 4,100 litres |
| Anomalies (noise, leak, smell, power dip) | None / described |
| Next-slot impact (overrun into next slot?) | No |

The record sheet is the template at `12-TEMPLATES/04-Motor-Run-Log.md`.

## 4. WHEN AND HOW TO WRITE

1. The run is entered **immediately after the motor stops** — not at night,
   not next morning, not "from memory".
2. Times are read from the **clock in the motor room**, verified where installed
   by the dated video/photo evidence (`04-Digital-Video-Proof.md`).
3. The operator writes and signs; the backup verifies where two signatures are
   required for the duty period.
4. Entries are made in **ink in the bound log book**; blank lines are struck
   through; corrections are made by a single line, the correct value, initial,
   and date — never by erasure or whitening.

## 5. THE LOG IS EVIDENCE

1. The Motor Run Log is accepted as evidence in every dispute, grievance, and
   CRB proceeding (`07-CONFLICT-RESOLUTION/`).
2. A log entry prevails over memory, hearsay, and "I am sure it happened". To
   challenge an entry, a member must produce **other evidence** (photo, witness
   with a written statement, meter reading) — a vote cannot overrule a log.
   See `00-CONSTITUTION/04-Truth-Supremacy/04-No-Voting-on-Proven-Facts.md`.
3. The log book is kept in the motor room or the common office, open to every
   member at any time under the Right to Information
   (`00-CONSTITUTION/02-Fundamental-Rights/02-Right-to-Information-and-Audit.md`).

## 6. FALSIFYING THE LOG — A SERIOUS OFFENCE

| Act | Classification |
|-----|----------------|
| Backdating, altering, or erasing an entry | Falsification of records — **serious offence, Enforcement Ladder Level 4** |
| Signing a run as operated when it did not happen | Falsification — Level 4 |
| Destroying or withholding the log book | Falsification — Level 4 |
| Failing to log a run (carelessness, not deception) | First time: Level 1–2; repeated: escalation toward falsification review |

1. Falsification is the **highest-severity record offence** because it attacks
   the system's ability to know the truth (P5, P6).
2. Any member who suspects falsification reports it through
   `05-Irregularities/04-Reporting-Violations.md`, including anonymously.
3. Penalties follow the Enforcement Ladder
   (`07-CONFLICT-RESOLUTION/05-Enforcement/01-Enforcement-Ladder.md`), with
   recovery of any common-fund loss caused by the false entry.

## 7. SCENARIO: "THE MOTOR NEVER RAN FOR US"

Group C claims its slot was skipped. The operator's log shows the run at
05:15–06:10 for Group C, gauge 3.4→3.1, signed and verified, with a photo of the
panel clock during the run. The claim is checked against the log, the storage
check, and the photo — not by a vote. If the group's tanks genuinely stayed
empty despite the logged run, the next question is a **network problem** (valve,
pipe), investigated by the repair track, not a schedule fraud.

## 8. RETENTION

1. Completed log books are retained for a minimum of **5 years**
   (`11-LEGAL-AND-COMPLIANCE/03-Records-Retention.md`).
2. A digital copy of each log page is photographed/uploaded to the common
   archive at the end of each duty period.

---

*The log is the system's truth. Whoever writes it must write it true, whoever
reads it may rely on it, and whoever would falsify it attacks the constitution
itself.*
