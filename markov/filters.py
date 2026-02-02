from typing import Optional
import re

def should_learn(text: str) -> bool:
    if len(text) < 5:
        return False
    if text.startswith(("!", "/")):
        return False
    if re.fullmatch(r"[^\w]+", text):
        return False
    return True


def sanitize_output(text: str) -> Optional[str]:
    if "@everyone" in text or "@here" in text:
        return None
    return text