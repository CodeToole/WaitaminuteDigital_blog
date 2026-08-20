from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False)
    title = blocks.CharBlock(max_length=180)
    subtitle = blocks.TextBlock(required=False)
    primary_cta_label = blocks.CharBlock(max_length=60, required=False, default='Book a discovery call')
    primary_cta_url = blocks.URLBlock(required=False)
    secondary_cta_label = blocks.CharBlock(max_length=60, required=False, default='Explore services')
    secondary_cta_url = blocks.URLBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'image'


class ServiceCardBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=80)
    description = blocks.TextBlock()
    icon = blocks.CharBlock(max_length=30, required=False, help_text='Optional icon key such as code, chart, bolt.')

    class Meta:
        icon = 'snippet'


class ServiceCardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False, default='What we build')
    intro = blocks.TextBlock(required=False)
    cards = blocks.ListBlock(ServiceCardBlock())

    class Meta:
        template = 'blocks/service_cards_block.html'
        icon = 'list-ul'


class CTASectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    body = blocks.TextBlock(required=False)
    button_label = blocks.CharBlock(max_length=60, required=False, default='Book a discovery call')
    button_url = blocks.URLBlock(required=False)

    class Meta:
        template = 'blocks/cta_block.html'
        icon = 'arrow-right'


class RichContentBlock(blocks.RichTextBlock):
    class Meta:
        label = 'Rich content'
        template = 'blocks/rich_content_block.html'
        icon = 'doc-full'


class PageStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    service_cards = ServiceCardsBlock()
    cta = CTASectionBlock()
    rich_content = RichContentBlock(features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'])
