#
# Queries a full-text search index of git commit history.
#
# How to run:
#   sh query.sh --query_text "author:bob message:'bug fix'"
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