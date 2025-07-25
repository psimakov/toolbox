#
# Queries a full-text search index of all files in a folder tree.
#
# How to run:
#   sh query.sh --query_text "Ultimate Question of Life, the Universe, and Everything"
#

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$DIR/.."

./py_env/bin/python \
    ./main.py \
    --data_dir ./whoosh_env \
    --do_query \
    "$@"

popd