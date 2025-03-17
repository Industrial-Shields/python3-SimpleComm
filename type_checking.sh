#!/bin/bash
python -m mypy --pretty --config-file mypy.ini --ignore-missing-imports . && python -m pyright --pythonversion 3.11
