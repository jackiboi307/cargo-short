# cargo-short

Shorter output for cargo, to be used with the `check` or `build` command.

## Usage

`cargo check --message-format json | python short.py`

(making an alias is recommended)

Using it with the `run` command is possible too, but piping is going to consume the output and printing / reading is going to fail, so I don't recommend it.

## Screenshot

<img src="https://raw.githubusercontent.com/jackiboi307/cargo-short/refs/heads/main/screenshot.png">

## Features and lacking features

Currently, you only get warnings and errors - sooner or later I'll add the other stuff.

The output includes file names, line numbers, the message and label, and a code snippet. ~~The code snippet includes highlighting using a red undercurl, and if there is any compiler suggestion it is included in bold green.~~ Update: suggestions and the red undercurl were removed as they sometimes did not work well.

Because of limited testing, errors are likely, and there is no error handling. I'll make sure to add that, but please report any errors!
