import json
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Locale, Page, Site
from marketing.models import HomePage, ServicesPage, AboutPage


class SetupWagtailHomepageCommandTests(TestCase):
    def setUp(self):
        # Ensure default locale exists
        self.locale = Locale.get_default()
        if not self.locale:
            self.locale = Locale.objects.first()
        if not self.locale:
            self.locale = Locale.objects.create(language_code="en-us")

        # Ensure root page exists
        self.root_page = Page.get_first_root_node()
        if not self.root_page:
            self.root_page = Page.objects.filter(depth=1).first()
        if not self.root_page:
            self.root_page = Page.add_root(instance=Page(title="Root", slug="root", locale=self.locale))

        # Create starter placeholder page (depth=2) if none exists
        if not Page.objects.filter(depth=2).exists():
            starter_page = Page(
                title="Welcome to your new Wagtail site!",
                slug="home",
                locale=self.locale,
                live=True,
            )
            self.root_page.add_child(instance=starter_page)

    def test_command_creates_production_homepage_and_site(self):
        out = StringIO()
        call_command("setup_wagtail_homepage", stdout=out)
        output = out.getvalue()

        # Console outputs check
        self.assertIn("Default Locale:", output)
        self.assertIn("Selected Root Page:", output)
        self.assertIn("Waitaminute Digital", output)
        self.assertIn("Site root assignment:", output)
        self.assertIn("Publication result:", output)

        # 1. Exactly one HomePage with slug "home"
        homepages = HomePage.objects.filter(slug="home")
        self.assertEqual(homepages.count(), 1)
        homepage = homepages.first()

        # 2. Non-null locale
        self.assertIsNotNone(homepage.locale)
        self.assertEqual(homepage.locale, self.locale)

        # 3. HomePage is live
        self.assertTrue(homepage.live)
        self.assertEqual(homepage.title, "Waitaminute Digital")

        # 4. Site root points to that HomePage
        site = Site.objects.filter(is_default_site=True).first()
        self.assertIsNotNone(site)
        self.assertEqual(site.root_page.specific, homepage)
        self.assertEqual(site.hostname, "waitaminutedigital.com")
        self.assertEqual(site.port, 443)
        self.assertEqual(site.site_name, "Waitaminute Digital")

        # 5. Seeded StreamField content is present
        self.assertTrue(bool(homepage.body))
        block_types = [block.block_type for block in homepage.body]
        self.assertIn("hero", block_types)
        self.assertIn("service_cards", block_types)
        self.assertIn("portfolio_highlights", block_types)
        self.assertIn("insights", block_types)
        self.assertIn("cta", block_types)
        self.assertIn("footer", block_types)

        # Verify specific content inside stream blocks
        hero_block = next(b for b in homepage.body if b.block_type == "hero")
        self.assertEqual(hero_block.value["eyebrow"], "Built for creators.")
        self.assertEqual(hero_block.value["title"], "Engineered for modern work.")
        self.assertEqual(hero_block.value["primary_cta_label"], "Book a Discovery Call")
        self.assertEqual(hero_block.value["primary_cta_url"], "/services/")
        self.assertEqual(hero_block.value["secondary_cta_label"], "View Our Work")
        self.assertEqual(hero_block.value["secondary_cta_url"], "/portfolio/")

        service_block = next(b for b in homepage.body if b.block_type == "service_cards")
        card_titles = [card["title"] for card in service_block.value["cards"]]
        self.assertIn("Modern Work Websites", card_titles)
        self.assertIn("AI and Automation", card_titles)
        self.assertIn("Managed Website Solutions", card_titles)

        portfolio_block = next(b for b in homepage.body if b.block_type == "portfolio_highlights")
        project_titles = [card["title"] for card in portfolio_block.value["cards"]]
        self.assertIn("The Acting Collective", project_titles)
        self.assertIn("Unicorn Bounty Hunters", project_titles)
        self.assertIn("Huncho Fest", project_titles)

        cta_block = next(b for b in homepage.body if b.block_type == "cta")
        self.assertEqual(cta_block.value["heading"], "Tell us what you're building.")

        footer_block = next(b for b in homepage.body if b.block_type == "footer")
        self.assertEqual(footer_block.value["brand_name"], "Waitaminute Digital")
        self.assertIn("Mobile, Alabama", footer_block.value["tagline"])

        # 6. Check that old starter page was archived and not deleted
        archived_pages = Page.objects.filter(slug="wagtail-starter-archive")
        self.assertEqual(archived_pages.count(), 1)
        archived = archived_pages.first()
        self.assertEqual(archived.title, "Archived Wagtail Starter Page")
        self.assertFalse(archived.live)

    def test_command_is_idempotent_can_run_twice(self):
        # Run 1
        out1 = StringIO()
        call_command("setup_wagtail_homepage", stdout=out1)

        # Run 2
        out2 = StringIO()
        call_command("setup_wagtail_homepage", stdout=out2)
        out2_val = out2.getvalue()

        self.assertIn("Reused and updated existing HomePage", out2_val)

        # Verify no duplicates
        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(HomePage.objects.filter(slug="home").count(), 1)
        self.assertEqual(ServicesPage.objects.count(), 1)
        self.assertEqual(AboutPage.objects.count(), 1)
        self.assertEqual(Site.objects.filter(is_default_site=True).count(), 1)
