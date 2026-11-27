#!/bin/sh
# Get the screenshots and logs (artifacts smoke-<platform>) of the latest Release smoke test run.
# Usage (in the repo, gh logged in): tools/smoke-fetch.sh [folder] [run-id]   Default folder: smoke-<run-id>
set -e
run=${2:-$(gh run list --workflow release-smoke.yml --limit 1 --json databaseId -q '.[0].databaseId')}
gh run view "$run" --json conclusion,url -q '"Run: " + .url + " (" + .conclusion + ")"'
gh run download "$run" --pattern 'smoke-*' --dir "${1:-smoke-$run}"
echo "Files: ${1:-smoke-$run}/"
