import json
from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page, Site
from marketing.models import HomePage, ServicesPage, AboutPage


def get_default_homepage_body():
    return [
        {
            "type": "hero",
            "value": {
                "eyebrow": "Built for creators.",
                "title": "Engineered for modern work.",
                "subtitle": "Waitaminute Digital is a modern web, automation, and AI solutions studio. We architect digital systems that turn effort into momentum.",
                "primary_cta_label": "Book a Discovery Call",
                "primary_cta_url": "/services/",
                "secondary_cta_label": "View Our Work",
                "secondary_cta_url": "/portfolio/",
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
                "intro": "We design conversion-focused websites, automate repetitive work, and build digital systems that give teams more clarity and momentum.",
                "cards": [
                    {
                        "kicker": "01",
                        "title": "Modern Work Websites",
                        "description": "High-converting websites designed around clarity, authority, and action.",
                        "link_url": "/services/",
                        "icon": "code",
                    },
                    {
                        "kicker": "02",
                        "title": "AI and Automation",
                        "description": "Copilot Studio, Power Automate, and workflow design that removes repetitive work.",
                        "link_url": "/services/",
                        "icon": "bolt",
                    },
                    {
                        "kicker": "03",
                        "title": "Managed Website Solutions",
                        "description": "Ongoing design, engineering, and optimization for teams that need their digital presence to evolve.",
                        "link_url": "/services/",
                        "icon": "chart",
                    },
                ],
            },
        },
        {
            "type": "portfolio_highlights",
            "value": {
                "eyebrow": "Featured work",
                "heading": "Systems that bring structure to creative momentum.",
                "intro": "Selected projects and client systems built for scale.",
                "show_dynamic_projects": True,
                "cards": [
                    {
                        "title": "The Acting Collective",
                        "summary": "Digital platform and community architecture for modern performers and creatives.",
                        "gradient_class": "gradient-one",
                        "link_url": "/portfolio/",
                    },
                    {
                        "title": "Unicorn Bounty Hunters",
                        "summary": "Interactive brand experience and digital platform built for scale.",
                        "gradient_class": "gradient-two",
                        "link_url": "/portfolio/",
                    },
                    {
                        "title": "Huncho Fest",
                        "summary": "Live event marketing and festival web experience driving ticket conversions.",
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
                "heading": "Tell us what you're building.",
                "body": "Every engagement is custom-scoped after a discovery call to match your operational goals and technical requirements.",
                "button_label": "Book a Discovery Call",
                "button_url": "/services/#consultation",
            },
        },
        {
            "type": "footer",
            "value": {
                "brand_name": "Waitaminute Digital",
                "tagline": "Built for creators. Engineered for modern work. — Mobile, Alabama",
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


class Command(BaseCommand):
    help = "Idempotently set up the production-ready Wagtail HomePage, archive starter page, and configure default Site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-body",
            action="store_true",
            help="Overwrite existing HomePage StreamField body with default production content even if body is not empty.",
        )

    def handle(self, *args, **options):
        # 1. Default Locale
        locale = Locale.get_default()
        if not locale:
            locale = Locale.objects.first()
        if not locale:
            locale = Locale.objects.create(language_code="en-us")
        self.stdout.write(f"Default Locale: {locale.language_code} (id={locale.id})")

        # 2. Selected Root Page
        root_page = Page.get_first_root_node()
        if not root_page:
            root_page = Page.objects.filter(depth=1).first()
        if not root_page:
            root_page = Page.add_root(instance=Page(title="Root", slug="root", locale=locale))
        self.stdout.write(f"Selected Root Page: '{root_page.title}' (id={root_page.id}, path={root_page.path})")

        # 3. Inspect existing children of root_page
        root_children = list(root_page.get_children())
        archived_starter = None
        existing_homepage = None

        for child in root_children:
            specific_child = child.specific
            if isinstance(specific_child, HomePage):
                existing_homepage = specific_child
            elif child.slug == "home" or "Welcome to your new Wagtail site" in child.title:
                starter = specific_child
                starter.title = "Archived Wagtail Starter Page"
                starter.slug = "wagtail-starter-archive"
                starter.live = False
                if hasattr(starter, "unpublish"):
                    try:
                        starter.unpublish()
                    except Exception:
                        pass
                starter.save()
                archived_starter = starter
                self.stdout.write(
                    self.style.WARNING(
                        f"Archived starter page: '{starter.title}' (id={starter.id}, slug='{starter.slug}', live={starter.live})"
                    )
                )

        if not archived_starter:
            self.stdout.write("Archived starter page: None (no unarchived starter placeholder found)")

        # 4. Reused or Created HomePage
        if not existing_homepage:
            existing_homepage = HomePage.objects.first()

        body_json = json.dumps(get_default_homepage_body())

        if not existing_homepage:
            homepage = HomePage(
                title="Waitaminute Digital",
                slug="home",
                intro="Built for creators. Engineered for modern work.",
                locale=locale,
                live=True,
                search_description="Waitaminute Digital designs modern websites, automation workflows, and digital systems for creators, founders, and ambitious teams.",
            )
            homepage.body = body_json
            root_page.add_child(instance=homepage)
            action_desc = "Created new HomePage"
        else:
            homepage = existing_homepage
            homepage.title = "Waitaminute Digital"
            homepage.slug = "home"
            homepage.locale = locale
            homepage.intro = "Built for creators. Engineered for modern work."
            if options.get("force_body") or not homepage.body:
                homepage.body = body_json
            homepage.save()
            action_desc = "Reused and updated existing HomePage"

        self.stdout.write(f"Reused or created homepage: {action_desc} '{homepage.title}' (id={homepage.id}, slug='{homepage.slug}')")

        # 5. Publication Result
        revision = homepage.save_revision()
        revision.publish()
        homepage.refresh_from_db()
        self.stdout.write(
            self.style.SUCCESS(
                f"Publication result: HomePage '{homepage.title}' published successfully (id={homepage.id}, live={homepage.live}, revision_id={revision.id})"
            )
        )

        # 6. Site Root Assignment
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if site:
            site.hostname = "waitaminutedigital.com"
            site.port = 443
            site.site_name = "Waitaminute Digital"
            site.root_page = homepage
            site.is_default_site = True
            site.save()
        else:
            site = Site.objects.create(
                hostname="waitaminutedigital.com",
                port=443,
                site_name="Waitaminute Digital",
                root_page=homepage,
                is_default_site=True,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Site root assignment: Site '{site.site_name}' ({site.hostname}:{site.port}, default={site.is_default_site}) -> Root Page '{site.root_page.title}' (id={site.root_page.id})"
            )
        )

        # 7. Subpages (ServicesPage and AboutPage)
        if not ServicesPage.objects.exists():
            services_page = ServicesPage(
                title="Services",
                slug="services",
                locale=locale,
                intro="What we build for ambitious teams.",
                live=True,
            )
            homepage.add_child(instance=services_page)
            services_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Created ServicesPage subpage (id={services_page.id})."))

        if not AboutPage.objects.exists():
            about_page = AboutPage(
                title="About",
                slug="about",
                locale=locale,
                intro="Waitaminute Digital helps founders and teams modernize their web presence, streamline recurring work, and design sharper digital experiences.",
                live=True,
            )
            homepage.add_child(instance=about_page)
            about_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Created AboutPage subpage (id={about_page.id})."))

        self.stdout.write(self.style.SUCCESS("Wagtail homepage bootstrap complete!"))


