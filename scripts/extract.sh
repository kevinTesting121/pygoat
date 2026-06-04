#!/usr/bin/env bash
# Reads input and operates on the requested files.
set -e

read -r BUNDLE
read -r NOTES

tar -xzf "$BUNDLE"
cat -n "$NOTES"
