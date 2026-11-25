#!/usr/bin/env python3
"""
fetch_tool.py: download a pinned, checksum-verified copy of a scanning tool into a private folder.

What it does
  Downloads one tool from its official GitHub release, at the version pinned
  below, checks the file's SHA-256 fingerprint against the one we recorded
  (copied from the maker's published checksums), and only then unpacks it into
  the folder you choose. If the fingerprint doesn't match, it deletes the
  download and stops. Nothing is installed system-wide. No admin rights. No sudo.

Tools (open licences only)
  gitleaks     8.30.1   MIT          finds passwords and keys in folders and code
  osv-scanner  2.6.0    Apache-2.0   finds known holes in code building blocks
  gam          7.48.24  Apache-2.0   Google Workspace read-only reports (macOS builds only here)

What it touches
  github.com release downloads, and the folder you name (default
  ~/FounderOS-security-tools). Standard library only.

Usage
  python3 -I fetch_tool.py gitleaks
  python3 -I fetch_tool.py osv-scanner --dest ~/FounderOS-security-tools
  python3 -I fetch_tool.py --list

Updating a pin: copy the new version and SHA-256 from the maker's checksums file
on the release page (never from anywhere else), test it, then commit.

Part of the Founder OS security module (Driven Young).
"""
import argparse
import hashlib
import os
import platform
import shutil
import ssl
import stat
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

PINS = {
    "gitleaks": {
        "version": "8.30.1",
        "url": "https://github.com/gitleaks/gitleaks/releases/download/v{v}/{f}",
        "files": {
            ("Darwin", "arm64"): ("gitleaks_8.30.1_darwin_arm64.tar.gz", "b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5"),
            ("Darwin", "x86_64"): ("gitleaks_8.30.1_darwin_x64.tar.gz", "dfe101a4db2255fc85120ac7f3d25e4342c3c20cf749f2c20a18081af1952709"),
            ("Linux", "x86_64"): ("gitleaks_8.30.1_linux_x64.tar.gz", "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"),
            ("Linux", "aarch64"): ("gitleaks_8.30.1_linux_arm64.tar.gz", "e4a487ee7ccd7d3a7f7ec08657610aa3606637dab924210b3aee62570fb4b080"),
            ("Windows", "AMD64"): ("gitleaks_8.30.1_windows_x64.zip", "d29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e"),
        },
        "binary": "gitleaks",
    },
    "osv-scanner": {
        "version": "2.6.0",
        "url": "https://github.com/google/osv-scanner/releases/download/v{v}/{f}",
        "files": {
            ("Darwin", "arm64"): ("osv-scanner_darwin_arm64", "98c460dcd37de25819babd757d04542045b6243113e209edcd4d89fedb0256b4"),
            ("Darwin", "x86_64"): ("osv-scanner_darwin_amd64", "60c5296637e977b28eeda5c7f13573e447659a632922737f94d11fa7e30ad6ca"),
            ("Linux", "x86_64"): ("osv-scanner_linux_amd64", "ca69b3d3cd08f889a49dc0a383122f71cc528b83803671df5fd874d97485b108"),
            ("Linux", "aarch64"): ("osv-scanner_linux_arm64", "2c71403eb443d05891c4f268c3ad771cf4f16e5443463fd7851ef8f454d3c7e4"),
            ("Windows", "AMD64"): ("osv-scanner_windows_amd64.exe", "e0ed7644118b717b028c249ee9d3515024e55e8510747ca08906eb96765354d6"),
        },
        "binary": "osv-scanner",
    },
    "gam": {
        "version": "7.48.24",
        "url": "https://github.com/GAM-team/GAM/releases/download/v{v}/{f}",
        "files": {
            ("Darwin", "arm64"): ("gam-7.48.24-macos26.6-arm64.tar.xz", "c342b1bce931cecb55526b7efbea6dfe5bb1078733f8bc386db171d9e2dfa821"),
            ("Darwin", "x86_64"): ("gam-7.48.24-macos26.6-x86_64.tar.xz", "991d6030ed6e3680589dcb9e151c01f9b67610e9f686ac8703d481adfbd6d97d"),
        },
        "binary": "gam7/gam",
        "note": "Built for macOS 26. On macOS 15 use the macos15.7 file from the same release page (check its fingerprint there).",
    },
}


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "FounderOS-security-check/1.0"})
    for cafile in (None, "/etc/ssl/cert.pem"):
        if cafile and not os.path.exists(cafile):
            continue
        try:
            ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r, open(path, "wb") as out:
                shutil.copyfileobj(r, out)
            return
        except urllib.error.URLError as e:
            if cafile is None and "CERTIFICATE_VERIFY_FAILED" in str(e):
                continue
            raise


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(archive, dest):
    """Unpack without letting any file land outside dest."""
    dest_real = os.path.realpath(dest)
    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            for m in z.namelist():
                if not os.path.realpath(os.path.join(dest, m)).startswith(dest_real + os.sep):
                    raise RuntimeError("unsafe path in archive: " + m)
            z.extractall(dest)
    else:
        with tarfile.open(archive) as t:
            members = []
            for m in t.getmembers():
                if m.issym() or m.islnk() or m.isdev():
                    continue  # skip links and device files entirely
                if not os.path.realpath(os.path.join(dest, m.name)).startswith(dest_real + os.sep):
                    raise RuntimeError("unsafe path in archive: " + m.name)
                members.append(m)
            if sys.version_info >= (3, 12):
                t.extractall(dest, members=members, filter="data")
            else:
                t.extractall(dest, members=members)


def main():
    ap = argparse.ArgumentParser(description="Download a pinned, checksum-verified tool into a private folder")
    ap.add_argument("tool", nargs="?", choices=sorted(PINS))
    ap.add_argument("--dest", default=os.path.expanduser("~/FounderOS-security-tools"))
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.tool:
        for k, v in PINS.items():
            print(f"{k} {v['version']}: " + ", ".join(f"{o}/{m}" for o, m in v["files"]))
        return 0
    pin = PINS[a.tool]
    key = (platform.system(), platform.machine())
    if key not in pin["files"]:
        print(f"No pinned build of {a.tool} for {key}. Install it by hand from the official release page and check its fingerprint.")
        return 1
    fname, want = pin["files"][key]
    dest = os.path.join(os.path.expanduser(a.dest), f"{a.tool}-{pin['version']}")
    os.makedirs(dest, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = os.path.join(td, fname)
        url = pin["url"].format(v=pin["version"], f=fname)
        print(f"Downloading {fname} from the official release...")
        download(url, tmp)
        got = sha256(tmp)
        if got != want:
            print(f"STOP: fingerprint doesn't match.\n  expected {want}\n  got      {got}\nNothing was installed.")
            return 2
        print("Fingerprint matches the maker's published checksum.")
        if fname.endswith((".tar.gz", ".tar.xz", ".zip")):
            safe_extract(tmp, dest)
        else:
            out = os.path.join(dest, pin["binary"] + (".exe" if fname.endswith(".exe") else ""))
            shutil.copy2(tmp, out)
    binpath = os.path.join(dest, pin["binary"] + (".exe" if key[0] == "Windows" else ""))
    if os.path.exists(binpath):
        os.chmod(binpath, os.stat(binpath).st_mode | stat.S_IXUSR)
    print(f"Ready: {binpath}")
    if pin.get("note"):
        print("Note: " + pin["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
