#
# Copyright 2025 Pavel Simakov
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

"""

    Queries git repository for history and exports it into JSON. No dependencies, but git.
    
    How to run:
    
        cd ~/
        mkdir -p ~/work/projects/tmp/
        git clone https://github.com/psimakov/toolbox.git
        git clone https://github.com/openai/openai-cookbook
        cd openai-cookbook

        python3 \
            ../toolbox/git-history-to-json/main.py \
            --git-dir "./.git" \
            --since "2025-06-21 00:00:00" \
            --until "2025-06-27 23:59:59" \
            --json_fn "weekly-grounding-data_2027-06-27.json"

"""

import argparse
import json
import logging


logger = logging.getLogger(__name__)


def runInShell(cmd):
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode:
        raise Exception(
            "Error code: %s\n%s\n%s" % (result.returncode, result.stdout, result.stderr)
        )
    return result.stdout.decode("utf-8").strip()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--git-dir", type=str, help="Folder to run git commands in.")
    parser.add_argument(
        "--since", type=str, help="Expression to pass into 'git log --since=\"\"' option."
    )
    parser.add_argument(
        "--until", type=str, help="Expression to pass into 'git log --until=\"\"' option."
    )
    parser.add_argument("--json_fn", type=str, help="Name of JSON file to output.")

    return parser.parse_args()


def git_commit_hashes(git_dir, since, until):
    logger.info("Working with git dir: %s" % git_dir)
    logger.info("Considering changes: since '%s', until '%s'.: %s" % (since, until))
    result = runInShell(
        ["git", "--git-dir", git_dir, "log", "--since", since, "--until", until, "--pretty=format:%H"]
    )
    return result.strip().split("\n")


def git_show(git_dir, since, until):
    commit_hashes = git_commit_hashes(git_dir, since, until)
    logger.info("Collected commit hashes: %s" % len(commit_hashes))

    commit_data = []
    for index, commit in enumerate(commit_hashes):
        if (index + 1) % 100 == 0:
            logger.info("Inspecting %s of %s" % (index, len(commit_hashes)))

        show_result = runInShell(
            [
                "git",
                "--git-dir",
                git_dir,
                "show",
                "--format=fuller",
                "--name-status",
                commit,
            ]
        )

        commit_data.append({"commit": commit, "info": show_result.strip().split("\n")})

    return commit_data


def git_history_to_json(args):
    data = git_show(args.git_dir, args.since)

    logger.info("Writing JSON output to: %s" % args.json_fn)
    with open(args.json_fn, "w") as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    logger.info("\nSTARTED: %s" % __file__)
    git_history_to_json(parse_args())
    logger.info("COMPLETED: %s\n" % __file__)
