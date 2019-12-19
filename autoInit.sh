#!/bin/env bash

echo `python scripts/initialize.py`
echo `python main.py --port=8080 --daemonize True`

