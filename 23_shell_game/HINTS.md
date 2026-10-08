# HINTS // 23 SHELL GAME

## run_tool / run_or_timeout / checked_output
<details><summary>Hint</summary>

`subprocess.run(args, input=stdin_text, capture_output=True, text=True)`. Add `timeout=` and
catch `subprocess.TimeoutExpired`, or add `check=True` and let `CalledProcessError` escape.
</details>

## pipe
<details><summary>Hint</summary>

```python
a = subprocess.Popen(first, stdout=subprocess.PIPE)
b = subprocess.Popen(second, stdin=a.stdout, stdout=subprocess.PIPE, text=True)
a.stdout.close()          # so `a` gets SIGPIPE if `b` exits early
out, _ = b.communicate()
a.wait()
```
</details>

## live_lines
<details><summary>Hint</summary>

`with subprocess.Popen(args, stdout=subprocess.PIPE, text=True) as proc:` then
`for line in proc.stdout: yield line.rstrip("\n")`. Leaving the `with` waits for the process.
</details>

## stop_politely
<details><summary>Hint</summary>

`proc.terminate()`, then `try: return proc.wait(timeout=grace)`, and
`except subprocess.TimeoutExpired: proc.kill(); return proc.wait()`. On Unix, death by signal
N gives a return code of `-N`.
</details>

## trap
<details><summary>Hint</summary>

The handler takes `(signum, frame)`. `signal.signal(...)` returns the old handler, so return
that.
</details>

## explain_errno
<details><summary>Hint</summary>

`errno.errorcode[code]` gives the symbolic name, and `os.strerror(code)` gives the message.
</details>

## patch_file
<details><summary>Hint</summary>

`with open(path, "r+b") as f, mmap.mmap(f.fileno(), 0) as m:`. Check
`offset + len(data) > len(m)`, then slice-assign `m[offset:offset + len(data)] = data`.
</details>

## owner_and_group / nonblocking_pipe / wait_readable
<details><summary>Hint</summary>

`pwd.getpwuid(st.st_uid).pw_name` and `grp.getgrgid(st.st_gid).gr_name`.
`fcntl.fcntl(r, fcntl.F_SETFL, fcntl.fcntl(r, fcntl.F_GETFL) | os.O_NONBLOCK)`.
`readable, _, _ = select.select([fd], [], [], timeout)`.
</details>
