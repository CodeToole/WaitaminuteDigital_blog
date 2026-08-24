# Security Policy

## Reporting Security Issues

Waitaminute Digital takes the security of our application and systems seriously. If you believe you have found a security vulnerability in this repository, please report it to us responsibly.

**Please do not report security vulnerabilities through public GitHub issues, pull requests, or discussions.**

### How to Report a Vulnerability

To report a vulnerability securely:

- Please report vulnerabilities through the contact form on the official Waitaminute Digital website: [https://waitaminutedigital.com/contact/](https://waitaminutedigital.com/contact/).
- Include details of the potential vulnerability, steps to reproduce, and any relevant proof-of-concept material.
- Give us a reasonable amount of time to review and remediate the issue before making any public disclosure.

## Security Guidance for Deployments

- **Secret Keys & Environment Variables:** Ensure `DJANGO_SECRET_KEY`, database credentials, and storage keys are generated securely and kept strictly private in production environment variables. Never commit `.env` files to source control.
- **Debug Mode:** Always set `DEBUG=False` in production environments.
- **Allowed Hosts & Origins:** Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` strictly to match your verified production domains.
- **TLS/HTTPS:** Enforce HTTPS and secure cookie attributes (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`) in production settings.
