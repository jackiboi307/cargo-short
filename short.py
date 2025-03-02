import json

RED     = '\033[91m'
YELLOW  = '\033[93m'
GREEN   = '\033[92m'
BLUE    = '\033[94m'
BOLD    = '\033[1m'
RESET   = '\033[0m'

UNDERCURL = "\033[58:5:1m\033[4:3m"

def insert(text, new, index):
    return text[:index] + new + text[index:]

def construct(
        _, /,
            level,
            message,
            file_name,
            label,
            text,
            highlight,
            lines,
            children
        ):

    # Insert help:
    for child in children:
        if child["level"] == "help":
            if len(child["spans"]) == 0:
                continue
            replacement = child["spans"][0]["suggested_replacement"]
            if replacement == "":
                continue
            text = insert(
                    text,
                    GREEN + BOLD + replacement + RESET,
                    child["spans"][0]["column_start"]-1)
            break

    highlight = list(highlight)
    highlight[0] -= 1
    highlight[1] -= 1

    # Add undercurl:
    length = len(text)
    # text = text[:highlight[0]] + UNDERCURL + text[highlight[0]:]
    text = insert(text, UNDERCURL, highlight[0])
    difference = len(text) - length
    highlight[1] += difference
    # text = text[:highlight[1]] + RESET + text[highlight[1]:]
    text = insert(text, RESET, highlight[1])

    # Remove whitespace to the left:
    text = text.strip()

    lines = str(lines[0]) if lines[1] == lines[0] else \
            f"{lines[0]} -> {lines[1]}"

    col = RED if level == "error" else YELLOW if level == "warning" else ""
    
    label = f": {label}" if label is not None else ""

    return f"{GREEN}{file_name}{RESET}: {BLUE+BOLD}{lines}{RESET}: " + \
           f"{col}{message}{RESET}" + \
           f"{label}\n\t{text}\n\n"

# Read the piped content:
if 1:
    lines = []
    while True:
        try:
            lines.append(json.loads(input()))
            if lines[-1]["reason"] == "build-finished":
                break

        except EOFError:
            break

# Debugging purposes:
else:
    lines = []
    with open("output.json") as file:
        for line in file.read().splitlines():
            lines.append(json.loads(line))

output = "\n"

for msg in lines:
    # Ignore everything except compiler-message
    # TODO: Add other stuff because it is probably useful

    if msg["reason"] == "compiler-message":
        msg = msg["message"]

        output += construct(None, # I added this None because of Python limitations

            level=msg["level"],
            message=msg["message"],

            # The stuff below does weird indexing to msg["spans"],
            # it assumes the length is 1 because I don't know what to do if it isn't
            # The same applies for msg["spans"][...]["text"]

            file_name=msg["spans"][0]["file_name"],
            label=msg["spans"][0]["label"],
            text=msg["spans"][0]["text"][0]["text"],
            highlight=(
                msg["spans"][0]["text"][0]["highlight_start"],
                msg["spans"][0]["text"][0]["highlight_end"]
            ),
            lines=(
                msg["spans"][0]["line_start"],
                msg["spans"][0]["line_end"]
            ),
            children = msg["children"]
        )

output = output.rstrip() # Remove last newline

print(output)
