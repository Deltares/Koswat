#!/usr/bin/env bash
poetry install
git config --global --add safe.directory "/usr/src/app"
git config --global core.autocrlf true