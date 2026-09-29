# Formalized "easy English" standards, and research on making LLM output understandable

Researched 2026-08-13. Primary sources where reachable; secondary sources flagged. Bare URLs inline.

## Findings summary

1. **Yes — several formalized standards exist, at different levels of rigor.** (High confidence.)
   - **ASD-STE100 Simplified Technical English** is the most rule-hard: 53 numbered writing rules plus a ~900-word controlled dictionary (one meaning per word), owned by ASD (Brussels), built for aerospace maintenance docs. Free to download after registration.
   - **ISO 24495-1:2023 "Plain language"** is the first international plain-language standard (ISO/TC 37): four governing principles (relevant, findable, understandable, usable) with guidelines. Paywalled.
   - **The Federal Plain Language Guidelines** (US, PLAIN/GSA, backed by the Plain Writing Act of 2010) are the most-used government ruleset: concrete rules ("use active voice", "use 'must' not 'shall'", "use pronouns", short sentences/sections). Free.
   - Others: **Inclusion Europe Easy-to-Read standards** (intellectual-disability audience), **GOV.UK style guide** (reading-age-9 target, banned-words list), **Plain English Campaign** guides (15–20-word average sentence), **WCAG 3.1.5** (lower-secondary reading level, AAA), and historical controlled vocabularies (**Ogden's Basic English** 850 words, **VOA Special English** ~1,500 words).
2. **Mechanical checkability splits the field.** (High confidence.) Controlled languages (STE, Basic English, VOA word list) are largely lintable — closed vocabulary, sentence-length caps, part-of-speech restrictions — and commercial STE checkers exist. Plain-language standards (ISO 24495-1, federal guidelines, Easy-to-Read) are principle-based; individual rules (passive voice, sentence length, word substitutions, readability formulas) are checkable, but full compliance requires human judgment (audience fit, testing). Everything is public and free except the ISO standard.
3. **The AI-specific literature is real and growing fast, but lopsided.** (Medium-high confidence.) Dozens of studies measure the *readability scores* of LLM output (consistently too high — college level for medical Q&A; prompting to "6th grade" improves but usually undershoots the target, landing ~8th–9th grade). Benchmarks show off-the-shelf LLMs match fine-tuned simplification models (BLESS). Precise grade-level *control* is an open research problem (prompting alone is coarse; fine-tuning/RL helps). Studies that measure actual *human comprehension* of LLM-simplified text — not just formula scores — are rare but now appearing: a 2025 prospective controlled trial of LLM-simplified oncologic CT reports found large comprehension gains (aOR ≈ 13). No study found that targets a *formal standard* (STE, ISO 24495-1) with an LLM and then measures comprehension — that's the gap.

---

## ASD-STE100 Simplified Technical English

- **Owner/maintainer:** AeroSpace and Defence Industries Association of Europe (ASD), Brussels; maintained by the Simplified Technical English Maintenance Group (STEMG). Current version: Issue 9, January 2025. https://www.asd-ste100.org/about_STE.html
- **Domain:** commercial-aviation maintenance documentation (origins late 1970s, AECMA Simplified English); now used across defence and other industries. Aimed at readers who are non-native English speakers.
- **Rules (concrete):** two parts —
  - **53 writing rules in 9 sections** (words, noun phrases, verbs, sentences, procedures, descriptive writing, warnings/cautions, punctuation, writing practices). Load-bearing examples: max **20 words per sentence in procedural text, 25 in descriptive text**; max **6 sentences per paragraph**, one topic per paragraph; use only approved verb forms (no -ing forms as verbs, no passive in procedures); use articles; one instruction per sentence in procedures. Sentence/paragraph limits confirmed at https://www.tcworld.info/e-magazine/technical-writing/asd-ste100-issue-9-setting-a-standard-for-technical-documentation and the standard itself https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf
  - **Controlled dictionary:** ~900 approved words, each with **one meaning and one part of speech** ("close" is only a verb, etc.), plus ~1,200 unapproved words with approved alternatives; writers may add company-specific Technical Names and Technical Verbs.
- **Availability:** full text free of charge; official copy obtained via a request form on asd-ste100.org (the Issue 9 PDF is served from the site). Not paywalled.
- **Mechanically checkable:** mostly yes — closed vocabulary + hard numeric limits + POS restrictions make it the most lintable standard on this list. Commercial checkers exist (Boeing Simplified English Checker, Etteplan HyperSTE, Congree); list per https://en.wikipedia.org/wiki/Simplified_Technical_English (secondary source; individual checker claims unverified this session). Residual human judgment: choosing Technical Names, and rules like "one topic per paragraph".
- **Evidence:** Chervak, Drury & Ouellette (1996), "Simplified English for Aircraft Workcards" — 16 workcards × 175 practicing aircraft maintenance technicians, between-subjects comprehension test: comprehension significantly improved with Simplified English, with the largest error reductions on difficult workcards and for non-native speakers. https://journals.sagepub.com/doi/abs/10.1177/154193129604000502 Boeing also ran empirical evaluations of controlled language in the 1990s: https://mt-archive.net/90/CLAW-1996-Holmback.pdf

## ISO 24495-1:2023 — Plain language, Part 1: Governing principles and guidelines

- **Owner/maintainer:** ISO Technical Committee 37 (Language and terminology); drafted by ~50 plain-language experts from 25 countries via the International Plain Language Federation's working group. https://www.iso.org/standard/78907.html https://www.iplfederation.org/iso-standard/
- **Domain:** general — any document for any audience, language-agnostic (examples in English).
- **Rules (concrete):** four governing principles, each with guidelines: readers get what they need (**relevant**); readers can easily find what they need (**findable**); readers can easily understand what they find (**understandable**); readers can easily use the information (**usable**). Principle names per https://www.iplfederation.org/iso-standard/
- **Sibling parts:** Part 2 (2025, legal communication), Part 3 (2026, science writing), Part 4 (in development, organizational implementation) — https://www.iso.org/standard/90061.html
- **Availability:** **paywalled** (sold by ISO and national bodies; iso.org returned 403 to automated fetch, price unverified — reseller listings confirm it is for sale, e.g. https://standards.iteh.ai/catalog/standards/iso/5266c5b6-e44a-4e68-9600-82b2a8932fc2/iso-24495-1-2023). I could see the principle names and scope via the IPLF and reseller previews; I could **not** read the guideline text itself. Full-guideline detail here is thin for that reason.
- **Mechanically checkable:** no. It is process- and outcome-oriented (know your audience, structure for findability, test the document), not a rule grammar. Individual downstream practices are checkable, but conformance is not.
- **Evidence:** the standard is expert consensus distilling the plain-language research base rather than itself validated; see plain-language evidence below.

## Federal Plain Language Guidelines (US)

- **Owner/maintainer:** PLAIN (Plain Language Action and Information Network), an interagency group; content historically at plainlanguage.gov, now folded into GSA's digital.gov with the source archived on GitHub. https://digital.gov/guides/plain-language Legal basis: **Plain Writing Act of 2010**, which requires federal agencies to use "clear Government communication that the public can understand and use."
- **Domain:** US government documents for the public.
- **Rules (concrete):** the March 2011 Federal Plain Language Guidelines (rev. May 2011) enumerate, among others: write for your average reader; organize to serve the reader; use useful headings; **use "you" and other pronouns**; **use active voice**; **use short sections and short sentences**; use the simplest tense; use strong active verbs; omit excess words; use concrete, familiar words; **use "must" for requirements, avoid "shall"**; place words carefully (subject–verb–object close together); avoid double negatives; minimize cross-references; use lists and tables; write for the web distinctly. Full 2011 text (archived mirror): https://wid.org/wp-content/uploads/2022/03/FederalPLGuidelines.pdf
- **Availability:** free, public domain.
- **Mechanically checkable:** partially. Passive-voice ratio, sentence length, "shall" bans, hidden-verb nominalizations, word-substitution lists are lintable (and tools like https://www.plainlanguage.gov checklists exist); "organize for the reader" and the guidelines' own capstone rule — **test your content with users** — are not.
- **Evidence:** Kimble, *Writing for Dollars, Writing to Please* (2nd ed. 2023) aggregates ~60 empirical studies: readers understand plain-language versions better and faster, prefer them, and comply more; organizations save money. https://cap-press.com/books/isbn/9781531024543/Writing-for-Dollars-Writing-to-Please summary at https://centerforplainlanguage.org/writing-for-dollars/ (The book itself is paywalled; the studies it cites are scattered across journals. I did not verify individual studies — thin at the study level, robust at the aggregate level.)

## GOV.UK style guide / GDS content design (UK)

- **Owner/maintainer:** Government Digital Service (GDS), Cabinet Office. Guidance for GOV.UK publishers: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/ and the A-to-Z style guide https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- **Domain:** UK government web content.
- **Rules (concrete):** write for a **reading age of ~9** (rationale: by age 9 most people have a ~5,000-word shape-recognized core vocabulary; adults read those words fastest — this is about the average UK adult, not children); plain-English word substitutions with an explicit banned/discouraged word list ("deliver" → make/create/provide, "leverage" → influence/use, "facilitate" → say specifically how, "purchase" → buy, "assist" → help, "approximately" → about); front-load sentences; explain jargon on first use.
- **Availability:** free.
- **Mechanically checkable:** substantially — the word list and readability targets are lintable (GDS historically used tools of this kind); audience-fit judgments are not.
- **Evidence:** GDS cites literacy statistics and usability testing; I did not locate a controlled GDS comprehension study this session (**thin**).

## Plain English Campaign (UK, private)

- **Owner/maintainer:** Plain English Campaign Ltd (founded 1979, Chrissie Maher); its **Crystal Mark** (1990) is a paid certification of document clarity. https://www.plainenglish.co.uk/ https://www.plainenglish.co.uk/services/crystal-mark
- **Rules (concrete):** free guide "How to write in plain English": **average sentence length 15–20 words**; prefer active verbs; use "you" and "we"; everyday words; bullet lists over long sentences; explain technical terms; clear headings. Free guides: https://www.plainenglish.co.uk/free-guides mirrored PDF: https://mstrust.org.uk/sites/default/files/plain_english_campaign_how_to_write_plain.pdf
- **Availability:** guides free; Crystal Mark certification is a paid service (human review, not a published rule grammar).
- **Mechanically checkable:** the guide's core rules yes; the Crystal Mark no (proprietary human judgment).
- **Evidence:** advocacy-driven; no controlled studies of its own found (**thin** — relies on the general plain-language evidence base).

## Inclusion Europe — "Information for all" European Easy-to-Read standards

- **Owner/maintainer:** Inclusion Europe (European association of people with intellectual disabilities and their families), produced 2010 under the EU "Pathways" project. Full text free: https://www.inclusion-europe.eu/wp-content/uploads/2017/06/EN_Information_for_all.pdf overview: https://www.inclusion-europe.eu/easy-to-read/
- **Domain:** information for people with intellectual disabilities (also serves low-literacy and second-language readers). German sibling: Leichte Sprache (not covered here).
- **Rules (concrete):** short sentences (one idea per sentence); no jargon; explain hard words when unavoidable; **same word for the same thing throughout**; active voice; no metaphors/foreign words; large clear font, generous white space; illustrative images; **test documents with people with intellectual disabilities before publishing**; the easy-to-read logo may be used by publications that comply.
- **Availability:** free.
- **Mechanically checkable:** partially (sentence length, word lists, layout); the mandatory user-testing step is inherently human.
- **Evidence:** grounded in participatory practice; controlled comprehension studies of the standard itself not found this session (**thin**).

## WCAG 3.1.5 Reading Level (W3C)

- **Owner/maintainer:** W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html
- **Rule (verbatim):** "When text requires reading ability more advanced than the lower secondary education level after removal of proper names and titles, supplemental content, or a version that does not require reading ability more advanced than the lower secondary education level, is available." Conformance level **AAA**. "Lower secondary" = 7–9 years of schooling (UNESCO ISCED).
- **Mechanically checkable:** approximately — readability formulas estimate the level, but the Understanding document defers to qualified-teacher evaluation; formula estimates are a proxy.
- **Availability:** free.

## Controlled vocabularies (historical/broadcast)

- **Ogden's Basic English (1930):** Charles K. Ogden, *Basic English: A General Introduction with Rules and Grammar*. **850 words** + a small operator-verb grammar (18 verbs); claim: 90% of Pocket Oxford concepts expressible. Public domain; word list at https://zbenglish.net/sites/basic/basiceng.html Fully lintable (closed vocabulary). Built as an international auxiliary language; comprehension evidence is period-anecdotal (**thin**).
- **VOA Special English (1959– , now "Learning English"):** Voice of America broadcasts using a **~1,500-word core vocabulary**, short declarative sentences, one idea per sentence, ~two-thirds normal speaking speed (~90 wpm). Official Word Book PDF: https://docs.voanews.eu/en-US-LEARN/2014/02/15/7f8de955-596b-437c-ba40-a68ed754c348.pdf Lintable (closed vocabulary). Longevity is the practical evidence; no controlled studies found (**thin**).
- **Attempto Controlled English (ACE):** University of Zurich; a controlled English with a **formal, machine-parseable semantics** (the APE parser translates ACE to first-order logic). https://attempto.ifi.uzh.ch/site/ Fully mechanically checkable by construction — but its goal is unambiguous machine interpretation, not human ease; included as the far end of the checkability spectrum.
- **CEFR (Council of Europe):** not an English simplification standard, but the dominant proficiency-leveling framework (A1–C2) used as the *target scale* in LLM-control research below. https://www.coe.int/en/web/common-european-framework-reference-languages

### Checkability/paywall matrix

| Standard | Mechanically checkable? | Full text free? |
|---|---|---|
| ASD-STE100 | Mostly (vocab + numeric limits; checkers exist) | Yes (registration) |
| ISO 24495-1 | No (principles/process) | **No — paywalled** |
| Federal Plain Language Guidelines | Partially | Yes |
| GOV.UK style guide | Substantially (word list, reading age) | Yes |
| Plain English Campaign guide | Core rules yes; Crystal Mark no | Guides yes; certification paid |
| Inclusion Europe Easy-to-Read | Partially (user testing required) | Yes |
| WCAG 3.1.5 | Approximately (formula proxy) | Yes |
| Basic English / VOA / ACE | Fully (closed vocab / parser) | Yes |

---

## AI/LLM-specific research on understandable output

### Readability of raw LLM output (measured by formulas)

- Default chatbot answers to health questions consistently score above recommended levels (AMA/NIH recommend ~6th grade for patient materials). Representative: ChatGPT 3.5 could not reach 6th-grade level on craniofacial patient materials without refinement; GPT-4 improved after priming with 6th-grade examples. https://journals.lww.com/prsgo/fulltext/10.1097/gox.0000000000005575~validation-of-chatgpt-35-as-a-tool-to-optimize-readability
- Prompting "rewrite at a 6th-grade level" reliably *improves* scores (~4 grade levels in one otolaryngology study) but typically lands ~9th grade — better, still above target. https://www.sciencedirect.com/science/article/abs/pii/S0196070924002886
- Cross-model comparison (ChatGPT vs Gemini vs Claude) on 60 patient-education materials: all improved readability over originals; Gemini and Claude more than ChatGPT; simplified outputs remained ~92–95% clinically appropriate. https://www.jmir.org/2025/1/e69955
- Systematic review of ChatGPT radiology-report simplification: https://onlinelibrary.wiley.com/doi/10.1111/1754-9485.70076

### Controlling readability / grade level (NLP research)

- **Measuring and Modifying the Readability of English Texts with GPT-4** (arXiv 2410.14028): GPT-4's own readability *judgments* correlate with human judgments (r ≈ 0.76) better than traditional formulas; it can shift text to coarse target levels but not precisely. https://arxiv.org/abs/2410.14028
- **Generating summaries/simplifications at specified grades:** Controlling Pre-trained Language Models for Grade-Specific Text Simplification (arXiv 2305.14993) https://arxiv.org/abs/2305.14993 ; ReadCtrl — readability-controlled instruction tuning (arXiv 2406.09205) https://arxiv.org/abs/2406.09205 ; document-level readability+coherence (arXiv 2412.18655) https://arxiv.org/abs/2412.18655
- **From Tarzan to Tolkien** (arXiv 2406.03030): controlling CEFR proficiency level of GPT-4/Llama-2/Mistral output for language learners; few-shot prompting vs fine-tuning vs RL — the open models need fine-tuning to match GPT-4's prompt-only control. https://arxiv.org/abs/2406.03030
- **BLESS** (EMNLP 2023, arXiv 2310.15773): 44 LLMs benchmarked on sentence simplification (Wikipedia/news/medical, few-shot); best LLMs, though never trained for simplification, match dedicated state-of-the-art simplification systems. https://aclanthology.org/2023.emnlp-main.821/ https://arxiv.org/abs/2310.15773
- Pre-LLM foundations the above build on: SARI metric (Xu et al. 2016) https://aclanthology.org/Q16-1029/ ; Newsela corpus critique of Simple-Wikipedia-based research (Xu et al. 2015) https://aclanthology.org/Q15-1021/ ; ASSET multi-reference dataset (Alva-Manchego et al. 2020) https://aclanthology.org/2020.acl-main.424/ (URLs from memory of standard ACL IDs — spot-check before citing onward.)

### Plain-language summarization of biomedical text

- Guo et al., Automated Lay Language Summarization of Biomedical Scientific Reviews (AAAI 2021) — Cochrane-based; code/data: https://github.com/qiuweipku/Plain_language_summarization
- **CELLS** (arXiv 2211.03818): largest parallel corpus for lay-language generation (63k expert-written abstract/lay pairs, 12 journals); retrieval augmentation for definitions. https://arxiv.org/abs/2211.03818
- **Factuality is the recognized failure mode:** FactPICO — factuality evaluation of LLM plain-language summaries of medical evidence (arXiv 2402.11456) https://arxiv.org/abs/2402.11456 ; PlainQAFact (arXiv 2503.08890) — notes "elaborative explanation" (adding background absent from the source) breaks standard factuality metrics. https://arxiv.org/abs/2503.08890
- **Are LLM-generated plain language summaries truly understandable?** (arXiv 2505.10409) — human evaluation of LLM PLS. https://arxiv.org/abs/2505.10409 (not read in full this session — **thin**).
- Jeblick et al. (arXiv 2212.14882), the field's early anchor: 15 radiologists rated ChatGPT-simplified radiology reports mostly factually correct, complete, and not harmful — but with instances of incorrect statements, missed key findings, and potentially harmful passages. https://arxiv.org/abs/2212.14882 Follow-up human evaluation of self-correction: https://arxiv.org/abs/2406.18859

### Studies measuring actual human comprehension of LLM-simplified text

This is the thinnest and most decisive slice — most of the literature stops at formula scores.

- **Prospective controlled (quasi-randomized) trial, Radiology 2025:** 200 cancer patients alternately assigned standard vs Llama-3.3-70B-simplified CT restaging reports (radiologist-reviewed). Simplified arm: better comprehension (adjusted OR ≈ 13.3), lower cognitive workload, reading time 7 min → 2 min. https://pubs.rsna.org/doi/10.1148/radiol.251844 https://pubmed.ncbi.nlm.nih.gov/41251553/
- **Randomized 3-period crossover** (31 breast-cancer patients/caregivers): preference for LLM-optimized clinical-trial descriptions over ClinicalTrials.gov originals — preference, not comprehension, as primary endpoint. https://dailynews.ascopubs.org/do/patients-prefer-ai-simplified-clinical-trial-information-standard-trial-descriptions
- **Registered RCTs in flight:** oncOPAL — LLM plain-language patient synopses in hematology/oncology, comprehension endpoint https://clinicaltrials.gov/study/NCT07519811 ; AI-INFOCARE / AI-MEDTALK protocols https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12680933/
- Chervak 1996 (above) is the pre-LLM existence proof that a formal controlled language yields measurable comprehension gains in the field; no LLM-era equivalent targeting STE or ISO 24495-1 was found. (Verified absence only to the depth of this search.)

### Synthesis for part 3

Verified pattern: (a) raw LLM output is too hard for general audiences by formula standards; (b) prompting reliably moves readability in the right direction but cannot hit numeric grade targets precisely — fine-tuning/RL closes some of the gap; (c) LLM simplification quality now matches dedicated simplification systems; (d) the binding constraint has shifted from fluency to *factuality* of simplified output; (e) genuine comprehension outcomes are just starting to be measured, and the first controlled trial is strongly positive. Nobody appears to be using the formal standards of part 1 as LLM output targets, despite STE being exactly the kind of closed, lintable spec an LLM pipeline could verify against.

---

## Candidate follow-up tickets

- **Can an LLM + STE checker loop produce conformant ASD-STE100 output?** STE is closed-vocabulary and numerically constrained — a lint-and-regenerate loop is buildable today; would give a *verifiable* "understandable English" mode rather than vibes-based simplification.
- **What do the ISO 24495-1 guidelines actually say beneath the four principles?** The full text is paywalled; buying one copy (~CHF 100–200, unverified) would settle whether it adds checkable substance over the free federal guidelines.
- **Which of Kimble's ~60 studies measured comprehension (vs preference/cost), and how strong are they methodologically?** The aggregate claim carries the whole plain-language evidence case; the primary studies were not individually verified here.
- **Do readability formulas predict comprehension at all for LLM-generated text?** arXiv 2410.14028 shows LLM judgments beat formulas on human-judged readability; whether Flesch-Kincaid on LLM output predicts *measured comprehension* is untested and underpins most of the medical literature above.
- **What did "Are LLM-generated plain language summaries truly understandable?" (arXiv 2505.10409) actually find?** Cited but not read; it is the closest existing human-comprehension evaluation of LLM PLS.
- **Is there a validated prompt/system-prompt pattern for chatbot answers (not document rewriting) at a target level?** Nearly all studies rewrite existing documents; the "make the assistant's own answers understandable" case — the one relevant to agent skills — is unmapped.
- **German Leichte Sprache DIN standard (DIN 8581-1:2024?) as a template:** Germany reportedly formalized easy language as a DIN standard — unverified; if true, it is a second ISO-grade ruleset and possibly more concrete than ISO 24495-1.
- **Do STE checkers (HyperSTE, Boeing SEC) expose APIs usable in an LLM pipeline, and what do they cost?** Checker landscape cited only via Wikipedia here.
- **CEFR-targeted generation quality (arXiv 2406.03030 follow-ups):** CEFR may be a better control scale than US grade levels for global audiences; how reliable are CEFR classifiers used as reward models?
