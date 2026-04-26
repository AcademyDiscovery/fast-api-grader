#!/usr/bin/env bash

set -e
set -x

pytest -n auto --dist loadgroup tests/ "${@}"
