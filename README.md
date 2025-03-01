# cargo-short

Shorter output for cargo, to be used with the `check` or `build` command.

## Usage

`cargo check --message-format json-diagnostic-short | python short.py`

(making an alias is recommended)

Using it with the `run` command is possible too, but piping is going to consume the output and printing / reading is going to fail, so I don't recommend it.

## Screenshot

<img src="https://raw.githubusercontent.com/jackiboi307/cargo-short/refs/heads/main/screenshot.png">

## Features and lacking features

Currently, you only get warnings and errors - sooner or later I'll add the other stuff.

The output includes file names, line numbers, the message and label, as well as a code snippet with highlighting using a red undercurl.

You might get a limited output if the "span" is longer than 1, I don't know what that is though.

Because of very limited testing, errors are likely, and there is no error handling. I'll make sure to add that, but please report any errors!
