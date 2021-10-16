# Anki Add-on Builder

<a title="License: GNU AGPLv3" href="https://github.com/glutanimate/anki-addon-builder/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a href="https://pypi.org/project/aab/"><img src="https://img.shields.io/pypi/v/aab.svg"></a>
<img src="https://img.shields.io/pypi/status/aab.svg">
<img src="https://img.shields.io/pypi/dd/aab.svg">


An opinionated development tool for building and packaging Anki add-ons. Used in most of my major Anki add-on projects.

- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Usage](#usage)
- [Specifications](#specifications)
- [Contributing](#contributing)
- [License and Credits](#license-and-credits)

## Disclaimer

### Project State

**Important**: Parts of the project are currently undergoing a major restructuring. As a result, some of the documentation below might no longer be up-to-date for `main`. For use in production, make sure to install a tagged release and not from source.


### Platform Support

`aab` has only only been confirmed to work on macOS and Linux so far.

## Installation

### Requirements

`aab` requires Python 3.8+.

### Installing the latest packaged build

#### Without Qt Designer support:

```bash
$ pip install aab
```

or

```bash
$ poetry add --dev aab
```

#### With Qt Designer support:

You will need to have `PyQt` installed for `aab` to compile and manage Qt designer forms. By default `aab` will use whatever `PyQt` version is available in the environment it runs in. Should you not have `PyQt` installed, then you can install it alongside `aab` using:


```bash
$ pip install aab[qt5,qt6]
```

or

```bash
$ poetry add --dev aab --extras "qt5 qt6"
```

This will install both `PyQt5` and `PyQt6`.

Depending on the Anki builds you are targeting, you might only need to have one PyQt version installed (`PyQt5` on Anki ≈2.1.50 and lower, `PyQt6` on more recent versions). If both `Qt` versions are installed, `aab` will simultaneously compile `PyQt5` and `PyQt6` forms, wrapping them in a version-agnostic shim. Add-on builds created in that manner will work on a wider range of Anki releases.

## Usage

You can get an overview of all supported actions by accessing the built-in help:

```
$ aab -h
usage: aab [-h] [-v] {build,ui,clean} ...

positional arguments:
    {build,ui,clean}
    build           Build and package add-on for distribution
    ui              Compile add-on user interface files
    clean           Clean leftover build files

optional arguments:
    -h, --help        show this help message and exit
    -v, --verbose     Enable verbose output
```

Each subcommand also comes with its own help screen, e.g.:

```
$ aab build -h
usage: aab build [-h] [-t {anki21,anki20,all}] [-d {local,ankiweb,all}]
                 [-c | -w | -r]
                 [version]

positional arguments:
  version               Version to build as a git reference (e.g. 'v1.2.0' or
                        'd338f6405'). Special instructions can be given with
                        the mutually exclusive '-c', '-w' or '-r' options.
                        Leave empty to build latest tag ('-r').

optional arguments:
  -h, --help            show this help message and exit
  -t {anki21,anki20,all}, --target {anki21,anki20,all}
                        Anki version to build for
  -d {local,ankiweb,all}, --dist {local,ankiweb,all}
                        Distribution channel to build for
  -c, --current-commit  Build the currently checked out commit.
  -w, --working-directory
                        Build the current working directory without the need
                        of a commit. Useful for development.
  -r, --release         Build the latest tag.
```

### Examples

_Build latest tagged add-on release_

```
aab build -d local -t anki21 --release
```

or simply

```
aab build
```

The output artifacts will be, by default, written into `./build/`.

_Compile Qt UI forms and resources for Anki 2.1_

```bash
aab ui -t anki21
```

## Specifications

### Project Structure

In order for `aab` to work correctly, your project should generally follow the directory structure below:

```
project root
├── src [required] (contains add-on package and Anki 2.0 entry-point)
│   ├── {module_name} [required] (add-on package)
│   │   └── locale [optionial] (directory containg '.po' files for localization)
|   └── {display_name}.py [optional] (Anki 2.0 entry-point)
└── addon.json [required] (contains add-on meta information read by aab)
```

For a more detailed look at the entire directory tree please feel free to take a look at some of the [add-ons I've published recently](https://github.com/topics/anki-addon?o=desc&q=user%3Aglutanimate&s=updated).

### `addon.json` File

All of the metadata needed by `aab` to work correctly is stored in an `addon.json` file at the root of the project tree. For more information on its fields and their specifications please refer to the [schema file](https://github.com/glutanimate/anki-addon-builder/blob/master/aab/schema.json).

### Localization

`aab` tries to automatically compile `.po` files found in the `locale` directory to `.mo` files for the build. File extensions are case sensitive.  The program `msgfmt` is used for compilation. It must be installed for this feature to work.

## Contributing

Contributions are welcome! To set up `anki-addon-builder` for development, please first make sure you have Python 3.8+ and [poetry](https://python-poetry.org/docs/) installed, then run the following steps:

```
$ git clone https://github.com/glutanimate/anki-addon-builder.git

$ cd anki-addon-builder

# Either set up a new Python virtual environment at this stage
# (e.g. using pyenv), or let poetry create the venv for you

$ make install
```

Before submitting any changes, please make sure that `anki-addon-builder`'s checks and tests pass:

```bash
make check
make lint
make test
```

This project uses `black`, `isort` and `autoflake` to enforce a consistent code style. To auto-format your code you can use:

```bash
make format
```

## License and Credits

*Anki Add-on Builder* is *Copyright © 2019-2021 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)* and [contributors](./CONTRIBUTORS).

*Anki Add-on Builder* is free and open-source software. Its source-code is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [license file](https://github.com/glutanimate/anki-addon-builder/blob/master/LICENSE) that accompanies this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. Please see the license file for more details.
