# options.py
# 10/18/2025 - Voltur
#
# Loading arguments from command‑line and local config file.
# 


import argparse
import json
import sys
from pathlib import Path
from typing import Dict

# Helpers for loading JSON / YAML
try:
    import yaml  # pip install pyyaml   # optional, for .yaml files
except ImportError:   # pragma: no cover
    yaml = None


def _read_json(path: Path) -> Dict:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _read_yaml(path: Path) -> Dict:
    if yaml is None:          # pragma: no cover
        return {}
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_local_config() -> Dict:
    candidates = [
        Path.cwd() / "volt-config.json",
        Path.cwd() / "volt-config.yaml",
        Path.home() / ".volt-config.rc",
        Path.home() / ".volt-config.json",
        Path.home() / ".volt-config.yaml",
    ]

    for cfg_path in candidates:
        data = _read_json(cfg_path) if cfg_path.suffix == ".json" else _read_yaml(cfg_path)
        if data:
            return data
    return {}


# Argparse boilerplate
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Volt-Chat: a local LLM chat client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # LLM model to use
    parser.add_argument("--persona", dest="persona", metavar="MODEL",
                        help="Name of the LLM model to use")
    # User's chat handle
    parser.add_argument("--handle", dest="handle", metavar="USERNAME",
                        help="Display name of the chat participant")
    # Base URL for local LLM server, include port
    parser.add_argument("--base-url", dest="base_url", metavar="URL",
                        help="Base URL of the local LLM server")
    # System prompt override
    parser.add_argument("--system-prompt", dest="system_prompt",
                        help="Override the system prompt")
    # Config file path
    parser.add_argument("--config", dest="config_path", metavar="PATH",
                        help="Explicitly load a config file (JSON or YAML)")
    # transcript file base directory
    parser.add_argument("--base-dir", dest="base_dir", metavar="PATH",
                        help="Base directory for saving/loading transcripts")
    # custom shell name
    parser.add_argument("--shell-name", dest="shell_name", metavar="NAME",
                        help="Custom shell name to display in the prompt")
    # Enable shell functions
    parser.add_argument("--set-exec-privs", dest="shell_exec_privs", metavar="0|1|2|3",
                        help="Set shell execution privileges (for /exec command). Use with caution! 0 = disabled")

    return parser


# Resolve the final configuration
def resolve_options() -> argparse.Namespace:

    # Defaults
    defaults: Dict = {
        "base_url": "http://localhost:3000",
        "persona": "Gemma3",
        "handle": "User",
        "system_prompt": "We are best buds!",
        "base_dir": str(Path.home()),
        "shell_name": "volt-shell",
        "shell_exec_privs": 0,
    }

    # Load the config file (auto or explicit)
    parser = _build_parser()

    # First parse once to grab --config early
    initial_args, _ = parser.parse_known_args()
    if initial_args.config_path:
        cfg_path = Path(initial_args.config_path).expanduser()
        cfg = _read_json(cfg_path) if cfg_path.suffix == ".json" else _read_yaml(cfg_path)
    else:
        cfg = _load_local_config()

    # Merge (config overrides defaults)
    merged: Dict = {**defaults, **cfg}

    # Parse again so we get every CLI flag
    final_args = parser.parse_args()

    # Command‑line wins – only override if the flag was actually given
    if final_args.base_url is not None:
        merged["base_url"] = final_args.base_url
    if final_args.system_prompt is not None:
        merged["system_prompt"] = final_args.system_prompt
    if final_args.persona is not None:
        merged["persona"] = final_args.persona
    if final_args.handle is not None:
        merged["handle"] = final_args.handle
    if final_args.base_dir is not None:
        merged["base_dir"] = final_args.base_dir
    if final_args.shell_name is not None:
        merged["shell_name"] = final_args.shell_name
    if final_args.shell_exec_privs is not None:
        merged["shell_exec_privs"] = final_args.shell_exec_privs

    return argparse.Namespace(**merged)

__all__ = ["resolve_options"]