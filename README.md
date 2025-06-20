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

Install both manually if needed:

```bash
pip install \
  git+https://github.com/stuarttempleton/volt-logger.git \
  git+https://github.com/stuarttempleton/volt-llm-client.git
````

---

## 💬 Usage

```bash
python volt-chat.py <model_name> <your_name> [--api-url=http://localhost:3000/api/chat/completions]
```

### Example

```bash
python volt-chat.py Gemma3 Alice
```

---

## 🔐 API Token

Make sure the `LLM_API_TOKEN` environment variable is set:

```bash
export LLM_API_TOKEN=your_token_here  # Unix/macOS
# OR
$env:LLM_API_TOKEN = "your_token_here"  # PowerShell
```

---

## Building the Executable (Windows)

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

> ⚠️ The resulting `.exe` includes all dependencies (`requests`, `volt-llm-client`, and `volt-logger`) and can be run on machines without Python installed.

---

## 🧪 Testing the Executable

Run your `.exe` from the command line:

```bash
volt-chat.exe Gemma3 Alice
```

---

## 🪪 License

[MIT](LICENSE)

