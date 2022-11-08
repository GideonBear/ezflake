import re
import subprocess
from logging import getLogger

from pytest import mark
from pathlib import Path
from typing import Callable, List, Union

from ezflake.violation import Violation, ViolationType


logger = getLogger(__name__)

SPLIT_SYMBOL = '&'
FORMAT = '%(path)s&%(row)d&%(col)d&%(code)s&%(text)s'
EXPECTED_VIOLATION_REGEX = re.compile(
    r'# ([1-9]+): (.+): (.+)$'
)


def generate_tests(testdir: Path) -> Callable[..., None]:
    files = testdir.iterdir()

    @mark.parametrize('file', files)
    def test_wrapper(file: Path) -> None:
        text = file.read_text()
        expected_violations = get_expected_violations(text)
        violations = run_flake8(file, file.with_suffix('').name)

        logger.info(f'Comparing {violations} and {expected_violations}')
        assert violations == expected_violations, \
            f'Expected violations:\n{expected_violations}\nGot violations:\n{violations}'

    return test_wrapper


def run_flake8(file: Path, select: str) -> List[Violation]:
    text = run_flake8_text(file, select, FORMAT)
    lines = text.split('\n')
    violations = []
    for line in lines:
        if line == '':
            continue
        elif line.count(SPLIT_SYMBOL) < 4:
            raise ValueError('Wrong format', line)
        path, lineno, col, code, text = line.split(SPLIT_SYMBOL, maxsplit=4)
        violation_type = ViolationType(code, text)
        violation = Violation(violation_type, int(lineno), int(col))
        violations.append(violation)
    return violations


def get_expected_violations(text: str) -> List[Violation]:
    lines = text.split('\n')
    violations = []
    for lineno, line in enumerate(lines):
        match = EXPECTED_VIOLATION_REGEX.search(line)
        if not match:
            continue
        col, code, message = match.groups()
        violation_type = ViolationType(code, message)
        violation = Violation(violation_type, lineno + 1, int(col))
        violations.append(violation)
    return violations


def run_flake8_text(file: Path, select: str, format: str = 'default') -> str:
    cmd = ['venv/bin/python', '-m', 'flake8', str(file), f'--select={select}', f'--format={format}']
    process = subprocess.run(cmd, stdout=subprocess.PIPE)
    stdout = process.stdout
    stderr = process.stderr
    if stderr:
        raise Exception(f'flake8 stderr:\n{stderr.decode()}')
    return stdout.decode()
