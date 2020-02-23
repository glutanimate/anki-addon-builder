# Anki Add-on Builder Add-on Specification Schema

```txt
https://github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json
```

JSON schema for the addon.json configuration files used by Anki Add-on Builder


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [addon.schema.json](../../aab/schemas/addon.schema.json "open original schema") |

## Anki Add-on Builder Add-on Specification Type

`object` ([Anki Add-on Builder Add-on Specification](addon.md))

# Anki Add-on Builder Add-on Specification Properties

| Property                                    | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                 |
| :------------------------------------------ | -------- | -------- | -------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [display_name](#display_name)               | `string` | Required | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-display_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/display_name")               |
| [module_name](#module_name)                 | `string` | Required | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-module_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/module_name")                 |
| [repo_name](#repo_name)                     | `string` | Required | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-repo_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/repo_name")                     |
| [local_name_suffix](#local_name_suffix)     | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-local_name_suffix.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/local_name_suffix")     |
| [ankiweb_id](#ankiweb_id)                   | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-ankiweb_id.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/ankiweb_id")                   |
| [version](#version)                         | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/version")                         |
| [author](#author)                           | `string` | Required | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-author.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/author")                           |
| [contact](#contact)                         | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-contact.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/contact")                         |
| [homepage](#homepage)                       | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-homepage.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/homepage")                       |
| [tags](#tags)                               | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-tags.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/tags")                               |
| [copyright_start](#copyright_start)         | `number` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-copyright_start.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/copyright_start")         |
| [conflicts](#conflicts)                     | `array`  | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-conflicting-add-ons.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/conflicts")           |
| [min_anki_version](#min_anki_version)       | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-min_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/min_anki_version")       |
| [max_anki_version](#max_anki_version)       | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-max_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/max_anki_version")       |
| [tested_anki_version](#tested_anki_version) | `string` | Optional | cannot be null | [Anki Add-on Builder Add-on Specification](addon-properties-tested_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/tested_anki_version") |

## display_name

The name displayed in Anki's UI (e.g. in the add-on list)


`display_name`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-display_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/display_name")

### display_name Type

`string`

## module_name

The module/package the add-on is imported as, i.e. the name of the add-on folder.


`module_name`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-module_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/module_name")

### module_name Type

`string`

## repo_name

The name of the git repository the add-on is hosted in. Currently only used for build names.


`repo_name`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-repo_name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/repo_name")

### repo_name Type

`string`

## local_name_suffix

A suffix to the display name to apply when creating builds for non-ankiweb distribution.


`local_name_suffix`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-local_name_suffix.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/local_name_suffix")

### local_name_suffix Type

`string`

## ankiweb_id

The AnkiWeb upload ID.


`ankiweb_id`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-ankiweb_id.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/ankiweb_id")

### ankiweb_id Type

`string`

## version

Add-on version string. Needs to follow semantic versioning guidelines.


`version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/version")

### version Type

`string`

## author

The main author/maintainer/publisher of the add-on.


`author`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-author.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/author")

### author Type

`string`

## contact

Contact details to list for the author (e.g. either a website or email)


`contact`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-contact.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/contact")

### contact Type

`string`

## homepage

Homepage of the add-on project (e.g. GitHub repository link)


`homepage`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-homepage.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/homepage")

### homepage Type

`string`

## tags

Space-delimited list of tags that characterize the add-on on AnkiWeb.


`tags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-tags.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/tags")

### tags Type

`string`

## copyright_start

Starting year to list for automatically generated copyright headers.


`copyright_start`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-copyright_start.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/copyright_start")

### copyright_start Type

`number`

## conflicts

A list of other AnkiWeb add-on IDs or package names that conflict with this add-on.


`conflicts`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-conflicting-add-ons.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/conflicts")

### conflicts Type

`string[]`

## min_anki_version

SemVer version string describing the minimum required Anki version to run this add-on.


`min_anki_version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-min_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/min_anki_version")

### min_anki_version Type

`string`

## max_anki_version

SemVer version string describing the maximum supported Anki version of this add-on


`max_anki_version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-max_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/max_anki_version")

### max_anki_version Type

`string`

## tested_anki_version

SemVer version string describing the latest Anki version this add-on was tested on.


`tested_anki_version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Anki Add-on Builder Add-on Specification](addon-properties-tested_anki_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/addon.schema.json#/properties/tested_anki_version")

### tested_anki_version Type

`string`
