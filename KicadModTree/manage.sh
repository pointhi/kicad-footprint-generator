BASE_DIR=$(dirname `readlink -f $0`)
PYTHONPATH=$BASE_DIR
ACTION=$1

pep8_check() {
    echo ''
    echo '[!] Running pep8 check'
    pep8 --max-line-length=120 ./
}

unit_tests() {
    echo ''
    echo '[!] Running unit tests'
    python tests/test.py
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
    tests                - Run all tests
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
