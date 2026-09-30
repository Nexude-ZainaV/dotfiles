# dotfiles

[![CI](https://github.com/Nexude-ZainaV/dotfiles/actions/workflows/ci.yml/badge.svg)](https://github.com/Nexude-ZainaV/dotfiles/actions/workflows/ci.yml)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)
![Sublime Text](https://img.shields.io/badge/Sublime%20Text-FF9800?logo=sublimetext&logoColor=white)

My editor setup for **VS Code** and **Sublime Text**: settings, extensions, and a
library of **242 guided snippets** across C, C++, C#, JavaScript/TypeScript, React,
Next.js, Node.js, Python, SQL, PHP, HTML and responsive CSS.

Every snippet carries short comments that explain *why* and *when* to use the
construct, so inserting one doubles as a refresher.

## What's inside

```
dotfiles/
├── snippets/
│   ├── build.py          # generates both editors' snippets from one source
│   └── src/              # one file per language: the source of truth
├── vscode/
│   ├── settings.json     # curated settings (merged, never overwrites yours)
│   ├── extensions.txt    # extension list
│   └── snippets/         # generated .code-snippets
├── sublime/
│   ├── Preferences.sublime-settings
│   ├── packages.json     # Package Control packages (LSP, Emmet...)
│   ├── *.sublime-settings  # per-language indentation
│   └── snippets/         # generated .sublime-snippet files
└── scripts/
    └── install.py        # applies everything to this machine
```

## Install

```bash
git clone https://github.com/Nexude-ZainaV/dotfiles.git
cd dotfiles
python scripts/install.py --extensions
```

The installer backs up every file it touches (`*.bak-<timestamp>`), merges settings
so your existing values always win, detects machine paths (C/C++ compiler, PHP) and
queues Sublime packages for Package Control to install on the next start.

## Snippet highlights

| Area | Prefixes |
|---|---|
| Control flow (every language) | `if` `ife` `elif` `ifn` (nested) `tern` `sw` / `match` `for` `while` `dowhile` `try` |
| Timers | `timer` everywhere, plus `timeout` `interval` `debounce` `throttle` `sleep` (JS), `ptimer` (C#), `ctimer` (Python) |
| AJAX | `fetchget` `fetchpost` `fetchtimeout` `fetchform` `xhr` `jqajax` `axios`, `json` (PHP endpoint), `ajaxform` (HTML) |
| Responsive | `bp` (breakpoint + device table), `mq` (mobile-first set), `mqmax` `mqrange` `mqpointer` `cq` `clamp` `grid` `vh`, `umq` (React hook), `img` / `pic` (srcset) |
| File templates | `cfile` `header` `cppfile` `classh` `csfile` `minapi` `xunit` `rfc` `uctx` `npage` `nlayout` `nroute` `nproxy` `express` `router` `script` `fastapi` `pytest` `phpclass` `phpunit` `html5` `reset` `respfile` `ct` |
| Imports at the top | `inc` (C/C++), `usings` (C#), `imp` (JS/TS, Python) in industry-standard group order |

In VS Code, file templates also appear under **File → New File... → Snippets** and
in the "fill with snippet" prompt of an empty file.

### Notation

Snippets are authored in an escape-free notation and compiled for each editor:

```text
«1:name»   tab stop 1 with default text   «1»   mirror of tab stop 1   «0»   final cursor
```

so PHP variables, template literals and backslashes are written exactly as code:

```python
("pdoq", "PDO prepared query", r"""
$stmt = $pdo->prepare('SELECT «1:id» FROM «2:users» WHERE «3:email» = :«3»');
""")
```

Rebuild after editing a source file: `python snippets/build.py`.

## License

[MIT](LICENSE)
