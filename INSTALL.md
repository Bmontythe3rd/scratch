# Installation Guide

## Prerequisites

- **Python 3.9 or later** — check with `python3 --version`
- **git** — to clone the repository
- A package installer: **uv** (recommended), **pipx**, or plain **pip** in a virtual environment

---

## Method 1 — uv (recommended)

`uv` creates an isolated environment for the tool automatically and puts `scratch` on your PATH.

### Step 1: Install uv

**Arch Linux**
```bash
sudo pacman -S uv
```

**macOS / Linux (any distro) via installer script**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Clone the repo
```bash
git clone https://github.com/Bmontythe3rd/scratch.git
cd scratch
```

### Step 3: Install Scratch as a tool
```bash
uv tool install .
```

### Step 4: Add uv's tool bin directory to your PATH (first time only)
```bash
uv tool update-shell
```

Then open a new terminal (or `source ~/.bashrc` / `source ~/.zshrc`).

### Step 5: Verify
```bash
scratch --version
```

---

## Method 2 — pipx

`pipx` is another tool designed specifically for installing Python CLI apps in isolated environments.

### Step 1: Install pipx

**Arch Linux**
```bash
sudo pacman -S python-pipx
```

**Other Linux / macOS**
```bash
pip install --user pipx
pipx ensurepath
```

### Step 2: Clone and install
```bash
git clone https://github.com/Bmontythe3rd/scratch.git
cd scratch
pipx install .
```

### Step 3: Verify
```bash
scratch --version
```

---

## Method 3 — pip + virtual environment

Use this if you don't want to install uv or pipx, or if you want an editable (hackable) install.

### Step 1: Clone the repo
```bash
git clone https://github.com/Bmontythe3rd/scratch.git
cd scratch
```

### Step 2: Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### Step 3: Install
```bash
# Regular install
pip install .

# Editable install (code changes take effect immediately — good for development)
pip install -e .
```

### Step 4: Use it

While the virtual environment is active:
```bash
scratch --version
```

To use `scratch` outside the venv, either activate it each time or add a shell alias:
```bash
echo 'alias scratch="/path/to/scratch/.venv/bin/scratch"' >> ~/.bashrc
source ~/.bashrc
```

---

## Usage after installation

```bash
scratch                # open an empty buffer
scratch notes.txt      # open (or create) a file
scratch --version      # print version and exit
```

See the [README](README.md) for the full keybindings reference.

---

## Uninstalling

**uv**
```bash
uv tool uninstall scratch-editor
```

**pipx**
```bash
pipx uninstall scratch-editor
```

**pip (venv)**
```bash
# Deactivate and delete the venv directory
deactivate
rm -rf .venv
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `scratch: command not found` after uv install | Run `uv tool update-shell` and open a new terminal |
| `scratch: command not found` after pipx install | Run `pipx ensurepath` and open a new terminal |
| `ModuleNotFoundError: textual` | The venv isn't activated, or install didn't complete — re-run `pip install .` inside the venv |
| Syntax highlighting missing | Install the `[syntax]` extra: `pip install "textual[syntax]"` — it's included by default but tree-sitter parsers may need a C compiler |
| Python version error | Scratch requires Python 3.9+. Run `python3 --version` to confirm |
