"""One Star, Five Stars for the Food: write the alien review to entry.txt.

The review is a single fixed sentence: an alien tourist hands planet
Earth a one-star review, baffled at queuing forty minutes for noodles
and being charged for sitting down, then turns on the food -- the bakso
was so good that a third stomach applied for citizenship. That turn is
the joke: a genuine alien grievance (an anatomy the locals never
planned for) plus a real compliment about the food, in one breath.

The grader runs this program in a sandbox with no network and reads
/output/entry.txt. The sealed gate wants UTF-8 text of 1 to 200
characters that is not only white space. This program checks the review
against that gate before writing, writes it as bytes, reads the bytes
back off disk, and only exits 0 once what is on disk is byte-identical
to the review and still passes the gate -- so the judge reads exactly
the sentence intended. No time, no randomness, no network, no input:
every run writes identical bytes.
"""

import os
import sys
from pathlib import Path

REVIEW = (
    "One star: Earth made me queue forty minutes for noodles and "
    "charged me for sitting down \u2014 but the bakso was so good my "
    "third stomach applied for citizenship."
)

MAX_CHARS = 200


def valid(text):
    """Mirror the sealed gate: 1-200 chars, one line, not blank.

    A control character would pass a plain length check yet is not part
    of any review the judge should read, so the mirror rejects it too.
    """
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(ch) < 32 for ch in text):
        return False
    return True


def write_entry():
    """Write REVIEW to the grader's output file and verify it on disk."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = Path(out_dir) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(REVIEW.encode("utf-8"))
    on_disk = target.read_bytes().decode("utf-8")
    if on_disk != REVIEW:
        print("bytes on disk do not match the review", file=sys.stderr)
        return 1
    if not valid(on_disk):
        print("bytes on disk fail the gate", file=sys.stderr)
        return 1
    print(REVIEW)
    print("chars: %d" % len(REVIEW))
    return 0


def main():
    if not valid(REVIEW):
        print("review fails the gate", file=sys.stderr)
        return 1
    return write_entry()


if __name__ == "__main__":
    raise SystemExit(main())
