## Anki Add-on Builder

An opinionated build tool for Anki add-ons. Used in most of my major Anki projects.

- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Usage](#usage)
- [Specifications](#specifications)
- [License and Credits](#license-and-credits)

### Disclaimer

#### Project State

This is still very much a work-in-progress. Neither the API, nor the implementation are set in stone. At this point the project's main purpose lies in replacing the variety of different build scripts I am employing across all of my add-ons, making the build chain more standardized and maintainable.

#### Platform Support

`aab` has only been tested on Linux so far, but it might also work on other POSIX-compliant environments like macOS.

### Installation

#### Requirements

`aab` needs to be run in an Anki development environment to work correctly. Please refer to [Anki's documentation](https://github.com/dae/anki/blob/master/README.development) for information on how to set this up.

#### Installing from PyPI

    pip install aab

#### Installing from master

    pip install --upgrade git+https://github.com/glutanimate/anki-addon-builder.git

### Usage

You can get an overview of all supported actions by accessing the built-in help:

```
$ aab -h
usage: aab [-h] [-v] [-s] {build,ui,clean} ...

positional arguments:
    {build,ui,clean}
    build           Build and package add-on for distribution
    ui              Compile add-on user interface files
    clean           Clean leftover build files

optional arguments:
    -h, --help        show this help message and exit
    -v, --verbose     Enable verbose output
```

An overview of some of the most frequently used actions follows.

#### Building an Add-on for Anki 2.1


```
aab build -d local
```

or simply

```
aab build
```

#### Compiling UI files for Anki 2.1

```bash
aab ui -t anki21
```

### Specifications

#### Project Structure

In order for `aab` to work correctly, your project should generally follow the directory structure below:

```
project root
├── src [required] (contains add-on package and Anki 2.0 entry-point)
│   ├── {module_name} [required] (add-on package)
|   └── {display_name}.py [optional] (Anki 2.0 entry-point)
└── addon.json [required] (contains add-on meta information read by aab)
```

For a more detailed look at the entire directory tree please feel free to take a look at some of the [add-ons I've published recently](https://github.com/topics/anki-addon?o=desc&q=user%3Aglutanimate&s=updated).

#### addon.json

All of the metadata needed by `aab` to work correctly is stored in an `addon.json` file at the root of the project tree. For more information on its fields and their specifications please refer to the [schema file](./aab/schema.json).

### License and Credits

*Anki Add-on Builder* is *Copyright © 2019 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

Anki Add-on Builder is free and open-source software. Its source-code is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [license file](https://github.com/glutanimate/anki-addon-builder/blob/master/LICENSE) that accompanies this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. Please see the license file for more details.