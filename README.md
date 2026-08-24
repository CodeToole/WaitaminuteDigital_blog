<div align="center">

# ⏱️ Waitaminute Digital

### Built for creators. Engineered for modern work.

The official website and portfolio platform for **Waitaminute Digital** — a Mobile, Alabama studio that
architects modern work systems: conversion-focused websites, AI & automation, and Microsoft 365–powered workflows.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.x-3366CC?style=for-the-badge&logo=htmx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Ready-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)

</div>

---

## 📖 Overview

This is the full-stack Django web application powering [waitaminutedigital.com](https://waitaminutedigital.com) — featuring a marketing site, a filterable project portfolio, a self-managed blog/CMS,
and a consultation-based lead funnel. It is configured for deployment on **Azure App Service** with **Azure Database for
PostgreSQL**, and doubles as a live demonstration of modern web solutions.

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
- ☁️ **Azure-ready deployment** — Gunicorn + WhiteNoise, environment-based config, PostgreSQL support.

---

## 🛠️ Tech Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| Language         | Python 3.14+                                 |
| Framework        | Django 6.1                                   |
| Interactivity    | HTMX                                         |
| Styling          | Hand-written CSS (brand design tokens)       |
| Database         | PostgreSQL (SQLite supported for dev)        |
| Prod server      | Gunicorn + WhiteNoise                        |
| Hosting          | Azure App Service (Linux) + Azure DB for PostgreSQL |
| Config / secrets | python-dotenv (`.env`)                       |

---

## 🗂️ Project Structure

```
.
├── waitaminute/        # Project config (settings, urls, wsgi, asgi)
├── core/               # Home, About, Contact
├── portfolio/          # Project model + HTMX tag filtering
├── blog/               # Post + Category models + HTMX live search
├── services/           # Service cards + "Book a Discovery Call"
├── leads/              # Lead capture (consultation funnel)
├── templates/          # base.html + page/error templates
├── static/             # CSS tokens, brand assets, favicons
├── docs/               # Architecture & media storage guides
├── .env.example        # Environment variable template (safe placeholders)
├── requirements.txt
└── manage.py
```

---

## 🚀 Local Setup

> **Prerequisites:** Python 3.14+, PostgreSQL or SQLite, and Git.

```bash
# 1. Clone
git clone https://github.com/CodeToole/WaitaminuteDigital_blog.git
cd WaitaminuteDigital_blog

# 2. Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Copy the template, then fill in YOUR local development values
cp .env.example .env

# 5. Set up the database & collect static files
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# 6. Run local server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** for the site and **http://127.0.0.1:8000/admin** for the CMS.

---

## 🔐 Environment Variables

All secrets live in a local `.env` file (which is **git-ignored**). Copy `.env.example` and fill in your own local values:

| Variable        | Description                                  |
| --------------- | -------------------------------------------- |
| `DJANGO_SECRET_KEY` | Django cryptographic signing key             |
| `DEBUG`         | `True` for local dev, `False` in production  |
| `ALLOWED_HOSTS` | Comma-separated hostnames                     |
| `DB_NAME`       | PostgreSQL database name                      |
| `DB_USER`       | PostgreSQL user                               |
| `DB_PASSWORD`   | PostgreSQL password                           |
| `DB_HOST`       | DB host (`localhost` for dev)                 |
| `DB_PORT`       | DB port (`5432` default)                      |
| `USE_SQLITE`    | `True` to use local SQLite database           |

> ⚠️ Never commit your real `.env`. Only `.env.example` (safe placeholders) belongs in version control.

---

## 🛡️ Security Policy

Please refer to [SECURITY.md](SECURITY.md) for details on responsible vulnerability disclosure and security guidelines.

---

## 💼 Featured Client Work

This portfolio showcases real projects delivered by Waitaminute Digital:

- 🎬 **[The Acting Collective](https://theactingcollective.vip)** — a registration & check-in platform for an in-person actor-training intensive.
- 🎤 **[Unicorn Bounty Hunters](https://unicornbountyhunters.com)** — a studio-booking and artist-roster site for an independent Mobile music collective.
- 🎶 **[Huncho Fest](https://hunchofest.com)** — the event + artist-registration site for Mobile's largest independent music festival.

---

## 🗺️ Roadmap

- [ ] Newsletter / email capture integration
- [ ] Automated lead notification workflows
- [ ] Integration with Microsoft Bookings for scheduling

---

## 📄 License

© Waitaminute Digital. All rights reserved.

---

<div align="center">

**Waitaminute Digital** · Mobile, Alabama
[Website](https://waitaminutedigital.com) · [LinkedIn](https://www.linkedin.com/in/corneliustoole/) · [GitHub](https://github.com/CodeToole)

</div>
