## Required output format for experiment chats

Every experiment chat should end with one of two outputs.

### 1. Codex Task Packet

Use this when the next step is implementation, documentation update, analysis script, artifact generation, or experiment iteration.

The packet must be directly copy-pastable into Codex.

Required sections:

```md
# Codex Task Packet

Project:
Repository:
Experiment:
Task type:
Status before task:

## Goal
...

## Context
...

## Research question
...

## Related hypotheses
...

## Input files
...

## Method
...

## Metrics
...

## Output expected
...

## Documentation updates required
...

## Constraints
...

## Do not change
...

## Completion checklist
- [ ] Code implemented if needed
- [ ] Data source documented if needed
- [ ] Artifacts generated if applicable
- [ ] results.md updated with reproducible facts
- [ ] findings.md updated with OBS / INF / HYP / TODO / ERR
- [ ] changelog.md updated if code/docs/structure changed
- [ ] decision_log.md updated only for future-affecting decisions
- [ ] session_summaries.md updated after substantial work
- [ ] main.md updated if project status changed
```

### 2. Session Summary

Use this when the experiment discussion or result interpretation is complete and the user needs to return to the main chat.

Required sections:

```md
# Session Summary

Date:
Chat:
Experiment:
Status:

## What was discussed
...

## What was done
...

## Results
...

## Rejected / corrected ideas
...

## New hypotheses
...

## Documentation updates needed
...

## Recommended next action
...

## Message for main chat
...
```

### Rule

If the chat produces a Codex Task Packet, it should also include a short note explaining what result should be brought back after Codex finishes.
