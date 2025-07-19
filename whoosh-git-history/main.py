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
import logging
import os
from pathlib import Path
import shutil
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import highlight


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

MAX_SIZE = 5 * 1024 * 1024  # 5MB


def create_index(index_base_dir, ns, json_fn):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Building index at: {index_dir}")

    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)

    raise Exception("Not Implemented")


def search_index(index_base_dir, ns, query_str, limit, query_highlight):
    index_dir = os.path.join(index_base_dir, ns)
    logger.info(f"Querying index at: {index_dir}")

    raise Exception("Not Implemented")


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
