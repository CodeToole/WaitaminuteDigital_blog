from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=100, required=False, default='Built for creators. Engineered for modern work.')
    title = blocks.CharBlock(max_length=255, default='We architect modern work systems that turn effort into momentum.')
    subtitle = blocks.TextBlock(required=False, default='Waitaminute Digital helps founders and teams modernize their web presence, automate operations, and turn customer interest into qualified follow-up.')
    primary_cta_label = blocks.CharBlock(max_length=60, required=False, default='Book a Discovery Call')
    primary_cta_url = blocks.CharBlock(max_length=255, required=False, default='/services/#consultation')
    secondary_cta_label = blocks.CharBlock(max_length=60, required=False, default='Explore services')
    secondary_cta_url = blocks.CharBlock(max_length=255, required=False, default='/services/')
    micro_points = blocks.ListBlock(
        blocks.CharBlock(max_length=100),
        required=False,
        default=['Azure-ready builds', 'Microsoft 365 + Copilot workflows', 'Conversion-first design'],
        help_text='Bullet points displayed beneath the call-to-action buttons.'
    )
    badge_text = blocks.CharBlock(max_length=60, required=False, default='Modern Work')
    image = ImageChooserBlock(required=False, help_text='Optional custom hero image. If omitted, animated brand visual is displayed.')

    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'image'
        label = 'Hero Section'


class ServiceCardBlock(blocks.StructBlock):
    kicker = blocks.CharBlock(max_length=20, required=False, default='01', help_text='Card number or index (e.g. 01, 02)')
    title = blocks.CharBlock(max_length=120)
    description = blocks.TextBlock()
    link_url = blocks.CharBlock(max_length=255, required=False, help_text='Optional link destination (e.g. /services/)')
    icon = blocks.CharBlock(max_length=30, required=False, help_text='Optional icon key such as code, chart, bolt.')

    class Meta:
        icon = 'snippet'
        label = 'Service Card'


class ServiceCardsBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False, default='Services')
    heading = blocks.CharBlock(max_length=180, required=False, default='What we build for ambitious teams.')
    intro = blocks.TextBlock(required=False)
    cards = blocks.ListBlock(ServiceCardBlock())

    class Meta:
        template = 'blocks/service_cards_block.html'
        icon = 'list-ul'
        label = 'Services Section'


class PortfolioCardBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120)
    summary = blocks.TextBlock()
    gradient_class = blocks.ChoiceBlock(
        choices=[
            ('gradient-one', 'Gradient 1 (Cyan / Purple)'),
            ('gradient-two', 'Gradient 2 (Purple / Pink)'),
            ('gradient-three', 'Gradient 3 (Cyan / Pink)'),
        ],
        default='gradient-one',
        required=False,
    )
    image = ImageChooserBlock(required=False, help_text='Optional project screenshot')
    link_url = blocks.CharBlock(max_length=255, required=False, default='/portfolio/')

    class Meta:
        icon = 'folder-open-inverse'
        label = 'Portfolio Highlight Card'


class PortfolioHighlightsBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False, default='Featured work')
    heading = blocks.CharBlock(max_length=180, required=False, default='Systems that bring structure to creative momentum.')
    intro = blocks.TextBlock(required=False)
    show_dynamic_projects = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text='Automatically display featured projects from the portfolio database when custom cards are empty.'
    )
    cards = blocks.ListBlock(PortfolioCardBlock(), required=False)

    class Meta:
        template = 'blocks/portfolio_highlights_block.html'
        icon = 'table'
        label = 'Portfolio Highlights'


class InsightsBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False, default='Insights')
    heading = blocks.CharBlock(max_length=180, required=False, default='Practical perspectives for modern operators.')
    show_dynamic_posts = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text='Display the latest published blog posts automatically.'
    )

    class Meta:
        template = 'blocks/insights_block.html'
        icon = 'doc-full-inverse'
        label = 'Insights / Blog Highlights'


class CTASectionBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False, default='Let’s talk')
    heading = blocks.CharBlock(max_length=180, default='Tell us what you’re building.')
    body = blocks.TextBlock(required=False)
    button_label = blocks.CharBlock(max_length=60, required=False, default='Book a Discovery Call')
    button_url = blocks.CharBlock(max_length=255, required=False, default='/services/#consultation')
    secondary_button_label = blocks.CharBlock(max_length=60, required=False)
    secondary_button_url = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = 'blocks/cta_block.html'
        icon = 'arrow-right'
        label = 'Discovery Call CTA'


class FooterNavLinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=60)
    url = blocks.CharBlock(max_length=255)

    class Meta:
        icon = 'link'
        label = 'Footer Link'


class FooterBlock(blocks.StructBlock):
    brand_name = blocks.CharBlock(max_length=60, required=False, default='WAITAMINUTE')
    tagline = blocks.CharBlock(max_length=180, required=False, default='Built for creators. Engineered for modern work.')
    email = blocks.CharBlock(max_length=120, required=False, default='hello@waitaminutedigital.com')
    contact_link_label = blocks.CharBlock(max_length=80, required=False, default="Tell us what you're building")
    contact_link_url = blocks.CharBlock(max_length=255, required=False, default='/services/#consultation')
    nav_links = blocks.ListBlock(FooterNavLinkBlock(), required=False)
    copyright = blocks.CharBlock(max_length=120, required=False, default='Waitaminute Digital. All rights reserved.')

    class Meta:
        template = 'blocks/footer_block.html'
        icon = 'site'
        label = 'Footer Section'


class RichContentBlock(blocks.RichTextBlock):
    class Meta:
        label = 'Rich content'
        template = 'blocks/rich_content_block.html'
        icon = 'doc-full'


class PageStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    service_cards = ServiceCardsBlock()
    portfolio_highlights = PortfolioHighlightsBlock()
    insights = InsightsBlock()
    cta = CTASectionBlock()
    footer = FooterBlock()
    rich_content = RichContentBlock(features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3', 'code', 'blockquote'])

