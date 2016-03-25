BASE_DIR=$(dirname `readlink -f $0`)
PYTHONPATH=$BASE_DIR
KICADMODTREE_DIR="$BASE_DIR/KicadModTree"
ACTION=$1

update_dev_packages() {
    pip install --upgrade -r "$BASE_DIR/requirements-dev.txt"
}

pep8_check() {
    echo ''
    echo '[!] Running pep8 check'
    pep8 --max-line-length=120 "$KICADMODTREE_DIR/"
}

unit_tests() {
    echo ''
    echo '[!] Running unit tests'
    python "$KICADMODTREE_DIR/tests/test.py"
}

py_test_coverage() {
    echo '[!] Running python test coverage'
    PYTHONPATH=`pwd` python -m nose2 -C --coverage "$KICADMODTREE_DIR" --coverage-report term-missing -s "$KICADMODTREE_DIR/tests"
}

tests() {
    set -e
    unit_tests
    pep8_check
    set +e
}



help() {
    [ -z "$1" ] || printf "Error: $1\n"
    echo ''
    echo "Searx manage.sh help

Commands
========
    help                 - This text
    pep8_check           - Pep8 validation
    unit_tests           - Run unit tests
    py_test_coverage     - Unit test coverage
    tests                - Run all tests
    update_dev_packages  - Check & update development and production dependency changes
"
}

#[ "$(command -V "$ACTION" | grep ' function$')" = "" ] \
#    && help "action not found" \
#    || $ACTION
if [ -n "$(type -t $ACTION)" ] && [ "$(type -t $ACTION)" = function ]; then
     $ACTION
 else
     help "action not found"
fi
