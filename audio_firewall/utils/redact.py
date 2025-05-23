import re

def redact_text(text, keywords):
    for kw in keywords:
        pattern = re.compile(rf"\\b{re.escape(kw)}\\b", re.IGNORECASE)
        text = pattern.sub("[REDACTED]", text)
    return text
