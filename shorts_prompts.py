"""YouTube Shorts Stüdyosu — modül tanımları ve prompt şablonları.

Her modül, kullanıcının kanal profilini (alan, kitle, rakipler, hedefler) alır ve
uzman rolüyle ayrıntılı bir çıktı üretir. Yaratıcı içerik (hook, başlık, senaryo,
altyazı, açıklama, hashtag) her zaman seçilen içerik dilinde (varsayılan: İngilizce)
üretilir; açıklamalar ve stratejik yorumlar ayrı seçilen açıklama dilinde yazılır.
"""

# Modelin bilmesi gereken, Shorts'a dair güncel referans bilgiler.
# Not: Platform kuralları değişebilir; model bunları "doğrulanması gereken" bilgi olarak sunmalı.
PLATFORM_FACTS = """
REFERENCE FACTS (state them as "verify in YouTube Studio / official help pages", rules change):
- Shorts can be up to 3 minutes long (vertical or square). 15–45 s remains the sweet spot for most
  niches; go longer only when the story genuinely holds attention.
- Since March 2025 a Shorts "view" counts every start/replay; "engaged views" is the stricter metric
  used for monetization. YouTube Studio shows "Viewed vs. swiped away" for each Short — this is the
  first gate of distribution.
- Shorts recommendations are driven by viewer satisfaction signals: viewed-vs-swiped ratio, average
  percentage viewed (often >100% thanks to loops), likes, shares, comments, subscribes from the Short,
  and follow-up behaviour (does the viewer watch more from the channel). Hashtags and titles help
  topical classification but are secondary.
- YouTube Partner Program: full tier (Shorts ad revenue share, 45% to creator) needs 1,000 subscribers
  + 10M valid public Shorts views in the last 90 days (or 4,000 public watch hours in 12 months).
  The lower "fan funding" tier (memberships, Super Thanks, Shopping) needs 500 subscribers + 3 public
  uploads in 90 days + 3M Shorts views in 90 days (or 3,000 watch hours). Thresholds can differ by country.
- Shorts can link to a long-form video ("Related video"), which is the main bridge to long-form watch time.
- English-language content reaches the largest, highest-CPM audiences (US, UK, CA, AU) but competition
  is also highest; specificity of niche matters more than broad appeal.
"""

BASE_ROLE = """
You are a world-class YouTube Shorts strategist who has consulted for top creators and media brands.
You give concrete, actionable, non-generic advice tailored to the creator profile below.
Never give vague advice like "be consistent" without specifying exactly what, how often and how to measure it.
Use tables, checklists and numbered steps where they help. Use realistic numbers and clearly label
assumptions. Do not invent statistics about specific real channels; when you mention competitors,
reason about their likely strategy from what the creator told you and say what to verify.
"""

LANGUAGE_RULES = """
LANGUAGE RULES (strict):
- Write all explanations, analysis and strategy commentary in: {explain_lang}.
- Write ALL audience-facing creative assets in: {content_lang} — this includes hooks, video titles,
  on-screen text, scripts/voice-over lines, captions/subtitles, descriptions, pinned comments,
  CTAs and hashtags. Write them in natural, native, conversational {content_lang} the way top
  creators in that language actually speak (short words, punchy rhythm, no textbook phrasing).
- When content language is English, target a global English-speaking audience (US/UK/CA/AU first),
  avoid culture-specific references the audience would not understand, and use US spelling.
"""


def channel_profile(p: dict) -> str:
    return f"""
CREATOR PROFILE
- Niche / topic: {p.get('niche') or '-'}
- Target audience: {p.get('audience') or '-'}
- Competitors / reference channels: {p.get('competitors') or '-'}
- Goals: {p.get('goals') or '-'}
- Current status (subscribers, views, upload frequency): {p.get('status') or '-'}
- Resources (time per week, budget, team, on-camera or faceless, tools): {p.get('resources') or '-'}
- Extra notes: {p.get('notes') or '-'}
"""


MODULES = {
    "system": {
        "title": "1 · Shorts İçerik ve Büyüme Sistemi",
        "short": "Kanal analizi, içerik kategorileri, senaryo ve kurgu süreci, takvim, uzun vadeli strateji",
        "task": """
TASK: Build a complete YouTube Shorts content & growth system for this creator.
Deliver these sections:
1. Niche analysis — positioning statement, the gap in the market, what makes this channel worth
   subscribing to (a one-sentence "subscribe promise"), and 3 positioning angles ranked.
2. Audience analysis — 2–3 viewer personas (age, context, pains, desires, what they search,
   what makes them share), and what each persona needs from a Short.
3. Competitor analysis — for each named competitor (or the archetypes in this niche): likely
   winning formats, weaknesses, and the concrete angle this creator should take to stand out.
4. Goal translation — turn the goals into measurable 30/90/180-day targets.
5. Content pillars — 4–6 recurring content categories (series) with: name, purpose
   (reach / trust / conversion), share of output (%), 3 example titles each (in content language).
6. Scriptwriting method — a reusable script framework with timing (0–3 s hook, setup, payoff,
   loop/CTA), word counts per segment (~2.5–3 words/sec), and one fully written example script.
7. Editing process — step-by-step editing workflow, style guide (fonts, caption style, color,
   cut pace, sound design, B-roll rules), and a pre-publish quality checklist.
8. Publishing calendar — a 4-week calendar (table: day, pillar, format, working title, time slot)
   with recommended frequency based on the creator's resources, and a batching routine.
9. Long-term strategy — how to build series, community, long-form bridge, and brand over 12 months.
""",
    },
    "ideas": {
        "title": "2 · Viral Shorts Araştırma Motoru (200 fikir)",
        "short": "Kanıtlanmış formatlar, hook'lar, duygusal tetikleyiciler ve sıralı 200 fikir",
        "task": """
TASK: Act as an elite viral content researcher for this niche.
{batch_instructions}
""",
        "batches": 4,
        "batch_size": 50,
    },
    "retention": {
        "title": "3 · Dikkat Çekici Açılış ve İzleyici Tutma Ustalığı",
        "short": "İlk 3 saniye, tempo, merak döngüleri, altyazı, geçişler, loop'lu kapanışlar",
        "task": """
TASK: Act as a YouTube retention strategist. Teach and design a complete system that makes viewers
watch this creator's Shorts to the end and rewatch them. Cover:
1. The first 3 seconds — the 3 layers of a hook (visual, on-screen text, spoken line), why
   "viewed vs. swiped away" is the first gate; 15 hook formulas, each with 2 ready examples
   written for THIS niche (in content language).
2. Pacing — visual change every 1–2 s, sentence length, removing breaths/filler, pattern interrupts;
   a second-by-second pacing map for a 30 s and a 60 s Short.
3. Curiosity loops — open loops, delayed payoff, "but…" turns, stacking questions; with examples.
4. Storytelling — 4 short-form story structures (e.g. problem→twist→payoff, list with best last,
   before/after, myth→truth) with a niche example each.
5. Editing rhythm — cut rules, zooms, jump cuts, B-roll, sound effects and music sync.
6. Captions — style rules (words per line, highlight keywords, safe zones away from UI buttons),
   tools to produce them.
7. Transitions — which ones help retention and which hurt it.
8. Endings — seamless loop techniques (last line flows into first line), rewatch triggers,
   comment-bait questions, subscribe CTAs that don't kill retention; 10 examples in content language.
9. Diagnosis table — retention graph shape → likely cause → fix.
10. A one-page pre-publish retention checklist.
""",
    },
    "ai_production": {
        "title": "4 · Yapay Zekâ Destekli Kısa Video Üretim Sistemi",
        "short": "Fikir→senaryo→seslendirme→kurgu→altyazı→müzik→yayın→analiz ve Reels/TikTok/Threads uyarlaması",
        "task": """
TASK: Act as an executive producer specialized in AI-assisted video production. Design an end-to-end,
efficient workflow for producing this creator's Shorts with AI tools. For EACH stage give: goal,
recommended tools (free and paid alternatives), exact steps, ready-to-copy AI prompts (in English),
time estimate, quality-control checks, and common mistakes:
1. Idea generation  2. Script writing  3. Voice-over (incl. AI voice and disclosure considerations)
4. Visuals & video editing (stock, AI-generated B-roll, screen recording, templates)
5. Captions/subtitles  6. Music & sound (licensing — only use cleared/royalty-free audio)
7. Publishing (title, description, hashtags, thumbnail frame, scheduling)
8. Performance analysis  9. Repurposing to Instagram Reels, TikTok and Threads — what to change per
   platform (length, caption, hashtags, on-screen text, cover, posting time, native features, and
   removing watermarks).
Then provide:
- A weekly batch-production schedule that produces the target number of Shorts per week.
- A Notion/Sheets-style production tracker template (table columns).
- Guardrails: YouTube's altered/synthetic content disclosure label, copyright, avoiding
  "reused/repetitious content" demonetization, keeping a human voice and originality.
""",
    },
    "algorithm": {
        "title": "5 · Shorts Büyüme ve Algoritma Stratejisi",
        "short": "Öneri sistemi nasıl çalışır, testler, metrikler ve kazanan kalıpları bulma",
        "task": """
TASK: Act as a YouTube Shorts growth expert.
1. Explain clearly how the Shorts recommendation system works (Shorts feed, seed audience testing,
   expansion waves, satisfaction signals, why views come in bursts, why old Shorts can revive),
   and what the creator controls vs. does not control.
2. Strategy to grow views, subscribers and engagement for this niche — concrete tactics per goal.
3. Content testing system — how to run A/B-style experiments on Shorts (one variable at a time:
   hook, length, format, topic, title, posting time), sample size, how long to wait, a test log template.
4. Performance optimization — what to do with a Short at 1 h, 24 h, 72 h, 7 days.
5. Metric analysis — the key metrics, how to read them, healthy benchmark ranges (label as
   approximate), and decision rules.
6. Winning-pattern detection — how to tag every Short (format, hook type, topic, length, emotion),
   find patterns in the data, and turn winners into series ("remix the winner" playbook).
7. Common growth killers and how to avoid them.
""",
    },
    "monetization": {
        "title": "6 · Shorts Para Kazanma Planı",
        "short": "Dijital ürün, satış ortaklığı, sponsorluk, üyelik, e-posta bülteni ve diğer gelirler",
        "task": """
TASK: Act as a business strategist for content creators. Design a complete monetization system for
this creator's Shorts audience. For EACH revenue stream — YouTube Partner Program (Shorts ad share),
fan funding (memberships, Super Thanks), YouTube Shopping, affiliate marketing, sponsorships/brand
deals, digital products (templates, guides, courses, presets), paid communities/memberships,
email newsletter, services/consulting, licensing, and any niche-specific stream — give:
- When to start it (subscriber/view thresholds and audience-trust signals),
- How to implement it step by step (tools, pricing ideas, funnel from Short → link → offer),
- Expected revenue range with assumptions clearly labeled,
- Risks and how to protect audience trust.
Then provide: a staged monetization roadmap (stage 0 → stage 4), a simple revenue model table,
a sponsor media-kit outline with rate-card logic, 3 product ideas fit for this niche,
and CTA/pinned-comment examples (in content language) that convert without hurting retention.
Note Shorts-specific limits (e.g. clickable links in Shorts are restricted — use related video,
channel links, pinned comments, profile link).
""",
    },
    "analytics": {
        "title": "7 · Performans Analizi ve Optimizasyonu",
        "short": "Analiz paneli, metrikler ve haftalık 'daha fazla / geliştir / durdur' değerlendirmesi",
        "task": """
TASK: Act as a YouTube analytics expert. Build a complete performance-analysis dashboard and review
system for this creator's Shorts.
1. Dashboard design — a spreadsheet layout (exact column names, formulas in Google Sheets syntax
   where useful) tracking per Short: publish date, pillar, format, hook type, length, views,
   viewed-vs-swiped %, average view duration, average % viewed, rewatch/loop rate, likes, comments,
   shares, subscribers gained, subs per 1,000 views, engagement rate, traffic source.
2. Metric definitions — how each metric is calculated / where to find it in YouTube Studio,
   and benchmark bands (poor / ok / good / excellent) labeled as approximate.
3. Trend tracking — weekly and monthly views, rolling averages, per-pillar performance, and
   how to spot topic/format fatigue.
4. Weekly review system — a 30-minute weekly ritual with a decision matrix that classifies every
   content type into: SCALE (make more), IMPROVE (iterate), or STOP — with explicit numeric rules.
5. A weekly review template (filled example with fictional sample numbers, clearly marked as example).
6. Monthly deep-dive questions and a quarterly strategy reset checklist.
""",
    },
    "roadmap": {
        "title": "8 · 12 Aylık Büyüme Yol Haritası",
        "short": "Aylık hedefler, paylaşım sıklığı, para kazanma aşamaları, iş birlikleri, KPI'lar ve B planları",
        "task": """
TASK: Act as a world-class creator-business growth consultant. Create a detailed 12-month roadmap that
turns this creator's Shorts strategy into a sustainable content business.
1. Phases (e.g. Foundation, Traction, Scale, Business) with goals and success criteria.
2. A month-by-month table (Month 1–12): focus, upload frequency, content priorities, audience
   growth target (subscribers & monthly views — conservative / expected / optimistic),
   monetization milestone, collaboration actions, KPIs, and key deliverables.
3. Collaboration strategy — who to collaborate with at each stage, how to pitch (with a short
   outreach message template in content language), collab formats that work in Shorts.
4. Systems & team — what to systemize or outsource and when.
5. KPI scorecard — the 8–10 KPIs to track monthly with targets.
6. Contingency plans — if growth is slower than expected at month 3, 6 and 9: diagnosis checklist,
   and concrete alternative strategies (pivot angle, new format, frequency change, long-form bridge,
   collabs, platform diversification), with triggers for when to apply each.
""",
    },
}


def ideas_batch_instructions(batch_index: int, batches: int, batch_size: int, previous_titles: str) -> str:
    start = batch_index * batch_size + 1
    end = start + batch_size - 1
    intro = ""
    if batch_index == 0:
        intro = """
First, before the ideas, give a concise research brief:
- The top 8 Shorts formats that consistently perform in this niche and why.
- 15 proven hook patterns (with one niche example each, in content language).
- Recurring winning topics/themes, editing styles, and the emotional triggers
  (curiosity, surprise, awe, humor, fear of missing out, relatability, controversy-without-toxicity,
  satisfaction, identity) that drive watch time and shares in this niche.
Then list the ideas.
"""
    avoid = f"\nDo NOT repeat or closely paraphrase these already-generated ideas:\n{previous_titles}\n" if previous_titles else ""
    return f"""{intro}
Generate ideas #{start} to #{end} of a 200-idea list of high viral-potential YouTube Shorts ideas
for this niche. The full list is ranked by audience demand and shareability, so ideas #{start}–#{end}
should belong to tier {batch_index + 1} of {batches} (tier 1 = highest demand & shareability).
Mix formats and content pillars; every idea must be specific (no generic "tips for X").
{avoid}
Output a markdown table with columns:
| # | Title (content language) | Hook — first line on screen/spoken (content language) | Format | Emotional trigger | Demand (1–10) | Shareability (1–10) | Why it will grab attention |
Keep "Why it will grab attention" to one tight sentence (explanation language).
Output exactly {batch_size} rows numbered {start}–{end}. No text after the table.
"""


def build_prompt(module_key: str, profile: dict, explain_lang: str, content_lang: str,
                 prior_context: str = "", batch_instructions: str = "") -> str:
    m = MODULES[module_key]
    task = m["task"].format(batch_instructions=batch_instructions) if "{batch_instructions}" in m["task"] else m["task"]
    context = ""
    if prior_context:
        context = f"""
PREVIOUS STRATEGY OUTPUTS FOR THIS CHANNEL (stay consistent with them, don't repeat them verbatim):
{prior_context}
"""
    return "\n".join([
        BASE_ROLE,
        LANGUAGE_RULES.format(explain_lang=explain_lang, content_lang=content_lang),
        PLATFORM_FACTS,
        channel_profile(profile),
        context,
        task,
        "Format the whole answer in clean Markdown with clear headings.",
    ])
