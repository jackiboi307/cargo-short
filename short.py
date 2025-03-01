import json

RED     = '\033[91m'
YELLOW  = '\033[93m'
GREEN   = '\033[92m'
BLUE    = '\033[94m'
BOLD    = '\033[1m'
RESET   = '\033[0m'

UNDERCURL = "\033[58:5:1m\033[4:3m"

def construct(
        _, /,
            level,
            message,
            file_name,
            label,
            text,
            highlight,
            lines
        ):

    # The weird stuff below is for formatting the code snippet
    
    # Remove whitespace to the left, and adjust highlight accordingly:
    length = len(text)
    text = text.lstrip()
    difference = length - len(text) + 1
    # I don't know why the above +1 is necessary,
    # but this seems to be working
    highlight = list(highlight)
    highlight[0] -= difference
    highlight[1] -= difference

    # Add undercurl:
    length = len(text)
    text = text[:highlight[0]] + UNDERCURL + text[highlight[0]:]
    difference = len(text) - length
    highlight[1] += difference
    text = text[:highlight[1]] + RESET + text[highlight[1]:]

    text = text.rstrip()

    lines = str(lines[0]) if lines[1] == lines[0] else \
            f"{lines[0]} -> {lines[1]}"

    col = RED if level == "error" else YELLOW if level == "warning" else ""

    return f"{GREEN}{file_name}{RESET}:{BLUE+BOLD}{lines}{RESET}: " + \
           f"{col}{message}{RESET}: " + \
           f"{label}\n\t{text}\n\n"

# Read the piped content:
if 1:
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break

# Debugging purposes:
else:
    with open("output.json") as file:
        lines = file.read().splitlines()

output = ""

for line in lines:
    msg = json.loads(line)

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
            )
        )

output = output.rstrip() # Remove last newline

print(output)
