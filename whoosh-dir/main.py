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
from pathlib import Path
import shutil
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from whoosh import highlight


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

MAX_SIZE = 5 * 1024 * 1024  # 5MB


class PlainFormatter(highlight.Formatter):
    """Formatter that returns plain text with matched terms in brackets."""

    def format_token(self, text, token, replace=False):
        return highlight.get_text(text, token, replace)


def create_index(index_base_dir, ns, docs_dir):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Building index at: {index_dir}")

    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)

    schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    indexed = 0
    not_text = 0
    too_large = 0
    excluded = 0
    errors = 0

    not_text_ext = {}

    def progress(caption):
        logger.info(
            f"{caption}: "
            + f"indexed: {indexed}, "
            + f"not text: {not_text}, "
            + f"too large: {too_large}, "
            + f"excluded: {excluded}, "
            + f"errors: {errors}"
        )

    logger.info(f"Looking for files in: {docs_dir}")
    for file in Path(docs_dir).rglob("*"):
        if not file.is_file():
            continue

        if any(part in mime.SKIP_FOLDERS for part in file.parts):
            excluded += 1
            continue

        if (indexed + not_text + too_large + errors) % 1000 == 0:
            progress("\tProgress")

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
            logger.error(f"Error in {file}: {e}")
            errors += 1

    logger.info(f"Writing index...")

    writer.commit()
    progress(f"Indexing completed")
    logger.info(f"All non-text file extensions: {not_text_ext.keys()}")


def search_index(index_base_dir, ns, query_str, limit, query_highlight):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Querying index at: {index_dir}")

    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        logger.info(f"Indexed documents: {searcher.doc_count()}")
        logger.info(f"Searching for: {query_str}\n")

        parser = MultifieldParser(["path", "content"], schema=ix.schema)
        query = parser.parse(query_str)

        results = searcher.search(query, limit=limit)
        if not query_highlight:
            results.formatter = PlainFormatter()

        logger.info(f"Ready: results: {len(results)}, limit: {limit}\n")
        for index, hit in enumerate(results):
            logger.info(f"# Result {index} (score {hit.score:.3f})")

            path = hit["path"]
            if path:
                logger.info(f"File: {path}\n")

            content = hit.highlights("content")
            if content:
                logger.info(f"Excerpt: {content}")
            logger.info(f"")


def parseargs():
    parser = argparse.ArgumentParser(
        description="Simple Whoosh-based text indexer and search tool."
    )

    parser.add_argument("--data_dir", help="Main directory for index files")
    parser.add_argument(
        "--ns", default="noname", help="Namespace, a sub-directory for index files"
    )

    parser.add_argument("--do_index", action="store_true", help="Perform indexing")
    parser.add_argument("--index_dir", help="Top of the directory tree to index")

    parser.add_argument("--do_query", action="store_true", help="Perform query")
    parser.add_argument("--query_text", help="Search query string")
    parser.add_argument(
        "--query_highlight",
        default=False,
        help="Highlight matched terms in the query string",
    )
    parser.add_argument(
        "--query_limit", default=10, help="Maximum number of results to return"
    )

    return parser.parse_args()


def main(args):
    if args.do_index:
        assert args.ns, "--ns required"
        assert args.data_dir, "--data_dir required"
        assert args.data_dir, "--index_dir required"
        create_index(args.data_dir, args.ns, args.index_dir)
        return

    if args.do_query:
        assert args.ns, "--ns required"
        assert args.data_dir, "--data_dir required"
        assert args.data_dir, "--index_dir required"
        assert args.query_text, "--query_text"
        assert args.query_limit, "--query_limit"
        search_index(
            args.data_dir,
            args.ns,
            args.query_text,
            int(args.query_limit),
            args.query_highlight,
        )
        return

    logger.info("Nothing to do.")


def report_duration(start_time):
    elapsed = time.time() - start_time
    hours, remainder = divmod(int(elapsed), 3600)
    minutes, seconds = divmod(remainder, 60)

    logger.info(f"Elapsed Time: {hours}h {minutes}m {seconds}s")


if __name__ == "__main__":
    logger.info("STARTED")
    start_time = time.time()
    main(parseargs())
    report_duration(start_time)
    logger.info("COMPLETED")
