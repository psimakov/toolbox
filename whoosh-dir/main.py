#
# Copyright 2025 Pavel (Pasha) Simakov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import mime

import argparse
import logging
import os
import shutil
from pathlib import Path
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

MAX_SIZE = 5 * 1024 * 1024  # 5MB

CLI_BLUE = "\033[1;34m"
CLI_RED = "\033[1;31m"
CLI_GREEN = "\033[1;32m"
CLI_NC = "\033[0m"


def create_index(index_dir, docs_dir):
    logger.info(f"Storing index at: {index_dir}")
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)

    schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    indexed = 0
    not_text = 0
    too_large = 0
    folders_skipped = 0
    errors = 0

    not_text_ext = {}

    def progress(caption):
        logger.info(
            f"{caption}: " + 
            f"indexed: {indexed}, " +
            f"not text: {not_text}, " +
            f"too large: {too_large}, " +
            f"errors: {errors}, " + 
            f"folders skipped: {folders_skipped}"
        )

    logger.info(f"Indexing: {docs_dir}")
    for file in Path(docs_dir).rglob("*"):
        if any(part in mime.SKIP_FOLDERS for part in file.parts):
            folders_skipped+= 1
            continue
        
        if (indexed + not_text + too_large + errors) % 1000 == 0:
            progress("Indexing progress")

        if file.suffix.lower() not in mime.TEXT_EXTENSIONS:
            not_text += 1
            not_text_ext[file.suffix.lower()] = True
            continue
        if file.stat().st_size > MAX_SIZE:
            too_large += 1
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
            writer.add_document(path=str(file), content=text)
            indexed += 1
        except Exception as e:
            print(f"Error in {file}: {e}")
            errors += 1

    writer.commit()
    progress(f"Indexing completed")
    logger.info(f"All non-text file extensions: {not_text_ext.keys()}")


def search_index(index_dir, query_str, limit):
    logger.info(f"Using index at: {index_dir}")
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        print(CLI_RED, f"Searching for: {query_str}", CLI_NC)

        parser = QueryParser("content", schema=ix.schema)
        query = parser.parse(query_str)
        results = searcher.search(query, limit=limit)

        print(CLI_RED, f"Ready: results: {len(results)}, limit: {limit}", CLI_NC)
        for hit in results:
            print(CLI_GREEN, f"\nScore: {hit.score:.3f}", CLI_NC)
            print(
                CLI_BLUE, f"\n{hit['path']}\n", CLI_NC, f"{hit.highlights('content')}"
            )


def parseargs():
    parser = argparse.ArgumentParser(
        description="Simple Whoosh-based text indexer and search tool."
    )

    parser.add_argument("--data_dir", help="Directory for index files")

    parser.add_argument("--do_index", action="store_true", help="Perform indexing")
    parser.add_argument("--index_dir", help="To pof the directory tree to index")

    parser.add_argument("--do_query", action="store_true", help="Perform query")
    parser.add_argument("--query_text", help="Search query string")
    parser.add_argument(
        "--query_limit", default=10, help="Maximum number of results to return"
    )

    return parser.parse_args()


def main(args):
    if args.do_index:
        create_index(args.data_dir, args.index_dir)
        return

    if args.do_query:
        search_index(args.data_dir, args.query_text, args.query_limit)
        return

    logger.info("Nothing to do.")


if __name__ == "__main__":
    logger.info("STARTED")
    main(parseargs())
    logger.info("COMPLETED")
