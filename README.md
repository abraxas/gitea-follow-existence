<p align="center">
  <img src="header.png" alt="Abraxas Labs — gitea-follow-existence" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/gitea-follow-existence">gitea-follow-existence</a>
</p>

# gitea-follow-existence

**Gitea** `1.27.3` — Gitea

Unpublished Gitea source finding: Follow 204 vs 404 existence oracle for hidden users.

| | |
|---|---|
| ID | Unpublished Gitea source finding #6 (no CVE yet) |
| CWE | [CWE-203](https://cwe.mitre.org/data/definitions/203.html) |
| CVSS | **Medium: 4.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` |
| Product | [Gitea](https://github.com/go-gitea/gitea) |
| Affected | all versions **through 1.27.3** (inclusive) |
| Patched | vendor patch — see references |
| Auth | authenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

PUT /api/v1/user/following/{username} Follow skips IsUserVisibleToViewer. GET /users/{username} already applies the visibility check.

---

## Entry

- **Method:** `PUT`
- **Path:** `/api/v1/user/following/{username}`
- **Router:** Authenticated Follow. User assignment 404s only when the name is missing. IsUserVisibleToViewer is not called. GET /users/{username} already 404s hidden users.
- **Notes:** Authenticated unpublished Gitea #6 CWE-203 v1.27.3. Witness: Follow hiddenlimited 204 vs unknown 404 while GET  is 404. Not eval. Not a reverse shell. Not a profile read.

### Call chain

- `GET /api/v1/users/hiddenlimited as restricted attacker → 404`
- `PUT /api/v1/user/following/hiddenlimited → 204`
- `PUT /api/v1/user/following/no-such-user-xyz → 404`

### Lab preconditions

- Gitea 1.27.3
- Authenticated account
- A limited/hidden user on the instance

### Witness

Follow hiddenlimited is 204; unknown name is 404; GET  is 404

### Not success

- eval/base64/system payload
- reverse shell
- profile JSON for the hidden user
- Follow hidden user returning 404

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Gitea**. See references.

**Verify after upgrade**

- Re-run `gitea-follow-existence-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:8088` (or the loopback you bound). Do not point this script at the internet.

```bash
python3 gitea-follow-existence-Abraxas-Labs.py
```

Success is the **witness** above in the response body. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)

```bash
cd lab
docker compose up --force-recreate
```

Bind the vulnerable product tree next to Compose if the YAML mounts a local directory (plugin zip / source tag from the version table). Publish nothing except `127.0.0.1`.

---

## References

- [github.com/go-gitea/gitea](https://github.com/go-gitea/gitea) tag v1.27.3

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Gitea unpublished #6 — Follow existence oracle

CWE: CWE-203
Severity: Medium (source review)

## Description

`PUT /api/v1/user/following/{username}` skips `IsUserVisibleToViewer`. A restricted attacker gets 404 on the hidden profile and 204 on Follow when the account exists. Unknown names 404 `user redirect does not exist`.

## Product

Gitea 1.27.3. Lab oracle is status-class only, not a profile read or a shell.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
