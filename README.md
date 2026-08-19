<div align="center">

# ⏱️ Waitaminute Digital

### Built for creators. Engineered for modern work.

The official website and portfolio platform for **Waitaminute Digital** — a Mobile, Alabama studio that
architects modern work systems: conversion-focused websites, AI & automation, and Microsoft 365–powered workflows.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-latest-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.x-3366CC?style=for-the-badge&logo=htmx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Ready-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)

</div>

---

## 📖 Overview

This is the ground-up rebuild of [waitaminutedigital.com](https://waitaminutedigital.com) — a full-stack
Django web application featuring a marketing site, a filterable project portfolio, a self-managed blog/CMS,
and a consultation-based lead funnel. It's designed to run on **Azure App Service** with **Azure Database for
PostgreSQL**, and it doubles as a live demonstration of the modern-work solutions the studio builds for clients.

**Designed & built by [Cornelius "Neil" Toole](https://www.linkedin.com/in/corneliustoole/)** — Founder & Lead
AI Collaborator, Waitaminute Digital.

---

## ✨ Features

- 🎨 **Custom brand design system** — dark-first UI with a neon cyan → electric purple palette, hand-written CSS tokens (no framework bloat), Space Grotesk / Inter / Space Mono typography.
- 🧩 **Interactive without a JS framework** — HTMX powers live portfolio **tag filtering**, blog **live search**, and inline **form submits** with zero page reloads.
- 📝 **Self-managed blog / CMS** — post articles and news straight from the Django admin (drafts vs. published, categories, cover images).
- 💼 **Filterable project portfolio** — real case studies with tag facets (Web · Brand · Strategy · Automation) and detail pages.
- 📞 **Consult-first lead funnel** — no public pricing; a "Book a Discovery Call" flow captures leads into the database for follow-up and custom quoting.
- 🔎 **SEO-ready** — per-page meta + Open Graph tags, `sitemap.xml`, `robots.txt`, canonical URLs.
- 🤖 **Branded error pages** — custom 404 / 500 featuring the studio mascot.
- ☁️ **Azure-ready deployment** — Gunicorn + WhiteNoise, environment-based config, PostgreSQL in every environment.

---

## 🛠️ Tech Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| Language         | Python 3.14+                                 |
| Framework        | Django (latest LTS)                          |
| Interactivity    | HTMX                                         |
| Styling          | Hand-written CSS (brand design tokens)       |
| Database         | PostgreSQL                                   |
| Prod server      | Gunicorn + WhiteNoise                        |
| Hosting          | Azure App Service (Linux) + Azure DB for PostgreSQL |
| Config / secrets | python-dotenv (`.env`)                       |

---

## 🗂️ Project Structure

```
waitaminute_digitalpydock/
├── waitaminute/        # Project config (settings, urls, wsgi)
├── core/               # Home, About, Contact
├── portfolio/          # Project model + HTMX tag filtering
├── blog/               # Post + Category models + HTMX live search
├── services/           # Service cards + "Book a Discovery Call"
├── leads/              # Lead capture (consultation funnel)
├── templates/          # base.html + page/error templates
├── static/             # CSS tokens, brand assets, favicons
├── .env.example        # Environment variable template (safe to share)
├── requirements.txt
└── manage.py
```

---

## 🚀 Local Setup

> **Prerequisites:** Python 3.14+, PostgreSQL running locally, and Git.

```bash
# 1. Clone
git clone https://github.com/CodeToole/WaitaminuteDigital_blog.git
cd WaitaminuteDigital_blog

# 2. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
#    Copy the template, then fill in YOUR real values (secret key, DB creds)
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux

# 5. Set up the database
python manage.py migrate
python manage.py createsuperuser

# 6. Run it
python manage.py runserver
```

Visit **http://127.0.0.1:8000** for the site and **http://127.0.0.1:8000/admin** for the CMS.

---

## 🔐 Environment Variables

All secrets live in a local `.env` file (which is **git-ignored**). Copy `.env.example` and fill in your own values:

| Variable        | Description                                  |
| --------------- | -------------------------------------------- |
| `SECRET_KEY`    | Django cryptographic signing key             |
| `DEBUG`         | `True` for local dev, `False` in production  |
| `ALLOWED_HOSTS` | Comma-separated hostnames                     |
| `DB_NAME`       | PostgreSQL database name                      |
| `DB_USER`       | PostgreSQL user                               |
| `DB_PASSWORD`   | PostgreSQL password                           |
| `DB_HOST`       | DB host (`localhost` for dev)                 |
| `DB_PORT`       | DB port (`5432` default)                      |

> ⚠️ Never commit your real `.env`. Only `.env.example` (placeholders) belongs in version control.

---

## 💼 Featured Client Work

This portfolio showcases real projects delivered by Waitaminute Digital:

- 🎬 **[The Acting Collective](https://theactingcollective.vip)** — a registration & check-in platform for an in-person actor-training intensive (Ziare Perryman).
- 🎤 **[Unicorn Bounty Hunters](https://unicornbountyhunters.com)** — a studio-booking and artist-roster site for an independent Mobile music collective.
- 🎶 **[Huncho Fest](https://hunchofest.com)** — the event + artist-registration site for Mobile's largest independent music festival.

---

## 🗺️ Roadmap

- [ ] Newsletter / email capture integration
- [ ] Optional Wagtail CMS upgrade for visual, drag-and-edit content editing
- [ ] Azure Communication Services email notifications on new leads
- [ ] Microsoft Bookings link on the consultation success screen

---

## 📄 License

© 2026 Waitaminute Digital. All rights reserved.

---

<div align="center">

**Waitaminute Digital** · Mobile, Alabama
[Website](https://waitaminutedigital.com) · [LinkedIn](https://www.linkedin.com/in/corneliustoole/) · [GitHub](https://github.com/CodeToole)

</div>
