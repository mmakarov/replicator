# Security Policy

## Supported Versions

Replicator is distributed as a self-contained Windows archive. Only the latest
GitHub Release is supported. Older releases are kept for reference and do not
receive fixes.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| Older releases | No |

## Reporting a Vulnerability

Please report security issues privately using GitHub's
[private vulnerability reporting](https://github.com/mmakarov/replicator/security/advisories/new).
Do **not** open a public issue for a vulnerability.

Include, if possible:

- a description of the issue and its impact;
- steps to reproduce;
- the affected file or command;
- the Replicator version or release tag.

You can expect an initial acknowledgement within a few days. Once the issue is
confirmed and fixed, a new release will be published and the report credited
unless you prefer to stay anonymous.

## Scope

Replicator runs locally and processes user-selected media files with `ffmpeg`.
Relevant reports include, for example, unsafe handling of file paths or
arguments passed to `ffmpeg`, or unexpected code execution from crafted inputs.
Issues that require an already-compromised machine or intentionally malicious
local configuration are generally out of scope.
