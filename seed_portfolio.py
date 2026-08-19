import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waitaminute.settings')

import django

django.setup()

from portfolio.models import Project, Tag

Project.objects.filter(slug__in=['northstar-rebrand', 'atlas-studio-launch', 'copilot-flow-audit']).delete()

for name, slug in [('Web', 'web'), ('Brand', 'brand'), ('Automation', 'automation'), ('Strategy', 'strategy')]:
    Tag.objects.get_or_create(name=name, slug=slug)

seed = [
    {
        'title': 'The Acting Collective',
        'slug': 'acting-collective',
        'client': 'The Acting Collective — Powered by Ziare',
        'summary': 'A direct pipeline from acting training to real film credits — built for Mobile, Alabama.',
        'body': "We designed and built the full registration experience for The Acting Collective, Ziare Perryman's actor-training pipeline in Mobile, AL. The site runs on .NET Blazor (Interactive Server) on Azure, with a monochrome-and-gold cinematic design. Key systems: a time-aware registration countdown that automatically flips to a waitlist when the session fills, Azure Table Storage for registrations and waitlist management, Azure Communication Services confirmation emails, Square payment links for checkout, and an Entra ID–protected staff check-in / roster page with search, attendance timestamps, and walk-in registration. The result: a boutique, high-touch enrollment flow that matches the brand and runs itself on event day.",
        'url': 'https://theactingcollective.vip',
        'is_featured': True,
        'tags': ['Web', 'Brand', 'Automation'],
    },
    {
        'title': 'Unicorn Bounty Hunters',
        'slug': 'unicorn-bounty-hunters',
        'client': 'Unicorn Bounty Hunters LLC — Ali Kazem',
        'summary': 'A studio-booking and artist-roster site for an independent Mobile music collective.',
        'body': "Unicorn Bounty Hunters is an independent recording studio, label, and podcast (Shadow Talk) based in Mobile, AL. We rebuilt their web presence into a single 'Prestige' hub: an artist roster (Ali Kazem, Malik Rosé, Unkn0wn Da Rapper, Yung Illie), a studio-session booking flow (date/time/duration → secure checkout), a music + merch showcase, and an email capture ('Join the Hunt') for exclusive drops and priority booking. The design leans into the dark, cinematic UBH identity so the brand reads as premium from the first scroll.",
        'url': 'https://unicornbountyhunters.com',
        'is_featured': True,
        'tags': ['Web', 'Brand'],
    },
    {
        'title': 'Huncho Fest',
        'slug': 'huncho-fest',
        'client': 'Huncho Fest — presented by NMBG Jay',
        'summary': "The event and artist-registration site for Mobile's biggest independent music festival.",
        'body': "Huncho Fest is Mobile's biggest independent music festival, staged at downtown's Mardi Gras Park and covered by FOX 10 and South Alabama News. We built the festival's web home: a bold, media-forward landing experience with artist registration, 'Secure Your Slot' ticket/registration capture, embedded live media (video + streaming links), and an email list for artist announcements and ticket drops. The design celebrates Gulf Coast culture while driving the two actions that matter — get artists to register and get fans to grab tickets.",
        'url': 'https://hunchofest.com',
        'is_featured': False,
        'tags': ['Web', 'Brand', 'Strategy'],
    },
]

for item in seed:
    project, created = Project.objects.get_or_create(
        slug=item['slug'],
        defaults={
            'title': item['title'],
            'client': item['client'],
            'summary': item['summary'],
            'body': item['body'],
            'url': item['url'],
            'is_featured': item['is_featured'],
        },
    )
    if not created:
        project.title = item['title']
        project.client = item['client']
        project.summary = item['summary']
        project.body = item['body']
        project.url = item['url']
        project.is_featured = item['is_featured']
        project.save()

    project.tags.clear()
    for tag_name in item['tags']:
        project.tags.add(Tag.objects.get(name=tag_name))

    print(f"seeded {project.title}")
