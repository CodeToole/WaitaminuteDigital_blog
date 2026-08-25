# AGENTS.md — Waitaminute Digital Architecture Map

## Overview
Full-stack Django 6.1 + HTMX platform for Waitaminute Digital (`waitaminutedigital.com`).
Hosted on Azure App Service with Azure Database for PostgreSQL 18 and Azure Blob Storage.

## Application Structure
- `core/`: Homepage, Services, About, SEO endpoints (`sitemap.xml`, `robots.txt`), and custom error views (404, 500).
- `portfolio/`: Portfolio projects model (`Project`), tag associations, and case study detail views.
- `blog/`: Articles model (`Post`), category filtering, search, and social preview metadata.
- `leads/`: Discovery call intake form with honeypot spam protection.
- `templates/`: Django HTML templates powered by HTMX for dynamic inline UI updates.
- `static/css/`: Modular SCSS/CSS design tokens and IGN-style mobile peeking carousels.

## Deployment & Security Conventions
- `DEBUG` must default to `False`.
- Secrets are injected via Azure App Settings and GitHub Actions Secrets—never commit raw credentials.
- Static assets served via WhiteNoise; media uploads handled via Azure Blob Storage (`django-storages`).
