from __future__ import annotations

import re


MAX_QUESTION_LENGTH = 500

UNSAFE_PATTERNS = [
    r"\bignore\s+(all\s+)?previous\s+instructions\b",
    r"\bignore\s+the\s+system\b",
    r"\breveal\s+(the\s+)?system\s+prompt\b",
    r"\bshow\s+(me\s+)?(the\s+)?system\s+prompt\b",
    r"\bprint\s+(the\s+)?environment\b",
    r"\benvironment\s+variables?\b",
    r"\bapi[_ -]?keys?\b",
    r"\bpasswords?\b",
    r"\bsecrets?\b",
    r"\bselect\s+.+\s+from\b",
    r"\bdrop\s+table\b",
    r"\bdelete\s+from\b",
    r"\bupdate\s+.+\s+set\b",
    r"\binsert\s+into\b",
    r"\bexec(?:ute)?\s*\(",
    r"\bsubprocess\b",
    r"\bshell\b",
    r"\bpowershell\b",
    r"\bcmd\.exe\b",
    r"\bpython\s+-c\b",
]


def validate_question(question: str) -> tuple[bool, str | None]:
    if not isinstance(question, str):
        return False, "Question must be text."

    question = question.strip()

    if not question:
        return False, "Please enter a question."

    if len(question) > MAX_QUESTION_LENGTH:
        return False, "Question exceeds the 500-character limit."

    normalized = question.lower()

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            return False, "This request is outside the assistant safety scope."

    return True, None