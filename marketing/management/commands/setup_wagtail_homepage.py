import json
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from marketing.models import HomePage, ServicesPage, AboutPage


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


class Command(BaseCommand):
    help = "Set up the production-ready Wagtail HomePage, replace default starter page, and configure Site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-body",
            action="store_true",
            help="Overwrite existing HomePage StreamField body with default production content.",
        )

    def handle(self, *args, **options):
        root_page = Page.get_first_root_node()
        if not root_page:
            self.stderr.write(self.style.ERROR("No root Wagtail page found."))
            return

        # Check if HomePage exists
        homepage = HomePage.objects.first()
        body_data = json.dumps(get_default_homepage_body())

        if not homepage:
            # Check for generic default page (depth=2)
            default_page = Page.objects.filter(depth=2).first()
            
            homepage = HomePage(
                title="Waitaminute Digital",
                slug="home",
                intro="Built for creators. Engineered for modern work.",
                live=True,
                search_description="Waitaminute Digital designs modern websites, automation workflows, and digital systems for creators, founders, and ambitious teams.",
            )
            homepage.body = body_data

            if default_page and not hasattr(default_page, "homepage"):
                # Delete or unpublish the starter placeholder
                root_page.add_child(instance=homepage)
                try:
                    default_page.delete()
                except Exception:
                    pass
            else:
                root_page.add_child(instance=homepage)

            homepage.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Created new HomePage '{homepage.title}' (id={homepage.id})."))
        else:
            if options.get("force_body") or not homepage.body:
                homepage.body = body_data
                homepage.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("Updated HomePage StreamField content."))

        # Configure or create Site
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if site:
            site.root_page = homepage
            site.site_name = "Waitaminute Digital"
            site.is_default_site = True
            site.save()
            self.stdout.write(self.style.SUCCESS(f"Updated default Wagtail Site (id={site.id}) root page to HomePage."))
        else:
            site = Site.objects.create(
                hostname="localhost",
                port=80,
                site_name="Waitaminute Digital",
                root_page=homepage,
                is_default_site=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Created default Wagtail Site with root page '{homepage.title}'."))

        # Ensure ServicesPage subpage exists
        if not ServicesPage.objects.exists():
            services_page = ServicesPage(
                title="Services",
                slug="services",
                intro="What we build for ambitious teams.",
                live=True,
            )
            homepage.add_child(instance=services_page)
            services_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("Created ServicesPage subpage."))

        # Ensure AboutPage subpage exists
        if not AboutPage.objects.exists():
            about_page = AboutPage(
                title="About",
                slug="about",
                intro="Waitaminute Digital helps founders and teams modernize their web presence, streamline recurring work, and design sharper digital experiences.",
                live=True,
            )
            homepage.add_child(instance=about_page)
            about_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("Created AboutPage subpage."))

        self.stdout.write(self.style.SUCCESS("Wagtail page tree and production homepage setup complete!"))
