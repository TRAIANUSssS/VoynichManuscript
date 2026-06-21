# Rejected Findings

No rejected findings have been recorded for this experiment yet.

ERR-2026-06-21-001:
During implementation, the first generated `top_tokens.csv` and `top_glyphs.csv` used the top-20 subtotal as the denominator for proportions. This was rejected because it conflicted with the full frequency-table denominator. The script was corrected before final documentation, and the artifacts were regenerated.
