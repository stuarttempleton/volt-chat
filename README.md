# volt-chat

**volt-chat** is a simple, terminal-based chat utility for interacting with local LLMs via OpenWebUI or Ollama-compatible APIs.  
It uses [`volt-llm-client`](https://github.com/stuarttempleton/volt-llm-client) under the hood for message handling and [`volt-logger`](https://github.com/stuarttempleton/volt-logger) for clean output.

---

## 🚀 Features

- Chat with local LLMs (e.g. Ollama, OpenWebUI-compatible)
- Context-aware, multi-turn conversation using `LLMConversation`
- Friendly, styled CLI experience with ANSI color support
- Easy to customize prompts, models, and API endpoints

---


## 📦 Requirements

- Python 3.7+
- [`volt-llm-client`](https://github.com/stuarttempleton/volt-llm-client)
- [`volt-logger`](https://github.com/stuarttempleton/volt-logger)
- [`pyyaml`](https://pyyaml.org/) (for YAML config support, optional)

Install all dependencies:

```bash
pip install -r requirements.txt
# or, manually:
pip install volt-llm-client pyyaml
```

---


## 💬 Usage

```bash
python volt-chat.py [--persona=MODEL] [--handle=USERNAME] [--base-url=URL] [--system-prompt=TEXT] [--config=PATH] [--no-color]
```

### Examples

```bash
python volt-chat.py --persona=Gemma3:12b --handle=Alice --base-url=http://localhost:3000
python volt-chat.py --persona=Llama2 --handle=Bob
python volt-chat.py --help
```

You can use environment variables in arguments, e.g.:

```powershell
python volt-chat.py --handle=$env:USERNAME
```

---

## 🔐 API Token

If your LLM server requires an API or bearer token, make sure the `LLM_API_TOKEN` environment variable is set:

```bash
export LLM_API_TOKEN=your_token_here  # Unix/macOS
# OR
$env:LLM_API_TOKEN = "your_token_here"  # PowerShell
```

---

## � Configuration Files

You can use a local config file for persistent settings:

- `volt-config.json` or `volt-config.yaml` (in your project folder or home directory)
- Or specify a config file with `--config=PATH`

User config files are ignored by git (see `.gitignore`).

Example `volt-config.json`:
```json
{
    "persona": "Gemma3",
    "handle": "Alice",
    "base_url": "http://localhost:3000"
}
```

---


## 🏗️ Building the Executable (Windows)

To build a standalone Windows `.exe` using PyInstaller:

1. Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Build the executable:
    ```bash
    python -m PyInstaller --onefile volt-chat.py
    ```

4. Your standalone executable will be in the `dist/` folder:
    ```
    dist/volt-chat.exe
    ```

> ⚠️ The resulting `.exe` includes all dependencies (`requests`, `volt-llm-client`, `volt-logger`, and optionally `pyyaml`) and can be run on machines without Python installed.

---


## 🧪 Testing the Executable

Run your `.exe` from the command line:

```bash
volt-chat.exe --persona=Gemma3 --handle=Alice
```

---

## 🪪 License

[MIT](LICENSE)

