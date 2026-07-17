# Security Policy

## Supported Versions

This project is under active development. Security fixes are applied to the
latest version on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| main    | ✅                  |

## Reporting a Vulnerability

DocFlow AI is designed to run 100% locally — it does not send data to any
external service by default. However, if you discover a security
vulnerability (e.g., in file handling, dependency versions, or the local API
surface), please report it responsibly:

1. **Do not open a public GitHub issue** for security vulnerabilities.
2. Email the maintainer directly at **mirajgaonkarshaunak@gmail.com** with:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
3. You can expect an initial response within a few days.

## Scope

Because this application runs locally and processes user-uploaded documents,
please pay particular attention to:

- Path traversal or unsafe file handling during upload/processing
- Injection risks in document parsing (OCR, Tika, DOCX/XLSX parsing)
- Dependency vulnerabilities (`pip audit` is recommended periodically)

## Local-First Design Note

By default, this project makes **no external network calls** for AI
inference (Ollama runs locally) or embeddings (sentence-transformers runs
on-device). Model weights are downloaded once from Hugging Face / Ollama's
registry on first use. If you modify the code to call external APIs, please
clearly document that change, as it alters the project's privacy guarantees.
