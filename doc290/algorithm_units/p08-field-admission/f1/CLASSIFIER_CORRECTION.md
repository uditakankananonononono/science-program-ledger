# Reviewer-requested pointer-classifier correction

Unpublished9349bf9 held for pointer recognizer using Unicode splitlines. It admitted
VT/FF/U+2028/NEL record separators incorrectly. Replaced pointer recognition with
explicit ASCII bytes/LF-only grammar,final LF required,canonical decimal size and
lowercase64hex hash. CRLF deliberately unresolved,not silently normalized. Raw-line
coordinate inventory still uses labeled Unicode splitlines. Added each separator
control plus CRLF. No selected source contents fetched,code execution or LFS access.
This is reviewer-requested code/test/freeze/hash change before corrected review;
not result repair or changed selection. Prior broken classifier retained in history.
