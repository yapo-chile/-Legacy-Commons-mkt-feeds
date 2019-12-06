#!/usr/bin/env bash

MYPY_THRESHOLD=5
MYPY_CURRENT=$(mypy app/app.py | tee /dev/tty | wc -l)

echo "Warn: $(($MYPY_CURRENT-1)) mypy issues"
if [[ $MYPY_CURRENT -gt $MYPY_THRESHOLD ]]; then
  echo "Mypy issues exceeded the threshold: $MYPY_CURRENT > $MYPY_THRESHOLD"
  exit 1
fi

pylint -f json -r n app/app.py | scripts/commands/./pylint-to-checkstyle.py > reports/checkstyle-report.xml