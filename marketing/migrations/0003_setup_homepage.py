import json
from django.db import migrations


def get_default_homepage_body():
    return [
        {
            "type": "hero",
            "value": {
                "eyebrow": "Built for creators. Engineered for modern work.",
                "title": "We architect modern work systems that turn effort into momentum.",
                "subtitle": "Waitaminute Digital helps founders and teams modernize their web presence, automate operations, and turn customer interest into qualified follow-up.",
                "primary_cta_label": "Book a Discovery Call",
                "primary_cta_url": "/services/#consultation",
                "secondary_cta_label": "Explore services",
                "secondary_cta_url": "/services/",
                "micro_points": [
                    "Azure-ready builds",
                    "Microsoft 365 + Copilot workflows",
                    "Conversion-first design",
                ],
                "badge_text": "Modern Work",
            },
        },
        {
            "type": "service_cards",
            "value": {
                "eyebrow": "Services",
                "heading": "What we build for ambitious teams.",
                "intro": "",
                "cards": [
                    {
                        "kicker": "01",
                        "title": "Modern Work Websites",
                        "description": "High-converting websites designed around clarity, authority, and action.",
                        "link_url": "/services/",
                        "icon": "",
                    },
                    {
                        "kicker": "02",
                        "title": "AI & Automation",
                        "description": "Copilot Studio, Power Automate, and workflow design that removes repetitive work.",
                        "link_url": "/services/",
                        "icon": "",
                    },
                    {
                        "kicker": "03",
                        "title": "Website-as-a-Service",
                        "description": "Ongoing design and optimization for teams that need their digital presence to evolve.",
                        "link_url": "/services/",
                        "icon": "",
                    },
                ],
            },
        },
        {
            "type": "portfolio_highlights",
            "value": {
                "eyebrow": "Featured work",
                "heading": "Systems that bring structure to creative momentum.",
                "intro": "",
                "show_dynamic_projects": True,
                "cards": [
                    {
                        "title": "Brand architecture",
                        "summary": "Messaging and customer journey aligned with a sharper digital story.",
                        "gradient_class": "gradient-one",
                        "link_url": "/portfolio/",
                    },
                    {
                        "title": "AI workflows",
                        "summary": "Automations that reduce admin friction without losing the human touch.",
                        "gradient_class": "gradient-two",
                        "link_url": "/portfolio/",
                    },
                    {
                        "title": "Marketing systems",
                        "summary": "Web experiences that convert attention into conversations and pipeline.",
                        "gradient_class": "gradient-three",
                        "link_url": "/portfolio/",
                    },
                ],
            },
        },
        {
            "type": "insights",
            "value": {
                "eyebrow": "Insights",
                "heading": "Practical perspectives for modern operators.",
                "show_dynamic_posts": True,
            },
        },
        {
            "type": "cta",
            "value": {
                "eyebrow": "Let’s talk",
                "heading": "Tell us what you’re building.",
                "body": "",
                "button_label": "Book a Discovery Call",
                "button_url": "/services/#consultation",
            },
        },
        {
            "type": "footer",
            "value": {
                "brand_name": "WAITAMINUTE",
                "tagline": "Built for creators. Engineered for modern work.",
                "email": "hello@waitaminutedigital.com",
                "contact_link_label": "Tell us what you're building",
                "contact_link_url": "/services/#consultation",
                "nav_links": [
                    {"label": "Services", "url": "/services/"},
                    {"label": "Portfolio", "url": "/portfolio/"},
                    {"label": "Blog", "url": "/blog/"},
                    {"label": "About", "url": "/about/"},
                ],
                "copyright": "Waitaminute Digital. All rights reserved.",
            },
        },
    ]


def setup_wagtail_homepage(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Page = apps.get_model("wagtailcore", "Page")
    Site = apps.get_model("wagtailcore", "Site")
    HomePage = apps.get_model("marketing", "HomePage")

    root_page = Page.objects.filter(depth=1).first()
    if not root_page:
        return

    homepage_content_type, _ = ContentType.objects.get_or_create(
        app_label="marketing",
        model="homepage"
    )

    body_json = json.dumps(get_default_homepage_body())

    homepage = HomePage.objects.first()
    if not homepage:
        default_starter = Page.objects.filter(depth=2).first()
        if default_starter and default_starter.content_type.model != "homepage":
            default_starter.title = "Waitaminute Digital"
            default_starter.slug = "home"
            default_starter.url_path = "/home/"
            default_starter.content_type = homepage_content_type
            default_starter.save()
            homepage = HomePage(
                id=default_starter.id,
                title="Waitaminute Digital",
                slug="home",
                intro="Built for creators. Engineered for modern work.",
                body=body_json,
                content_type=homepage_content_type,
                path=default_starter.path,
                depth=default_starter.depth,
                numchild=default_starter.numchild,
                url_path="/home/",
                live=True,
            )
            homepage.save()
        else:
            max_path = Page.objects.filter(depth=2).order_by("-path").values_list("path", flat=True).first()
            if max_path:
                suffix = int(max_path[-4:]) + 1
                path = f"{root_page.path}{suffix:04d}"
            else:
                path = f"{root_page.path}0001"

            homepage = HomePage.objects.create(
                title="Waitaminute Digital",
                slug="home",
                intro="Built for creators. Engineered for modern work.",
                body=body_json,
                content_type=homepage_content_type,
                path=path,
                depth=2,
                numchild=0,
                url_path="/home/",
                live=True,
            )
            root_page.numchild = Page.objects.filter(depth=2).count()
            root_page.save()

    site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
    if site:
        site.root_page_id = homepage.id
        site.site_name = "Waitaminute Digital"
        site.is_default_site = True
        site.save()
    else:
        Site.objects.create(
            hostname="localhost",
            port=80,
            site_name="Waitaminute Digital",
            root_page_id=homepage.id,
            is_default_site=True,
        )


def remove_wagtail_homepage(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_alter_aboutpage_body_alter_homepage_body_and_more'),
        ('wagtailcore', '0097_baselogentry_uuid_action_timestamp_indexes'),
    ]

    operations = [
        migrations.RunPython(setup_wagtail_homepage, remove_wagtail_homepage),
    ]
