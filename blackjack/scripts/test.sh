#!/usr/bin/env bash

set -e
set -x

pip install -U pytest
pytest -s -vv blackjack/tests
