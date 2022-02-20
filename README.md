## Anki Add-on Builder

<a title="License: GNU AGPLv3" href="https://github.com/glutanimate/anki-addon-builder/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a href="https://pypi.org/project/aab/"><img src="https://img.shields.io/pypi/v/aab.svg"></a>
<img src="https://img.shields.io/pypi/status/aab.svg">
<img src="https://img.shields.io/pypi/dd/aab.svg">


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

#### Installing the latest release

    pip install aab

#### Installing from the master branch

    pip install --upgrade git+https://github.com/glutanimate/anki-addon-builder.git

### Usage

You can get an overview of all supported actions by accessing the built-in help (options below reflect latest main branch state and might not be available in pypi builds, yet):

```
$ aab -h
usage: aab [-h] [-v] {build,ui,manifest,clean,create_dist,build_dist,package_dist} ...

positional arguments:
  {build,ui,manifest,clean,create_dist,build_dist,package_dist}
    build               Build and package add-on for distribution
    ui                  Compile add-on user interface files
    manifest            Generate manifest file from add-on properties in addon.json
    clean               Clean leftover build files
    create_dist         Prepare source tree distribution for building under build/dist. This is
                        intended to be used in build scripts and should be run before `build_dist`
                        and `package_dist`.
    build_dist          Build add-on files from prepared source tree under build/dist. This step
                        performs all source code post-processing handled by aab itself (e.g.
                        building the Qt UI and writing the add-on manifest). As with `create_dist`
                        and `package_dist`, this command is meant to be used in build scripts
                        where it can provide an avenue for performing additional processing ahead
                        of packaging the add-on.
    package_dist        Package pre-built distribution of add-on files under build/dist into a
                        distributable .ankiaddon package. This is inteded to be used in build
                        scripts and called after both `create_dist` and `build_dist` have been
                        run.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose output
```

Each subcommand also comes with its own help screen, e.g.:

```
$ aab build -h
usage: aab build [-h] [-t {qt6,qt5,all,anki21}] [-d {local,ankiweb,all}] [version]

positional arguments:
  version               Version to (pre-)build as a git reference (e.g. 'v1.2.0' or 'd338f6405').
                        Special keywords: 'dev' - working directory, 'current' – latest commit,
                        'release' – latest tag. Leave empty to build latest tag.

optional arguments:
  -h, --help            show this help message and exit
  -t {qt6,qt5,all,anki21}, --target {qt6,qt5,all,anki21}
                        Anki release type to build for. Use 'all' (deprecated alias: 'anki21') to
                        target both Qt5 and Qt6.
  -d {local,ankiweb,all}, --dist {local,ankiweb,all}
                        Distribution channel to build for

```

#### Examples

_Build latest tagged add-on release_

```
aab build -d local -t anki21 release
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

All of the metadata needed by `aab` to work correctly is stored in an `addon.json` file at the root of the project tree. For more information on its fields and their specifications please refer to the [schema file](https://github.com/glutanimate/anki-addon-builder/blob/master/aab/schema.json).

### License and Credits

*Anki Add-on Builder* is *Copyright © 2019 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

With code contributions by the following awesome people:

- [zjosua](https://github.com/zjosua)

Anki Add-on Builder is free and open-source software. Its source-code is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [license file](https://github.com/glutanimate/anki-addon-builder/blob/master/LICENSE) that accompanies this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. Please see the license file for more details.
