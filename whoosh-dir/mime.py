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


SKIP_FOLDERS = {'.git', '__pycache__', '.venv', '.idea'}

TEXT_EXTENSIONS = {
    # General text and documentation
    '.txt', '.md', '.markdown', '.rst', '.log', '.ini', '.cfg', '.conf', '.properties',
    '.nfo', '.readme',

    # Source code files
    '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.js', '.ts', '.jsx', '.tsx',
    '.rb', '.php', '.pl', '.sh', '.bat', '.ps1', '.go', '.rs', '.swift', '.kt', '.kts',
    '.m', '.mm', '.scala', '.lua', '.dart', '.r', '.jl', '.vb', '.vbs', '.groovy', '.asm',
    '.sql', '.tsql', '.graphql', '.gql', '.awk', '.rake', '.lkml',

    # Web and templating
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml', '.xhtml', '.vue', '.ejs',
    '.twig', '.jinja', '.mustache', '.hbs', '.handlebars', '.liquid', '.slim', '.tmpl',
    '.template', '.tpl', '.erb',

    # Config, serialization, and data
    '.json', '.yaml', '.yml', '.toml', '.env', '.csv', '.tsv', '.ndjson', '.avsc', '.proto', '.puml',
    '.textproto',

    # Build, CI, tooling
    '.makefile', '.mk', '.cmake', '.gradle', '.pom', '.dockerfile', '.gitignore',
    '.gitattributes', '.editorconfig', '.babelrc', '.eslintignore', '.prettierrc', '.stylelintrc',
    '.bazel', '.bzl', '.bazelrc', '.bazelproject', '.sum', '.mod', '.lcov',

    # Notebooks and scripts
    '.ipynb', '.rmd', '.tex', '.bib', '.do', '.sas', '.scm', '.clj', '.coffee', '.script',

    # Project-specific or lesser-known text formats
    '.cue', '.m3u', '.mdx', '.nix', '.tf', '.tfvars', '.mcfunction', '.config', '.sln',
    '.csproj', '.vcxproj', '.asmx', '.aspx', '.cshtml', '.fs', '.fsx', '.targets', '.props',
    '.http', '.rest', '.yarnrc', '.npmrc', '.build', '.buck', '.jake', '.gyp', '.ipxe', '.re',
    '.rei', '.ml', '.mli', '.po', '.pot', '.mf', '.gemspec', '.patch', '.dtd', '.src', '.feature',
    '.jflex', '.map', '.list', '.expected', '.rbi', '.d', '.sky'
}
