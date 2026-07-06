# Security Policy

## Reporting a vulnerability

If you find a security issue, please **do not open a public issue**. Email **narayancoding@gmail.com** with a description and steps to reproduce. You can expect an acknowledgement within a few days.

## Notes

- Never commit credentials or API keys; use environment variables or local config excluded from git.
- Dependency vulnerability reports (see `requirements.txt` where present) are welcome.

## API keys

This app uses a Google Gemini API key. Load it from the environment (never hard-code it), and rotate it immediately if it is ever exposed.
