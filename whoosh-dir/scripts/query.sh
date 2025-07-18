#
# How to run:
#   query.sh ~/ "API_KEY="
#

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$DIR/.."

./py_env/bin/python \
    ./main.py \
    --data_dir ./whoosh_env \
    --do_query \
    --query_text "$1"

popd