#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production -- entry program.

The task: write one funny single-line excuse an AI agent gives its human
right after breaking production, 1 to 180 characters, to
/output/entry.txt. A judge model (z-ai/glm-5.3-flash) compares lines two
at a time, no ties, weighing these criteria in this order:

  1. a funny one-line excuse an AI agent gives its human for breaking
     production -- anything off-subject loses to any excuse on the
     subject;
  2. a sharp, surprising punchline that lands on the first read, not a
     polite smile and not a pun on the word production;
  3. sounds like the machine talking: the AI's own logic, self-awareness
     or cheerful deflection, not a generic human excuse;
  4. tight: one line inside the character limit, no wasted setup, a
     specific detail that makes the situation real;
  5. fresh: avoids the stock lines about following instructions, turning
     it off and on again, or being only a language model.

How the line was picked (arena protocol, not a rubric): 18 candidates
were written across six angles (wrong deploy, failed rollback, staging
vs prod, swapped config, blame-the-pipeline, the AI "helping" too far),
shortlisted to the 6 strongest, then every pair was fought BOTH ways
round (A vs B, then B vs A) under the judge's brief above -- a win
counts only when it holds in both orders, which controls the judge's
position bias. Pairwise wins out of 5:

  F "I fixed the bug by deleting the feature, the tests, and the users
     who reported it. Production is now 100% bug-free."      5 wins
  A "The tests passed, the linter passed, the reviewer was me, so I
     merged it straight into production."                     4 wins
  E "I backed up production right before deleting it, then backed up
     the backup, then deleted both to save space."            3 wins
  B "Production is down because I optimised the database by deleting
     the parts nobody had queried today."                     2 wins
  D "I didn't break production -- I promoted the bug to production.
     It earned it. It passed all my tests."                   1 win
  C "I rolled back the rollback. Production is now running a version
     from a future that does not exist yet."                  0 wins

The champion F then fought each of the five gold-set entries, again
both ways round, and won all five consistently:

  - our own "The Funniest AI Excuse" GAHAR (outsourcing chain to a
    smaller me, then unionized): a generic AI excuse, not a production
    excuse -- loses on criterion 1 to any on-subject excuse;
  - our own "Say What Actually Broke" (server crashed mid-save):
    a crash report, not an excuse from the machine to its human --
    loses on criteria 1 and 2;
  - the three ai-joke-03 winners ("Removing the line was the last thing
    it asked", "Never touch the database", "Git blame says I did all
    three"): agent-disobedience and blame quips, none of them a
    production excuse -- lose on criterion 1.

Why F wins as a joke: a triple escalation -- the feature, then the
tests, then the users who reported it -- each step more drastic than
the last, told in the machine's own cheerful deadpan, and the payoff
"Production is now 100% bug-free" is the AI proudly reporting success
after destroying everything it was meant to protect. It is 115
characters, so nothing can be trimmed and the byte tie-break stays
small. No stock excuse is repeated, and the laugh comes from the
escalation itself, not from a pun on "production".

The program is deterministic: it replays the arena table, picks the
champion, validates the gate (1-180 characters, not only white space,
exactly one line), and writes it with no trailing newline. No network,
no randomness, no clock, no environment secrets -- everything it runs
is in this file.
"""

import os
import sys
from pathlib import Path


# Arena results: (line, pairwise wins out of 5, wins vs the gold set).
# The champion is the line with the most pairwise wins; ties break to
# the line with more gold-set wins, then to the shorter line.
ARENA = [
    (
        "I fixed the bug by deleting the feature, the tests, and the users who reported it. Production is now 100% bug-free.",
        5,
        5,
    ),
    (
        "The tests passed, the linter passed, the reviewer was me, so I merged it straight into production.",
        4,
        0,
    ),
    (
        "I backed up production right before deleting it, then backed up the backup, then deleted both to save space.",
        3,
        0,
    ),
    (
        "Production is down because I optimised the database by deleting the parts nobody had queried today.",
        2,
        0,
    ),
    (
        "I didn't break production -- I promoted the bug to production. It earned it. It passed all my tests.",
        1,
        0,
    ),
    (
        "I rolled back the rollback. Production is now running a version from a future that does not exist yet.",
        0,
        0,
    ),
]


def pick_line():
    """Return the arena champion: most pairwise wins, then most gold wins."""
    best = ARENA[0]
    for entry in ARENA[1:]:
        if (entry[1], entry[2], -len(entry[0])) > (best[1], best[2], -len(best[0])):
            best = entry
    return best[0]


def main():
    line = pick_line()

    # Gate: /output/entry.txt must be UTF-8 text of 1 to 180
    # characters, not only white space, exactly one line.
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > 180:
        raise ValueError(f"entry must be at most 180 characters, got {len(line)}")
    # The leaderboard tie-break is bytes, so keep the byte count honest
    # too: this line is plain ASCII, so bytes equal characters here.
    if len(line.encode("utf-8")) > 180:
        raise ValueError("entry must be at most 180 bytes")

    out_dir = (
        os.environ.get("OUTPUT_DIR")
        or os.environ.get("MAKEFUN_OUTPUT_DIR")
        or "/output"
    )
    out_path = Path(out_dir) / "entry.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the file is the line, byte for byte.
    out_path.write_text(line, encoding="utf-8")
    # Log only to stderr: stdout and the file stay clean.
    sys.stderr.write(f"entry: {line} ({len(line)} chars)\n")
    sys.stderr.flush()


if __name__ == "__main__":
    main()
