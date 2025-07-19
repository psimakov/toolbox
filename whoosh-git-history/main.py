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


import argparse
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import shutil
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from whoosh import highlight


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

MAX_SIZE = 5 * 1024 * 1024  # 5MB


def parse_git_date_to_utc(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
    return dt.astimezone(timezone.utc)


def unpack(history_item):
    commit_on = None
    author = None
    lines = []
    files = []
    
    space_sep = "    "
    
    can_files = False
    for item in history_item["info"]:
        if item.startswith("CommitDate: "):
            assert commit_on is None
            commit_on = item.split("CommitDate: ")[1]
            
        if item.startswith("Author: "):
            assert author is None
            author = item.split("Author: ")[1]

        if item.startswith(space_sep):
            lines.append(item.split(space_sep)[1])
            continue
        
        if item == "":
            can_files = True
            continue

        if can_files:
            files.append(item.split("\t")[1])
            continue

    return {
        "commit": history_item["commit"],
        "author": author,
        "timestamp": parse_git_date_to_utc(commit_on),
        "message": " ".join(lines),
        "files": files,
    }


def create_index(index_base_dir, ns, json_fn):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Building index at: {index_dir}")

    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)

    logger.info(f"Loading git history from {json_fn}")
    with open(json_fn, "r") as stream:
        data = json.loads(stream.read())
    logger.info(f"Loaded {len(data)} items")
    
    schema = Schema(
        commit=ID(stored=True, unique=True),
        author=TEXT(stored=True),
        timestamp=DATETIME(stored=True),
        message=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        files=TEXT(stored=True),
    )
    ix = create_in(index_dir, schema)
    writer = ix.writer()
    
    count = 0
    for index, packed in enumerate(data):
        count += 1
        if count % 1000 == 0:
            logger.info(f"\tProgress: indexed: {count}")
        
        item = unpack(packed)
        writer.add_document(
            commit=item["commit"],
            author=item["author"],
            timestamp=item["timestamp"],
            message=item["message"],
            files=item["files"],
        )

    logger.info(f"Indexing completed: indexed: {count}")
    logger.info(f"Writing index...")

    writer.commit()
    logger.info(f"Indexing completed")


def search_index(index_base_dir, ns, query_str, limit, query_highlight):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Querying index at: {index_dir}")

    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        logger.info(f"Searching for: {query_str}\n")

        parser = QueryParser("content", schema=ix.schema)
        query = parser.parse(query_str)

        results = searcher.search(query, limit=limit)

        logger.info(f"Ready: results: {len(results)}, limit: {limit}\n")
        for index, hit in enumerate(results):
            logger.info(f"# Result {index} (score {hit.score:.3f})")

            for part in [
                "commit", "author", "timestamp", "message", "files"
            ]:
                item = hit[part]
                if item:
                    logger.info(f"{part}: {item}")

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
    parser.add_argument("--json_fn", help="JSON file with git history.")

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
        assert args.json_fn, "--json_fn required"
        create_index(args.data_dir, args.ns, args.json_fn)
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
