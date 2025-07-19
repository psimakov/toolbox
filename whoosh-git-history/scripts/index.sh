#
# Building a full-text search index of git commit history.
#
# How to run:
#   index.sh --json_fn "./git-commit-history.json"
#

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$DIR/.."

if [ ! -d "./py_env" ]; then
    python3 -m venv ./py_env    
    ./py_env/bin/pip install -r ./requirements.txt
fi

./py_env/bin/python \
    ./main.py \
    --data_dir ./whoosh_env \
    --do_index \
    "$@"

popd