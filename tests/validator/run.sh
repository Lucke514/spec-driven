#!/usr/bin/env bash
# Runs scripts/validate.py against the fixtures here and checks exit codes.
#   valid-*    must exit 0 with no error lines
#   invalid-*  must exit 1 and print the message in the fixture's `expect` file
# The assets templates must parse (exit 0 or 1, no traceback); they need not pass.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
validate="$here/../../scripts/validate.py"
fail=0

check() { # name expected-exit expected-text target...
  local name="$1" want="$2" text="$3"; shift 3
  local out code
  out="$(python3 "$validate" "$@" 2>&1)"; code=$?
  if [ "$code" -ne "$want" ]; then
    echo "FAIL $name: exit $code, want $want"; echo "$out" | sed 's/^/  /'; fail=1; return
  fi
  if [ -n "$text" ] && ! grep -qF -- "$text" <<<"$out"; then
    echo "FAIL $name: output lacks '$text'"; echo "$out" | sed 's/^/  /'; fail=1; return
  fi
  if [ "$want" -eq 0 ] && grep -q ': error:' <<<"$out"; then
    echo "FAIL $name: error lines on a valid fixture"; fail=1; return
  fi
  echo "ok   $name"
}

for dir in "$here"/valid-*/; do
  check "$(basename "$dir")" 0 "" "$dir"
done
check "valid-small (file path)" 0 "" "$here/valid-small/spec.md"
for dir in "$here"/invalid-*/; do
  check "$(basename "$dir")" 1 "$(cat "$dir/expect")" "$dir"
done

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
assets="$here/../../assets"
cp "$assets/spec-template.md" "$tmp/spec.md"
cp "$assets/plan-template.md" "$tmp/plan.md"
cp "$assets/tasks-template.md" "$tmp/tasks.md"
out="$(python3 "$validate" "$tmp" 2>&1)"; code=$?
if [ "$code" -gt 1 ] || grep -q Traceback <<<"$out"; then
  echo "FAIL templates: exit $code"; echo "$out" | sed 's/^/  /'; fail=1
else
  echo "ok   templates parse"
fi

[ "$fail" -eq 0 ] && echo "all validator checks passed"
exit "$fail"
