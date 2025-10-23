import os
import subprocess
import threading
import shlex
import sys

class ExecutionManager:
    def __init__(self):
        self.cwd = os.getcwd()

    def show(self):
        print(f"Current working directory: {self.cwd}")

    # ----------------------
    # Entry point: run structured task list
    # ----------------------
    def exec_tasks(self, tasks):
        last_exit_code = 0
        for task in tasks:
            last_exit_code = self._run_task(task, last_exit_code)
        return last_exit_code

    # ----------------------
    # Run a single task
    # ----------------------
    def _run_task(self, task, last_exit_code):
        # Conditional execution
        run_if = task.get("run_if", "always")
        if run_if == "last_failed" and last_exit_code == 0:
            return last_exit_code
        if run_if == "last_success" and last_exit_code != 0:
            return last_exit_code

        # Builtin commands
        if task.get("type") == "builtin":
            return self._handle_builtin(task["cmd"], task.get("stdout"), task.get("append"))

        # Subshell
        if task.get("type") == "subshell":
            subshell = ExecutionManager()
            subshell.cwd = self.cwd
            inner_tasks = task.get("tasks", [])
            return subshell.exec_tasks(inner_tasks)

        # Background
        if task.get("background"):
            threading.Thread(target=self._run_pipeline,
                             args=(task["cmd"], task.get("stdout"), task.get("append", False)),
                             daemon=True).start()
            display = " | ".join(" ".join(p) for p in task["cmd"])
            print(f"[bg] started: {display}")

            return 0

        # Normal command / pipeline
        return self._run_pipeline(task["cmd"], task.get("stdout"), task.get("append", False))

    # ----------------------
    # Handle pipes and redirection
    # ----------------------
    def _run_pipeline(self, cmd, stdout_target=None, append=False):
        # cmd can be a single command or list of lists (pipeline)
        if isinstance(cmd[0], list):
            pipeline_parts = cmd
        else:
            pipeline_parts = [cmd]

        prev_proc = None
        procs = []
        num_cmds = len(pipeline_parts)

        for i, args in enumerate(pipeline_parts):
            stdin = prev_proc.stdout if prev_proc else None
            stdout = subprocess.PIPE if i < num_cmds - 1 else None

            if i == num_cmds - 1 and stdout_target:
                mode = "ab" if append else "wb"
                stdout = open(stdout_target, mode)

            try:
                proc = subprocess.Popen(
                    args,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    cwd=self.cwd,
                )
                procs.append(proc)
            except FileNotFoundError:
                print(f"Command not found: {args[0]}")
                return 127
            finally:
                if prev_proc and prev_proc.stdout:
                    prev_proc.stdout.close()
            prev_proc = proc

        if not procs:
            return 0

        out, err = procs[-1].communicate()

        if out and not stdout_target:
            print(out.decode(errors="ignore"), end="")
        if err:
            print(err.decode(errors="ignore"), end="")

        return procs[-1].wait()

    # ----------------------
    # Builtins
    # ----------------------
    def _handle_builtin(self, cmd, stdout=None, append=None):
        if not cmd:
            return 0
        if cmd[0] == "cd":
            path = cmd[1] if len(cmd) > 1 else os.path.expanduser("~")
            try:
                os.chdir(path)
                self.cwd = os.getcwd()
            except Exception as e:
                print(f"cd: {e}")
            return 0
        elif cmd[0] == "pwd":
            out_stream = sys.stdout
            out_append = 'a' if append else 'w'
            if stdout is not None:
                out_stream = open(stdout, out_append)
            print(self.cwd, file=out_stream)
            return 0
        elif cmd[0] == "show":
            self.show()
            return 0
        elif cmd[0] == "exit":
            raise SystemExit(0)
        return 0


if __name__ == "__main__":

    from raw_parser import parse_raw_command
    import json
    
    execmgr = ExecutionManager()
    while True:
        try:
            command = input("volt> ")
            if command.strip() in ("exit", "quit"):
                sys.exit(0)

            # Try JSON first
            try:
                tasks = json.loads(command)
            except json.JSONDecodeError:
                tasks = parse_raw_command(command)

            execmgr.exec_tasks(tasks)

        except (EOFError, KeyboardInterrupt):
            print("\nExiting volt-shell.")
            sys.exit(0)
        except SystemExit:
            print("Goodbye.")
            sys.exit(0)