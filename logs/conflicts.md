# Conflicts

This file records contradictions between experiments, sources, or interpretations.

## C-001: Parser policy changes baseline and position results

Experiments:
- exp-001
- exp-002
- exp-002b

Conflict:
Historical `exp-001` and `exp-002` outputs used a parser that did not remove inline IVTFF angle-tag markup before token normalization. `exp-002b` uses a cleaned parser that replaces inline `<...>` markup with token boundaries. The cleaned rerun changes token count, unique token count, entropy, top-token counts, and line-position distribution distances.

Possible explanations:
Markup text such as `plant` entered old normalized tokens. Replacing tags with token boundaries also splits some strings that were previously joined across markup.

Next checks:
Decide whether cleaned parser outputs should supersede old parser-limited baselines for future work. Consider classifying IVTFF angle-tag roles rather than removing all inline `<...>` forms uniformly.

Status:
open

## Template

## C-XXX: Short conflict title

Experiments:
- exp-XXX
- exp-YYY

Conflict:
...

Possible explanations:
...

Next checks:
...

Status:
open / resolved / superseded
