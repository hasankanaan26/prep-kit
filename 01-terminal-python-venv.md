# 01 Terminal, Python and a virtual environment

About 40 minutes. By the end you'll have Python installed and a private Python setup for
this kit.

## Get the kit

The kit lives at <https://github.com/hasankanaan26/prep-kit>. You don't need git yet:
on that page, click the green "Code" button, then "Download ZIP", and unzip it. (If you
already use git: `git clone https://github.com/hasankanaan26/prep-kit.git`.)

Put the `prep-kit` folder somewhere easy to find, for example a `projects` folder in your
home directory (`C:\Users\you\projects\prep-kit`). A downloaded ZIP unzips as
`prep-kit-main`; rename it to `prep-kit`. In step 08 you'll download the course code into
the same `projects` folder, next to it.

## The terminal

A terminal is a window where you type commands instead of clicking. Everything in this
course starts there.

- Windows: open PowerShell. In VS Code, press Ctrl+` to get one inside the editor.
- macOS: open Terminal (Cmd+Space, type "Terminal").

Five commands are enough for this kit:

| What you want | Windows (PowerShell) | macOS / Linux |
| --- | --- | --- |
| Where am I? | `pwd` | `pwd` |
| What's in this folder? | `ls` | `ls` |
| Go into a folder | `cd prep-kit` | `cd prep-kit` |
| Go up one level | `cd ..` | `cd ..` |
| Clear the screen | `cls` | `clear` |

The folder you're "in" matters. When a step says "from `prep-kit/`", `cd` there first.
Running a script from the wrong folder is the most common first-week mistake, and some
scripts fail silently when you do it.

## Install Python

The course uses Python 3.12 (3.11 also works).

- Windows: download it from <https://www.python.org/downloads/>. Windows comes with a
  launcher called `py`, which is how you run Python here. Plain `python` often isn't set up.
  Check with `py -3.12 --version`.
- macOS: `brew install python@3.12` if you use Homebrew, or the installer from python.org.
  Check with `python3.12 --version`.

## What a virtual environment is

Every Python project needs packages (other people's code: `openai`, `httpx` and so on).
If you install them all into the one Python on your computer, projects end up fighting
over versions.

A virtual environment ("venv") is a folder with its own private copy of Python and its own
packages, for one project. Think of a separate toolbox per job: what you put in this one
doesn't mess up the others, and if it gets into a bad state you delete the folder and make
a new one.

## Make one for the kit

From the `prep-kit/` folder (`cd` into it first):

```powershell
# Windows
py -3.12 -m venv .venv
.venv\Scripts\activate
```

```bash
# macOS / Linux
python3.12 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. That's how you know it's active. You do this
`activate` step every time you open a new terminal for the course.

If PowerShell says running scripts is disabled, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Install the kit's packages

```powershell
pip install -r requirements.txt
```

`pip` is Python's package installer, and `requirements.txt` is the shopping list. This one
is small and takes a minute or two. The course gets its own venv and a much bigger list in
step 08: one toolbox per project.

## Check it

```powershell
py code\where_am_i.py
```

(On macOS/Linux, with the venv active, use `python code/where_am_i.py`. Inside an
active venv, `python` always means the venv's Python on every system.)

You should see `Virtual env : YES` and four `ok` packages. For a useful comparison, open a
second terminal without activating anything and run it again: it reports a different
Python, and probably missing packages. That difference is the whole point of a venv.

## If something went wrong

| You see | Try |
| --- | --- |
| `py` or `python` is not recognized | Reinstall Python and tick "Add python.exe to PATH" |
| `running scripts is disabled` | The `Set-ExecutionPolicy` line above |
| `pip` installs, but the script can't find the package | The venv wasn't active when you ran pip. Activate, install again |
| You're lost and the venv is a mess | Delete the `.venv` folder and make it again. Nothing else is lost |

Next: [02 APIs](02-apis.md)
