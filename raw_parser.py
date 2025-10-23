import shlex

def split_shell_top_level(cmd, delimiters):
    """
    Splits a command string by delimiters (like &&, ||, ;) at top level,
    respecting quotes and parentheses.
    Returns a list of (segment, operator) pairs.
    """
    segments = []
    current = ""
    op = None
    quote = None
    escape = False
    depth = 0

    i = 0
    while i < len(cmd):
        ch = cmd[i]

        if escape:
            current += ch
            escape = False
            i += 1
            continue

        if ch == "\\":
            current += ch
            escape = True
            i += 1
            continue

        if ch in ("'", '"'):
            if quote == ch:
                quote = None
            elif quote is None:
                quote = ch
            current += ch
            i += 1
            continue

        if ch == "(" and not quote:
            depth += 1
        elif ch == ")" and not quote and depth > 0:
            depth -= 1

        # Detect top-level operator
        if not quote and depth == 0:
            for delim in delimiters:
                if cmd.startswith(delim, i):
                    if current.strip():
                        segments.append((current.strip(), op))
                    op = delim.strip()
                    current = ""
                    i += len(delim)
                    break
            else:
                current += ch
                i += 1
        else:
            current += ch
            i += 1

    if current.strip():
        segments.append((current.strip(), op))
    return segments


def parse_redirection(cmd):
    """
    Detects > and >> outside quotes and parentheses.
    Returns (base_cmd, target_file, append)
    """
    quote = None
    escape = False
    depth = 0

    for i, ch in enumerate(cmd):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch in ("'", '"'):
            if quote == ch:
                quote = None
            elif not quote:
                quote = ch
            continue
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if not quote and depth == 0:
            if cmd[i:i+2] == ">>":
                return cmd[:i].strip(), cmd[i+2:].strip(), True
            elif ch == ">":
                return cmd[:i].strip(), cmd[i+1:].strip(), False
    return cmd.strip(), None, False


def parse_pipeline(cmd):
    """
    Splits a pipeline (|) respecting quotes and parentheses.
    Returns list of commands (each as list of tokens).
    """
    parts = split_shell_top_level(cmd, ["|"])
    pipeline = [shlex.split(seg.strip()) for seg, _ in parts]
    return pipeline


def parse_raw_command(raw_cmd):
    """
    Parse raw shell string into structured JSON task format.
    """
    tasks = []
    segments = split_shell_top_level(raw_cmd, ["&&", "||", ";"])

    for seg, prev_op in segments:
        task = {}

        # Background
        if seg.endswith("&"):
            task["background"] = True
            seg = seg[:-1].strip()

        # Subshell
        if seg.startswith("(") and seg.endswith(")"):
            inner = seg[1:-1].strip()
            task["type"] = "subshell"
            task["tasks"] = parse_raw_command(inner)
        else:
            # Redirection
            base, out, append = parse_redirection(seg)
            if out:
                task["stdout"] = out
                task["append"] = append

            # Pipeline or single command
            if "|" in base:
                task["cmd"] = parse_pipeline(base)  
            else:
                task["cmd"] = shlex.split(base)
            
            BUILTINS = {"cd", "pwd", "exit"}  # example set
            if "cmd" in task:
                if isinstance(task["cmd"], list) and task["cmd"]:
                    if task["cmd"][0] in BUILTINS:
                        task["type"] = "builtin"
                    else:
                        task["type"] = "external"
            print(task)

        # Conditional
        if prev_op == "&&":
            task["run_if"] = "last_success"
        elif prev_op == "||":
            task["run_if"] = "last_failed"
        else:
            task["run_if"] = "always"

        tasks.append(task)

    return tasks
