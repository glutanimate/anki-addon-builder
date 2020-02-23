#!/bin/bash
#
# Generates markdown-formatted documentation from JSON schema files
#
# Requires jsonschema2md (https://github.com/adobe/jsonschema2md)

jsonschema2md -d aab/schemas/ -o docs/schemas -x -
