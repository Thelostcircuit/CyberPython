# 23 // SHELL GAME

```
[PYTHIA-9] external tools: cam_loop (C, 2080) ── liftctl.sh ── doorfw (firmware CLI) ── trust: LOW
```

**Modules:** `subprocess`, `signal`, `os` processes, `platform`, `errno`, `mmap`, `select`, `pty`, `tty`, `termios`, `fcntl`, `resource`, `pwd`, `grp`, `posix`

Three of the swarm's workers are other people's programs, and each has its own quirks. The
camera looper sometimes hangs forever. The door firmware tool writes errors to the wrong
stream. The lift script needs its input piped in, and exits with code 3 when the lift is
busy.

> **MONTY:** Python is a superb *conductor* of other programs. `subprocess` starts them and
> talks to them. `signal` lets you ask them to stop, or be asked yourself. And a handful of
> Unix modules let you get right down to the operating system: file descriptors, memory-mapped
> files, users and groups, resource limits. On this job we control the OS, rather than the
> other way round.

---

## ▓ TECH BRIEFING

### `subprocess.run`: the workhorse

```python
import subprocess, sys
r = subprocess.run(["liftctl", "status"], capture_output=True, text=True)
r.returncode, r.stdout, r.stderr

subprocess.run(cmd, input="floor -6\n", capture_output=True, text=True)   # feed stdin
subprocess.run(cmd, timeout=5)          # raises subprocess.TimeoutExpired (and kills the child)
subprocess.run(cmd, check=True)         # raises CalledProcessError on a non-zero exit
subprocess.run(cmd, cwd="/tmp", env={**os.environ, "MODE": "quiet"})
subprocess.run([sys.executable, "-c", "print(1)"])    # run Python itself, portably
```

**Pass a list of arguments, not a string, and avoid `shell=True`.** With a list, every
argument arrives exactly as given, so untrusted text can't turn into shell syntax. If you
really need a shell, build the line with `shlex.quote` (ch 21).

### `subprocess.Popen`: full control

```python
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
for line in p.stdout:              # read output as it arrives
    ...
p.wait(timeout=5); p.poll()        # poll: None while still running
p.terminate(); p.kill(); p.send_signal(signal.SIGUSR1)

a = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
b = subprocess.Popen(cmd2, stdin=a.stdout, stdout=subprocess.PIPE)   # a pipeline: cmd1 | cmd2
a.stdout.close(); out, _ = b.communicate()
```

`communicate()` sends input and reads all output without deadlocking on full pipes.
`subprocess.DEVNULL` discards output, and `stderr=subprocess.STDOUT` merges the two streams.

### `signal`

```python
import signal
def on_term(signum, frame):
    print("cleaning up"); raise SystemExit(0)
old = signal.signal(signal.SIGTERM, on_term)     # install; returns the previous handler
signal.signal(signal.SIGTERM, old)               # restore
signal.Signals(15).name                          # 'SIGTERM'
os.kill(pid, signal.SIGTERM)
signal.alarm(5)                                  # Unix: SIGALRM in 5 s
```

Handlers run in the main thread, between bytecodes. Keep them tiny. `SIGKILL` can't be caught.

### `os` process tools, `errno`, `platform`

```python
os.getpid(), os.getppid(), os.cpu_count(), os.getloadavg(), os.uname()
os.environ, os.putenv, os.kill(pid, sig), os.waitpid(pid, 0)
os.pipe(), os.read(fd, n), os.write(fd, b), os.close(fd), os.isatty(fd)

import errno
errno.ENOENT, errno.errorcode[2], os.strerror(2)     # 'ENOENT', 'No such file or directory'
# OSError subclasses map to errnos: FileNotFoundError ↔ ENOENT, PermissionError ↔ EACCES...

import platform
platform.system(), platform.release(), platform.machine(), platform.python_version()
platform.freedesktop_os_release()                  # Linux distro info
```

On Unix, `os` is built on the `posix` module (on Windows, `nt`). Always import `os`.

### Low-level I/O: `select`, `mmap`, `fcntl`

```python
import select
readable, _, _ = select.select([fd], [], [], 1.0)   # wait up to 1 s for fd to have data
# select.poll / epoll / kqueue for many fds;  `selectors` (ch 25) wraps them nicely

import mmap
with open(path, "r+b") as f, mmap.mmap(f.fileno(), 0) as m:
    m[0:4] = b"OURO"          # edit the file like a bytearray, in place
    m.find(b"rack")

import fcntl                   # Unix: file-descriptor flags and advisory locks
flags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)   # reads now raise BlockingIOError instead of waiting
fcntl.flock(f, fcntl.LOCK_EX)                           # exclusive advisory lock
```

### Unix accounts, limits, and terminals

```python
import pwd, grp, resource
pwd.getpwuid(os.getuid()).pw_name      # user name;   .pw_dir home, .pw_shell
grp.getgrgid(os.getgid()).gr_name      # group name
resource.getrlimit(resource.RLIMIT_NOFILE)     # (soft, hard) max open files
resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
```

`pty` runs programs in a pseudo-terminal (`pty.spawn`), so they think a human is typing.
`termios` reads and sets terminal attributes (echo, line buffering), and `tty.setraw(fd)` /
`tty.setcbreak(fd)` are shortcuts for turning on character-at-a-time input. That's how
`getpass` hides your typing.

---

## ▓ THE JOB

Unix-only parts are skipped on Windows. In `job.py`:

1. **`run_tool(args, stdin_text=None)`**: `(returncode, stdout, stderr)` as text.
2. **`run_or_timeout(args, seconds)`**: stdout, or the string `"TIMEOUT"`.
3. **`checked_output(args)`**: stdout, raising `CalledProcessError` on failure.
4. **`pipe(first, second)`**: `first | second` with two `Popen`s, returning the second's stdout.
5. **`live_lines(args)`**: a generator of output lines as the child produces them.
6. **`stop_politely(proc, grace)`**: `terminate()`, wait `grace` seconds, `kill()` if it's still alive. Return the exit code.
7. **`trap(signum, log)`**: install a handler that appends the signal's *name* to `log`. Return the previous handler.
8. **`explain_errno(code)`**: `"ENOENT: No such file or directory"`.
9. **`machine_report()`**: a few `platform` facts.
10. **`patch_file(path, offset, data)`**: edit a file in place through `mmap`.
11. **`owner_and_group(path)`**: names via `pwd`/`grp`.
12. **`nonblocking_pipe()`**: an `os.pipe()` whose read end is set non-blocking with `fcntl`.
13. **`wait_readable(fd, timeout)`**: `select`.
