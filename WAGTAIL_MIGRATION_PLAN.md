# Wagtail Incremental Migration Plan

This plan upgrades the existing Django site to Wagtail without rebuilding the application or replacing the current PostgreSQL-backed architecture.

## Scope and constraints

- Keep the current project structure and custom Django apps in place.
- Preserve all existing PostgreSQL data and existing app tables.
- Keep Blog and Portfolio operating as they are during the migration.
- Convert the Home, Services, and About marketing pages into Wagtail Page models with StreamField blocks.
- Keep Wagtail admin available inside the same deployment for marketing content changes.
- Prepare final deployment steps for Azure App Service.

## Phase 1: install Wagtail without disturbing the current app

1. Add Wagtail to the existing dependency set in `requirements.txt`.
2. Add Wagtail apps and middleware to `waitaminute/settings.py`.
3. Add Django sites support and Wagtail site configuration.
4. Add Wagtail admin/document URLs and keep the existing app URLs for Blog and Portfolio.
5. Do not delete or rewrite the current `blog`, `portfolio`, or `leads` apps.

Example dependency additions:

```bash
pip install "wagtail>=6.3,<8"
```

In practice, lock the exact version that matches the current Django baseline in Azure before you deploy.

## Phase 2: add a dedicated marketing app

Create a new app named `marketing` and keep it side-by-side with `core`, `blog`, `portfolio`, and `services`.

Required files:

- `marketing/apps.py`
- `marketing/blocks.py`
- `marketing/models.py`
- `templates/blocks/*.html`
- `templates/marketing/*.html`

This app owns:

- `HomePage`
- `ServicesPage`
- `AboutPage`

Each page uses `StreamField` so marketing content can be edited in Wagtail Admin.

## Phase 3: block model design

Use `StreamField` blocks for these content sections:

- Hero sections
- Service cards
- Call-to-action sections
- Rich content areas

Recommended block structure:

```python
class PageStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    service_cards = ServiceCardsBlock()
    cta = CTASectionBlock()
    rich_content = RichContentBlock()
```

This keeps the marketing pages flexible while staying compatible with the current site architecture.

## Phase 4: preserve DB data and existing app functionality

1. Keep the existing `blog.models.Post` and `portfolio.models.Project` models untouched.
2. Continue using the current PostgreSQL database for all existing tables.
3. Do not do a destructive migration or replace Blog/Portfolio tables with Wagtail Page models.
4. On the homepage and landing pages, pull the latest blog posts and featured portfolio items from the existing Django models.
5. This preserves live production data while letting Wagtail manage the marketing copy and layout.

## Phase 5: migration commands

Run migrations in the current environment with the existing database connection string:

```bash
python manage.py makemigrations marketing
python manage.py migrate
python manage.py createcachetable  # optional if cache is used
```

If the app is already deployed in Azure, run the same migration against the staging database first, then back up and promote the production DB.

## Phase 6: create the Wagtail site structure

Create the Wagtail Site record and assign the root page to the new `HomePage` object.

Recommended site setup:

- Site name: `Waitaminute Digital`
- Hostname: production domain + Azure App Service hostname
- Root page: `HomePage`

Then add child pages:

- Home
- Services
- About

Set slugs to `home`, `services`, and `about` to match the public URLs.

## Phase 7: Azure App Service deployment

### Required App Service settings

Add these environment variables in Azure App Service Configuration:

```text
DJANGO_SECRET_KEY=<your secret>
DEBUG=False
ALLOWED_HOSTS=waitaminutedigital.com,www.waitaminutedigital.com,waitaminutedigitalpy-<app-name>.azurewebsites.net
PUBLIC_SITE_URL=https://waitaminutedigital.com
DB_NAME=<postgres-db-name>
DB_USER=<postgres-user>
DB_PASSWORD=<postgres-password>
DB_HOST=<db-hostname>
DB_PORT=5432
```

### Build and deploy

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

Use the App Service startup command:

```bash
gunicorn waitaminute.wsgi:application --bind 0.0.0.0:8000
```

### Important checks after deploy

1. Confirm `/admin` still works for the Django admin.
2. Confirm `/cms` works for Wagtail Admin.
3. Confirm `/blog/` and `/portfolio/` still work.
4. Confirm `/`, `/services/`, and `/about/` render from the Wagtail page tree.
5. Confirm PostgreSQL data remained intact.

## Rollback strategy

- Keep the existing custom home/services/about templates until the Wagtail pages are verified in staging.
- Use a blue/green or staging slot in Azure to validate the Wagtail page tree before making it live.
- Do not remove the legacy Django views until the production site has been validated.

## Deployment recommendation

Use a staged deployment:

1. Ship Wagtail into the current app and run migrations in Azure staging.
2. Create the Wagtail `HomePage`, `ServicesPage`, and `AboutPage` entries.
3. Populate content in Wagtail Admin.
4. Validate URLs, images, and admin editing.
5. Promote the staged deployment to production.

This approach is the safest incremental upgrade because it preserves PostgreSQL data, leaves the existing Django apps intact, and gives the marketing team a real Wagtail editor without a full site rebuild.
