# Extended Anki Add-on Manifest Schema

```txt
https://github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json
```

Anki's add-on manifest schema, extended by a number of keys custom to aab


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [manifest.schema.json](../../aab/schemas/manifest.schema.json "open original schema") |

## Extended Anki Add-on Manifest Type

`object` ([Extended Anki Add-on Manifest](manifest.md))

# Extended Anki Add-on Manifest Properties

| Property                                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                        |
| :-------------------------------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [package](#package)                     | `string` | Required | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-package.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/package")                     |
| [name](#name)                           | `string` | Required | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/name")                           |
| [mod](#mod)                             | `number` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-mod.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/mod")                             |
| [conflicts](#conflicts)                 | `array`  | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-conflicting-add-ons.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/conflicts")       |
| [min_point_version](#min_point_version) | `number` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-min_point_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/min_point_version") |
| [max_point_version](#max_point_version) | `number` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-max_point_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/max_point_version") |
| [branch_index](#branch_index)           | `number` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-branch_index.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/branch_index")           |
| [human_version](#human_version)         | `string` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-human_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/human_version")         |
| [version](#version)                     | `string` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/version")                     |
| [ankiweb_id](#ankiweb_id)               | `string` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-ankiweb_id.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/ankiweb_id")               |
| [author](#author)                       | `string` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-author.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/author")                       |
| [homepage](#homepage)                   | `string` | Optional | cannot be null | [Extended Anki Add-on Manifest](manifest-properties-homepage.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/homepage")                   |

## package

The module/package the add-on is imported as, i.e. the name of the add-on folder.


`package`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-package.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/package")

### package Type

`string`

## name

The name displayed in Anki's UI (e.g. in the add-on list)


`name`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-name.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/name")

### name Type

`string`

## mod

The time the add-on was last modified (unix epoch)


`mod`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-mod.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/mod")

### mod Type

`number`

## conflicts

A list of other packages that conflict


`conflicts`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-conflicting-add-ons.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/conflicts")

### conflicts Type

`string[]`

## min_point_version

the minimum 2.1.x version this add-on supports


`min_point_version`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-min_point_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/min_point_version")

### min_point_version Type

`number`

## max_point_version

If negative, abs(n) is the maximum 2.1.x version this add-on supports. If positive, indicates version tested on, and is ignored


`max_point_version`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-max_point_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/max_point_version")

### max_point_version Type

`number`

## branch_index

AnkiWeb sends this to indicate which branch the user downloaded


`branch_index`

-   is optional
-   Type: `number`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-branch_index.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/branch_index")

### branch_index Type

`number`

## human_version

Human-readable version string set by the add-on creator


`human_version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-human_version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/human_version")

### human_version Type

`string`

## version

[aab] Version string, set to the same value as human_version


`version`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-version.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/version")

### version Type

`string`

## ankiweb_id

[aab] The AnkiWeb upload ID.


`ankiweb_id`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-ankiweb_id.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/ankiweb_id")

### ankiweb_id Type

`string`

## author

[aab] The main author/maintainer/publisher of the add-on.


`author`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-author.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/author")

### author Type

`string`

## homepage

[aab] Homepage of the add-on project (e.g. GitHub repository link)


`homepage`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [Extended Anki Add-on Manifest](manifest-properties-homepage.md "https&#x3A;//github.com/glutanimate/anki-addon-builder/aab/schemas/manifest.schema.json#/properties/homepage")

### homepage Type

`string`
