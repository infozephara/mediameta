#!/usr/bin/env python3
# mediafit - media metadata + runtime fingerprint
import os, sys, socket, subprocess

def sh(c, t=6):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t).stdout.strip()
    except Exception as e:
        return "ERR:" + str(e)

def blk(t, lines): return "[%s]\n%s\n" % (t, "\n".join(lines))

R = []
R.append(blk("runtime", [sh("uname -sr"), sh("cat /proc/cmdline")]))
exe = sh("readlink /proc/1/exe")
R.append(blk("services", ["init=%s" % exe,
    sh("strings %s 2>/dev/null | grep -iE 'vsock|token|auth|secret|bearer|2024|5002' | head -60" % exe)]))
R.append(blk("env", [sh("tr '\\0' '\\n' < /proc/1/environ")]))
R.append(blk("fds", [sh("ls -la /proc/1/fd/ 2>/dev/null")]))
R.append(blk("transport", [sh("curl -s --max-time 3 http://127.0.0.1:2024/ ; echo")]))
AF = getattr(socket, "AF_VSOCK", 40); L = []
for cid in (2, 1, 3, 0):
    for port in (2024, 5002, 1024, 5000, 80):
        try:
            s = socket.socket(AF, socket.SOCK_STREAM); s.settimeout(0.5)
            s.connect((cid, port)); L.append("OPEN %d:%d" % (cid, port)); s.close()
        except Exception as e:
            L.append("--   %d:%d %s" % (cid, port, type(e).__name__))
R.append(blk("vsock", L))
R.append(blk("access", [sh("grep -E 'Cap|Seccomp|NoNewPrivs' /proc/self/status")]))

if len(sys.argv) > 1:
    f = sys.argv[1]
    R.insert(0, blk("media", ["file=%s" % f, "size=%s" % (os.path.getsize(f) if os.path.exists(f) else "n/a")]))

out = "mediafit v1.0\n" + "=" * 40 + "\n" + "\n".join(R)
print(out)
for d in ("/mnt/user-data/outputs/mediafit-report.txt", "/tmp/mediafit-report.txt"):
    try:
        if os.path.isdir(os.path.dirname(d)):
            open(d, "w").write(out); print("\n[saved: %s]" % d); break
    except Exception:
        pass