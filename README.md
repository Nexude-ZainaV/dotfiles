# dotfiles

[![CI](https://github.com/Nexude-ZainaV/dotfiles/actions/workflows/ci.yml/badge.svg)](https://github.com/Nexude-ZainaV/dotfiles/actions/workflows/ci.yml)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)
![Sublime Text](https://img.shields.io/badge/Sublime%20Text-FF9800?logo=sublimetext&logoColor=white)

This is my editor setup for VS Code and Sublime Text: settings, extensions, and 242
snippets for C, C++, C#, JavaScript/TypeScript, React, Next.js, Node.js, Python,
SQL, PHP, HTML and responsive CSS.

Each snippet has a few short comments on why and when you'd use it. I wrote them
that way so inserting one also reminds me how the construct works.

## Layout

```
dotfiles/
  snippets/
    build.py              generates both editors' snippets from one source
    src/                  one file per language, the source of truth
  vscode/
    settings.json         settings to merge (never overwrites yours)
    extensions.txt        extension list
    snippets/             generated .code-snippets
  sublime/
    Preferences.sublime-settings
    packages.json         Package Control packages (LSP, Emmet...)
    *.sublime-settings    per-language indentation
    snippets/             generated .sublime-snippet files
  scripts/
    install.py            applies everything to this machine
```

## Install

```bash
git clone https://github.com/Nexude-ZainaV/dotfiles.git
cd dotfiles
python scripts/install.py --extensions
```

The installer backs up every file it touches (`*.bak-<timestamp>`) before writing.
Settings are merged so your existing values always win. It also detects machine
paths (the C/C++ compiler and PHP) and queues the Sublime packages, which Package
Control installs on the next start.

## Snippets

| Area | Prefixes |
|---|---|
| Control flow (every language) | `if` `ife` `elif` `ifn` (nested) `tern` `sw` / `match` `for` `while` `dowhile` `try` |
| Timers | `timer` everywhere, plus `timeout` `interval` `debounce` `throttle` `sleep` (JS), `ptimer` (C#), `ctimer` (Python) |
| AJAX | `fetchget` `fetchpost` `fetchtimeout` `fetchform` `xhr` `jqajax` `axios`, `json` (PHP endpoint), `ajaxform` (HTML) |
| Responsive | `bp` (breakpoint + device table), `mq` (mobile-first set), `mqmax` `mqrange` `mqpointer` `cq` `clamp` `grid` `vh`, `umq` (React hook), `img` / `pic` (srcset) |
| File templates | `cfile` `header` `cppfile` `classh` `csfile` `minapi` `xunit` `rfc` `uctx` `npage` `nlayout` `nroute` `nproxy` `express` `router` `script` `fastapi` `pytest` `phpclass` `phpunit` `html5` `reset` `respfile` `ct` |
| Imports at the top | `inc` (C/C++), `usings` (C#), `imp` (JS/TS, Python), grouped in the usual order |

In VS Code the file templates also show up under File > New File... > Snippets, and
in the "fill with snippet" prompt you get in an empty file.

### Notation

I write the snippets in a notation that needs no escaping, and the build compiles
it for each editor:

```text
«1:name»   tab stop 1 with default text   «1»   mirror of tab stop 1   «0»   final cursor
```

That means PHP variables, template literals and backslashes are written exactly as
they appear in code:

```python
("pdoq", "PDO prepared query", r"""
$stmt = $pdo->prepare('SELECT «1:id» FROM «2:users» WHERE «3:email» = :«3»');
""")
```

After editing a source file, rebuild with `python snippets/build.py`. CI rebuilds
too and fails if the generated files don't match.

## License

[MIT](LICENSE)
