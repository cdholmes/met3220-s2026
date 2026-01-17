
#!/usr/bin/env python3
"""
String Indexing Quiz
- Randomized questions on positive/negative indexing and slicing.
- Immediate feedback with explanations.
- No external libraries needed.
"""

import random
import textwrap

# You can add or remove sample strings here.
SAMPLES = [
    "python",
    "indexing",
    "hello world",
    "data science",
    "Florida",
    "university",
    "banana",
    "abcde",
    "0123456789"
]

def explain_slice(s, start, stop, step=None):
    """Return a human-readable explanation of s[start:stop:step]."""
    base = f"s[{'' if start is None else start}:{'' if stop is None else stop}"
    if step is not None:
        base += f":{step}"
    base += "]"
    # Build actual slice
    result = s[slice(start, stop, step)]
    return base, result

def format_literal(val):
    """Format expected answers consistently for comparison and display."""
    if isinstance(val, str):
        return val
    elif isinstance(val, Exception):
        return val.__class__.__name__
    else:
        return str(val)

def normalize_user(text):
    """Normalize user input for comparison (trim only)."""
    return text.strip()

def ask(prompt, expected, explanation):
    """Ask a single question and return (correct: bool)."""
    print()
    print(textwrap.fill(prompt, width=80))
    user = input("\nYour answer: ")
    user_norm = normalize_user(user)
    expected_norm = format_literal(expected)

    correct = (user_norm == expected_norm)
    if correct:
        print("✅ Correct!")
    else:
        print(f"❌ Not quite. Expected: {repr(expected_norm)}")
    print(f"ℹ️  {explanation}")
    return correct

def question_char_at(s):
    """Question about direct indexing s[i]."""
    n = len(s)
    # choose index sometimes out of range or negative
    choice = random.choice([
        random.randrange(-n, n),           # valid range
        random.choice([n, -n-1, n+3])      # invalid indices
    ])
    prompt = f"For s = {repr(s)}, what is s[{choice}] ?"
    try:
        expected = s[choice]
        explanation = f"Zero-based indexing; negative indices count from the end. s[{choice}] = {repr(expected)}."
    except IndexError:
        expected = IndexError("out of range")
        explanation = "Direct indexing requires a valid position; out-of-range raises IndexError."
    return prompt, expected, explanation

def question_slice_basic(s):
    """Question about basic slice s[a:b]."""
    n = len(s)
    a = random.choice([None, random.randrange(-n-1, n+1)])
    b = random.choice([None, random.randrange(-n-1, n+1)])
    base, result = explain_slice(s, a, b)
    prompt = f"For s = {repr(s)}, what is {base} ?"
    explanation = f"Slicing does not raise on out-of-range; it returns empty string. Result: {repr(result)}."
    return prompt, result, explanation

def question_slice_step(s):
    """Question about stepped slice s[a:b:c]."""
    n = len(s)
    step = 0
    # ensure step != 0
    while step == 0:
        step = random.choice([-3, -2, -1, 1, 2, 3])
    a = random.choice([None, random.randrange(-n-1, n+1)])
    b = random.choice([None, random.randrange(-n-1, n+1)])
    base, result = explain_slice(s, a, b, step)
    prompt = f"For s = {repr(s)}, what is {base} ?"
    explanation = (
        f"Step controls direction/stride. With step={step}, start/stop are interpreted accordingly. "
        f"Slices are safe and clamp to bounds. Result: {repr(result)}."
    )
    return prompt, result, explanation

def question_reverse(s):
    """Classic reverse slice."""
    prompt = f"For s = {repr(s)}, what is s[::-1] ?"
    expected = s[::-1]
    explanation = "s[::-1] reverses the string (start/stop omitted, step = -1)."
    return prompt, expected, explanation

def question_len_vs_indexerror(s):
    """Clarify len vs indexing error."""
    n = len(s)
    idx = n  # always out of range for 0-based indexing
    prompt = f"For s = {repr(s)} (len={n}), what happens with s[{idx}] ?"
    expected = IndexError("out of range")
    explanation = (
        f"Valid indices are 0..{n-1} and -1..{-n}. Using index {idx} is out-of-range and raises IndexError."
    )
    return prompt, expected, explanation

def question_empty_slice(s):
    """Show when slices yield empty string."""
    # Construct a scenario likely to be empty (incompatible direction)
    n = len(s)
    a = random.choice([random.randrange(-n+1, n+1)])
    if a<0:
        b = random.choice([random.randrange(-n,a)])
    else:
        b = random.choice([random.randrange(0, a)])
    prompt = f"For s = {repr(s)}, what is s[{a}:{b}] ?"
    expected = s[a:b]
    explanation = "With default step=1, start > stop gives ''. Slices never raise IndexError."
    return prompt, expected, explanation

def question_empty_slice_orig(s):
    """Show when slices yield empty string."""
    # Construct a scenario likely to be empty (incompatible direction)
    prompt = f"For s = {repr(s)}, what is s[3:1] ?"
    expected = s[3:1]
    explanation = "With default step=1, start > stop gives ''. Slices never raise IndexError."
    return prompt, expected, explanation

    
def question_first_last(s):
    """Ask for first and last characters."""
    prompt = f"For s = {repr(s)}, what is s[0] + s[-1] ? (concatenate the two characters)"
    expected = s[0] + s[-1]
    explanation = "s[0] is first char; s[-1] is last char. Concatenating gives the two-character string."
    return prompt, expected, explanation

def question_slice_omit_bounds(s):
    """Ask about omitted bounds."""
    which = random.choice(["start", "stop"])
    n = len(s)
    if which == "start":
        a = random.choice([random.randrange(0, n+1)])
        prompt = f"For s = {repr(s)}, what is s[:{a}] ?"
        expected = s[:a]
        explanation = "Omitting start defaults to the beginning."
    else:
        a = random.choice([random.randrange(-n, n+1)])
        prompt = f"For s = {repr(s)}, what is s[{a}:] ?"
        expected = s[a:]
        explanation = "Omitting stop goes to the end."
    return prompt, expected, explanation

def build_question_bank():
    """Return a list of callables that generate (prompt, expected, explanation)."""
    return [
        question_char_at,
        question_slice_basic,
        question_slice_step,
        question_reverse,
        question_len_vs_indexerror,
        question_empty_slice,
        question_first_last,
        question_slice_omit_bounds,
    ]

def runtest():
    print("=== String Indexing Quiz ===")
    print("Answer exactly as Python would produce (e.g., hello, '', IndexError).")
    print("Tip: For strings, type them without extra quotes; empty string is just nothing between quotes: ''")
    print()

    questions = build_question_bank()
    total = 10  # number of questions per run
    score = 0

    for i in range(1, total + 1):
        s = random.choice(SAMPLES)
        qgen = random.choice(questions)
        prompt, expected, explanation = qgen(s)
        print(f"\nQuestion {i}/{total}")
        correct = ask(prompt, expected, explanation)
        score += int(correct)

    print("\n=== Results ===")
    print(f"Score: {score} / {total}")
    if score == total:
        print("Perfect! You’ve got string indexing down.")
    elif score >= int(0.7 * total):
        print("Solid work—review the explanations you missed to tighten up details.")
    else:
        print("Recommend a quick refresher on zero-based indexing, negatives, and slicing semantics.")

    print("\nKey reminders:")
    print("- Strings are zero-based: s[0] is the first character.")
    print("- Negative indices count from the end: s[-1] is the last character.")
    print("- Slices never raise IndexError; they clamp to bounds and can be empty.")
    print("- Direct indexing out-of-range raises IndexError.")
    print("- s[::-1] reverses the string.")

if __name__ == "__main__":
    runtest()
