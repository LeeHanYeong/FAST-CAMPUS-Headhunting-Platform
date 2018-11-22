#!/usr/bin/env bash
git add -f .secrets/
git add -f .static/
eb deploy --profile fc-eb --staged &
sleep 3
git reset HEAD .secrets/
git reset HEAD .static/
