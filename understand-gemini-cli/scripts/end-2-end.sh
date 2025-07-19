#
# Tests a collection of tools and extensions designed for
# LLM-assisted coding, using the Gemini CLI repository as
# the evaluation target.
#
# How to run:
#   sh end-2-end.sh
#

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$DIR/../work_dir"
TOOLBOX_DIR="$DIR/../.."

echo "Cleaning folders"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

echo "Cloning Gemini CLI repo"
git clone https://github.com/google-gemini/gemini-cli.git \
    "$WORK_DIR/gemini-cli"

echo "Building a full-text search index of files & content"
sh "$TOOLBOX_DIR/whoosh-dir/scripts/index.sh" \
    --index_dir "$WORK_DIR/gemini-cli"

echo "Querying a full-text search index of files & content"
sh "$TOOLBOX_DIR/whoosh-dir/scripts/query.sh" \
    --query_text "You are an interactive CLI agent" \
    --query_limit 1

echo "Capturing git commit history"
python3 \
    "$TOOLBOX_DIR/git-history-to-json/main.py" \
    --git-dir "$WORK_DIR/gemini-cli/.git" \
    --json-fn "$WORK_DIR/git-commit-history.json"

echo "Building a full-text search index of git commit history"
sh "$TOOLBOX_DIR/whoosh-git-history/scripts/index.sh" \
    --json_fn "$WORK_DIR/git-commit-history.json"
