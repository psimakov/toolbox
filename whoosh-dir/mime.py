SKIP_FOLDERS = {'.git', '__pycache__', '.venv', '.idea'}

TEXT_EXTENSIONS = {
    # General text and documentation
    '.txt', '.md', '.markdown', '.rst', '.log', '.ini', '.cfg', '.conf', '.properties',

    # Source code files
    '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.js', '.ts', '.jsx', '.tsx',
    '.rb', '.php', '.pl', '.sh', '.bat', '.ps1', '.go', '.rs', '.swift', '.kt', '.kts',
    '.m', '.mm', '.scala', '.lua', '.dart', '.r', '.jl', '.vb', '.vbs', '.groovy', '.asm',
    '.sql', '.tsql', '.graphql', '.gql',

    # Web and templating
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml', '.xhtml', '.vue', '.ejs',
    '.twig', '.jinja', '.mustache', '.hbs', '.handlebars', '.liquid',

    # Config, serialization, and data
    '.json', '.yaml', '.yml', '.toml', '.env', '.ini', '.conf', '.cfg', '.csv', '.tsv',
    '.ndjson', '.avsc', '.proto', '.puml',

    # Build, CI, tooling
    '.makefile', '.mk', '.cmake', '.gradle', '.pom', '.dockerfile', '.gitignore',
    '.gitattributes', '.editorconfig', '.babelrc', '.eslintignore', '.prettierrc', '.stylelintrc',

    # Notebooks and scripts
    '.ipynb', '.rmd', '.tex', '.bib', '.do', '.sql', '.sas', '.scm', '.clj', '.coffee',

    # Misc text-based
    '.txt', '.nfo', '.jsonl', '.lock', '.manifest', '.metadata', '.readme',

    # Project-specific or lesser-known text formats
    '.cue', '.m3u', '.mdx', '.nix', '.tf', '.tfvars', '.mcfunction', '.config', '.sln',
    '.csproj', '.vcxproj', '.asmx', '.aspx', '.cshtml', '.fs', '.fsx', '.targets', '.props',
    '.http', '.rest', '.yarnrc', '.npmrc', '.bazel', '.bzl', '.build', '.buck', '.jake',
    '.gyp', '.ipxe', '.re', '.rei', '.ml', '.mli', '.po', '.pot'
}
