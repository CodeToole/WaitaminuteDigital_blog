import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waitaminute.settings')

import django
from django.utils import timezone

django.setup()

from blog.models import Category, Post

Category.objects.get_or_create(name='Strategy', slug='strategy')
Category.objects.get_or_create(name='AI', slug='ai')
Category.objects.get_or_create(name='Operations', slug='operations')

seed = [
    {
        'title': 'Designing a website that acts like a sales system',
        'slug': 'designing-a-website-that-acts-like-a-sales-system',
        'excerpt': 'Clarity on the page keeps conversion momentum high and reduces friction before the first conversation begins.',
        'body': "A website is not just a brochure. It is a system for attention, trust, and action. When a visitor arrives, they should understand who you help, why it matters, and what happens next without guessing.\n\nThat means your pages need to do more than look polished. They need a clear narrative arc: identify the problem, position the solution, and give the visitor a low-friction way to reach out. The strongest websites are designed with a conversion path built into the layout, not bolted on after the fact.\n\nFor founders and lean teams, this usually means clearer service language, more confident CTAs, and fewer distractions. When the buying journey is obvious, the conversation starts sooner and the sales process becomes calmer and more intentional.",
        'category': 'Strategy',
        'status': 'published',
    },
    {
        'title': '3 signs your team is ready for workflow automation',
        'slug': '3-signs-your-team-is-ready-for-workflow-automation',
        'excerpt': 'Repetition, handoffs, and stale data are usually the first warning signs that automation can pay for itself quickly.',
        'body': "Teams rarely need a huge AI rollout before they benefit from automation. The first clue is repeatable work that happens the same way every week. If someone's manually moving information across tools, re-sending the same email, or updating the same record in multiple places, it is a process that can likely be improved.\n\nThe second signal is fragmented systems. If the client workflow depends on spreadsheets, email threads, calls, and a CRM all at once, the process is leaking time. The third is slow follow-through: when leads go cold because no one has a clean handoff plan, automation can restore rhythm.\n\nThis is not about replacing judgment or human connection. It is about reducing friction so your team can focus on higher-value work.",
        'category': 'AI',
        'status': 'published',
    },
    {
        'title': 'What a modern work stack should feel like',
        'slug': 'what-a-modern-work-stack-should-feel-like',
        'excerpt': 'The right stack should reduce friction, not create another layer of hidden complexity.',
        'body': "A modern work stack should feel calm and connected. The tools should support the actual work instead of forcing teams to think about the toolchain every time they need a simple task done. That means fewer manual breaks in the workflow, cleaner handoffs, and a stronger sense of operational rhythm.\n\nFor many businesses, that begins with a clear website, a CRM or intake flow, and a few automation rules that actually save time. Nothing fancy is required at the start. The goal is to build a system that is easy to explain, easy to maintain, and easy to trust.\n\nThe best systems feel invisible to the people running them. They create momentum without generating chaos.",
        'category': 'Operations',
        'status': 'draft',
    },
]

for item in seed:
    category, _ = Category.objects.get_or_create(name=item['category'], slug=item['category'].lower().replace(' ', '-'))
    post, created = Post.objects.get_or_create(
        slug=item['slug'],
        defaults={
            'title': item['title'],
            'excerpt': item['excerpt'],
            'body': item['body'],
            'category': category,
            'status': item['status'],
            'published_at': timezone.now() if item['status'] == 'published' else None,
        },
    )
    if not created:
        post.title = item['title']
        post.excerpt = item['excerpt']
        post.body = item['body']
        post.category = category
        post.status = item['status']
        post.published_at = timezone.now() if item['status'] == 'published' else None
        post.save()
    print(f"seeded {post.title}")
