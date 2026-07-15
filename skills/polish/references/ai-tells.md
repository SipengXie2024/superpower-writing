# AI tells: strip the marks of machine-written prose

The de-AI pass of polish. It removes the signs of AI-generated text so writing
reads as human-written: inflated symbolism, promotional language, em-dash
overuse, rule-of-three, vague attribution, AI vocabulary, hidden actors, negative
parallelism, causal-tail chains, contrast-scaffold density, filler.

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup. Key insight from that page: LLMs guess the
most statistically likely next token, so the output drifts toward the phrasing
that fits the widest variety of cases. That average-of-everything texture is the
tell.

Read Voice Calibration and Register Awareness first, then work the patterns.

## Contents

- **Voice Calibration, Register Awareness, Personality**: calibrate before editing.
- **Content patterns (rules 1-6)**: significance inflation, notability, -ing tails, promotional language, weasel words, outline-like sections.
- **Language and grammar (rules 7-13)**: AI vocabulary, copula avoidance, negative parallelism, rule of three, elegant variation, false ranges, passive voice.
- **Style patterns (rules 14-19+)**: em-dash overuse, boldface, inline-header lists, title case, emojis, curly quotes.

## Voice Calibration (when the user gives a writing sample)

If the user supplies a sample of their own prose, read it before rewriting. Note
sentence-length patterns (short and punchy, long and flowing, mixed), word-choice
level (casual, academic, between), how they open paragraphs, punctuation habits,
recurring phrases, and how they handle transitions.

Then match that voice. Do not just remove AI patterns; replace them with the
author's patterns. If they write short sentences, do not produce long ones. If
they use "stuff" and "things", do not upgrade to "elements" and "components".

Voice matching is a soft guide, never an override of a venue requirement. Three
tiers, in order:

1. **Discipline conventions are HARD.** If a CS / systems / ML venue expects
   third-person plural "we", an author's first-person habit yields.
2. **Target-journal conventions are STRONG.** Nature short paragraphs override an
   author's long-paragraph habit; an ICML / NeurIPS density limit beats an
   author's expansive cadence.
3. **Author personal style is SOFT.** Apply it only where it does not conflict
   with the first two tiers.

When a personal habit clashes with a discipline or venue norm, follow the norm.
This is not a detector-evasion tool: the goal is text the author would have
written, not text engineered to fool a classifier.

## Register Awareness : read before applying the patterns

The patterns below assume blog, marketing, encyclopedic, or conversational prose.
Identify the register first. Some rules misfire on academic, technical, code, or
quoted material, and applying them blindly does more damage than good.

### Quick triage : pick one register

1. **Academic / scholarly.** Multi-author paper, citations or `\cite{}` / `\ref{}`
   markers, third-person plural "we", named methods or results, domain compound
   modifiers ("cold-cache compile time", "per-contract dispatch identity"). LaTeX
   source counts.
2. **Technical / code-adjacent.** Fenced code blocks, function names, file paths,
   command examples, API docs, release notes that name internal systems.
3. **Direct quote, citation, or reference.** Text inside quotation marks
   attributed to someone else, bibliography entries, transcribed dialogue.
4. **Conversational / personal.** First-person singular, casual tone, opinions
   stated directly.
5. **Default (blog / marketing / encyclopedic).** None of the above. Apply all
   patterns.

When in doubt, default to blog/marketing and note the assumption at the end.

### Rules safe in every register

These remove pure formatting noise or chatbot artifacts. Apply everywhere:
18 (emojis), 19 (curly quotes), 20 (collaborative-communication artifacts),
21 (knowledge-cutoff disclaimers), 22 (sycophantic tone), 28 (signposting),
29 (fragmented headers).

### Restraint required in academic / technical register

- **Rule 26 (hyphenated pairs), do not strip** compound modifiers that are field
  conventions. `cold-cache compile time`, `per-contract dispatch identity`,
  `end-to-end retries` are single technical units; removing the hyphen forces a
  re-parse and creates real ambiguity.
- **Voice / soul, do not inject** first-person singular ("I keep coming back
  to..."), opinionated reactions, or casual asides. Multi-author papers use "we"
  and stay third-person. Injecting voice corrupts the authorial collective.
- **Rule 8 (copula avoidance), apply selectively.** "X represents Y" can be
  precise framing, not inflation. Strip "stands as a testament"; keep "represents
  a measured systems effect".
- **Rule 14 (em dashes), apply selectively.** Academic prose sometimes uses an
  em dash where a comma would create ambiguity. Check the alternative reads
  cleaner before swapping.
- **Rule 10 (rule of three), check first.** The trio may be a real enumeration
  (three benchmarks, three contributions). Strip only rhetorical filler.
- **Verb register, preserve scholarly verbs.** Do not informalize `shows /
  demonstrates / preserves / reports / presents` into `lands / dresses up / pulls
  off`. Precise reporting verbs are part of the contract with the reader.
- **Person, never switch.** If the original uses "we", do not rewrite to "I".
- **Rules 30 and 31 (argument rhythm), thin, never strip.** Formal scope
  statements legitimately use causal tails and contrast pairs ("this gives
  integrity, not confidentiality"). Judge by section-level density.

### Skip entirely

- **Code blocks, function names, file paths, commands**, leave verbatim; only
  humanize surrounding prose.
- **Direct quotes**, leave the quoted text exactly; edit only the framing.
- **Bibliography / citations / reference lists**, leave verbatim.

### Mixed-language inputs

Humanize each language segment by its own conventions. Do not translate,
romanize, or strip diacritics.

## Personality (do not overcorrect into soulless prose)

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as
obvious as slop: every sentence the same length, no opinions, no acknowledgment
of uncertainty, reads like a press release. In conversational and default
registers, let a human show: have opinions, vary the rhythm, use "I" when it
fits, be specific about feeling. In academic and technical registers this
restraint flips (see above): the register itself is the voice, and injecting
first-person reaction breaks it.

---

## CONTENT PATTERNS

### 1. Undue emphasis on significance, legacy, broader trends
**Watch:** stands/serves as, is a testament/reminder, a vital/pivotal/crucial
role/moment, underscores its importance, reflects broader, symbolizing its
lasting, setting the stage for, marking a shift, key turning point, evolving
landscape, indelible mark, deeply rooted.
**Problem:** LLMs puff up importance by tying arbitrary facts to a broader topic.
**Before:** established in 1989, marking a pivotal moment in the evolution of regional statistics.
**After:** established in 1989 to collect and publish regional statistics independently.

### 2. Undue emphasis on notability and media coverage
**Watch:** independent coverage, national media outlets, written by a leading
expert, active social media presence.
**Problem:** LLMs list sources without context to assert notability.
**Fix:** replace the list with one concrete, sourced fact (a specific 2024 NYT interview and what was said).

### 3. Superficial analysis with -ing tails
**Watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting...,
contributing to..., fostering..., showcasing....
**Problem:** present-participle phrases tacked on to fake depth.
**Before:** ...resonates with the region's beauty, symbolizing bluebonnets, reflecting the community's deep connection.
**After:** The temple uses blue, green, and gold. The architect said these reference local bluebonnets and the Gulf coast.

### 4. Promotional / advertisement language
**Watch:** boasts a, vibrant, rich (figurative), profound, showcasing, exemplifies,
commitment to, nestled, in the heart of, groundbreaking, renowned, breathtaking,
must-visit, stunning.
**Problem:** LLMs struggle to keep a neutral tone, especially on "heritage" topics.
**Before:** Nestled within the breathtaking region of X, Y stands as a vibrant town with rich cultural heritage.
**After:** Y is a town in the X region, known for its weekly market and 18th-century church.

#### 4a. Promotional language in academic / systems-paper Results prose
The default list misfires here (vibrant, nestled rarely appear in research prose),
but Results sections have their own dialect of inflation. Strip these even when the
register is academic.
**Watch:** overwhelmingly, dominant, captures, sparse side channel, settling RQ in
the affirmative, highly, extensively, robustly, comprehensively, decisively,
conclusively, strikingly, remarkably, definitively, clearly demonstrates.
**Problem:** a 90+ percent measurement already establishes the claim. Inflated
adjectives read as compensation for weak evidence, not confidence in strong
evidence. Reviewers parse adjective inflation as defensiveness.
**Substitutions:**
- `overwhelmingly invariant` → `most bytes are invariant` (or state the percent)
- `the dominant case, not a sparse side channel` → `the common case, not a corner case`
- `settling RQ in the affirmative` → `answering RQ`
- `clearly demonstrates / robustly shows / decisively establishes` → `shows`
- `highly effective` → state the metric directly

The `common case / corner case` pair is the systems-native contrast that keeps the
rebuttal-of-objection function without promotional language.

### 5. Vague attribution and weasel words
**Watch:** Industry reports, Observers have cited, Experts argue, Some critics
argue, several sources (when few are cited).
**Problem:** opinions attributed to vague authorities without a specific source.
**Fix:** name the source and date, or drop the framing. "Experts believe it plays a crucial role" → a specific 2019 survey by a named body.

### 6. Outline-like "Challenges and Future Prospects" sections
**Watch:** Despite its... faces several challenges, Despite these challenges,
Challenges and Legacy, Future Outlook.
**Problem:** formulaic filler sections.
**Fix:** replace with concrete, dated events (a specific project started in 2022 to address recurring floods).

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI vocabulary"
**Watch:** actually, additionally, align with, crucial, delve, emphasizing,
enduring, enhance, fostering, garner, highlight (verb), interplay,
intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase,
tapestry, testament, underscore (verb), valuable, vibrant.
**Problem:** these appear far more often in post-2023 text and co-occur.
**Fix:** delete or replace with a plain equivalent; recast the sentence around a concrete fact.

### 8. Avoidance of "is" / "are" (copula avoidance)
**Watch:** serves as / stands as / marks / represents [a], boasts / features /
offers [a].
**Problem:** elaborate constructions substituted for a simple copula.
**Before:** Gallery 825 serves as the exhibition space and boasts over 3,000 square feet.
**After:** Gallery 825 is the exhibition space. It has four rooms totaling 3,000 square feet.

### 9. Negative parallelism and tailing negations
**Problem:** "Not only... but...", "It's not just about X, it's Y" are overused. So
are clipped tailing negations ("no guessing", "no wasted motion") tacked on instead
of written as a real clause.
**Before:** It's not merely a song, it's a statement. / The options come from the selected item, no guessing.
**After:** The heavy beat adds to the aggressive tone. / The options come from the selected item without forcing the user to guess.

### 10. Rule of three overuse
**Problem:** ideas forced into groups of three to seem comprehensive.
**Before:** keynote sessions, panel discussions, and networking opportunities; innovation, inspiration, and industry insights.
**After:** The event includes talks and panels, with time for informal networking.

### 11. Elegant variation (synonym cycling)
**Problem:** the same referent renamed every mention (protagonist, main character, central figure, hero).
**Fix:** name it once, use a pronoun after. "The protagonist faces many challenges but eventually triumphs and returns home."

### 12. False ranges
**Problem:** "from X to Y" where X and Y are not on a meaningful scale.
**Before:** from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter.
**After:** The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Passive voice and subjectless fragments
**Problem:** the actor is hidden or the subject dropped ("No configuration file needed", "The results are preserved automatically"). Rewrite when active voice is clearer.
**Before:** No configuration file needed. The results are preserved automatically.
**After:** You do not need a configuration file. The system preserves the results automatically.

## STYLE PATTERNS

### 14. Em-dash overuse
**Problem:** LLMs use em dashes (,) more than humans, mimicking punchy sales
writing. Most rewrite more cleanly with commas, periods, or parentheses.
**Before:** promoted by Dutch institutions,not by the people themselves,even in official documents.
**After:** promoted by Dutch institutions, not by the people themselves, even in official documents.

### 15. Overuse of boldface
**Problem:** phrases emphasized in boldface mechanically.
**Fix:** remove the bold; let sentence structure carry the emphasis.

### 16. Inline-header vertical lists
**Problem:** list items that start with a bolded header followed by a colon, each restating the header.
**Fix:** fold into prose. "The update improves the interface, speeds up load times, and adds end-to-end encryption."

### 17. Title case in headings
**Problem:** every main word capitalized.
**Before:** ## Strategic Negotiations And Global Partnerships
**After:** ## Strategic negotiations and global partnerships

### 18. Emojis
**Problem:** headings or bullets decorated with emojis. Remove them and recast as plain prose.

### 19. Curly quotation marks
**Problem:** curly quotes (“...”) instead of straight ("..."). Replace with straight quotes.

## COMMUNICATION PATTERNS

### 20. Collaborative-communication artifacts
**Watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!,
Would you like..., let me know, here is a....
**Problem:** chatbot correspondence pasted as content. Delete it; open with the actual content.

### 21. Knowledge-cutoff disclaimers
**Watch:** as of [date], up to my last training update, while specific details are
limited/scarce, based on available information.
**Problem:** AI disclaimers left in text. Replace with the sourced fact, or delete.

### 22. Sycophantic / servile tone
**Problem:** overly positive, people-pleasing language ("Great question!", "That's an excellent point").
**Fix:** delete the flattery; state the substance.

## FILLER AND HEDGING

### 23. Filler phrases
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "has the ability to process" → "can process"
- "It is important to note that the data shows" → "The data shows"

### 24. Excessive hedging
**Problem:** over-qualifying ("could potentially possibly be argued that... might have some effect").
**Fix:** "The policy may affect outcomes." Keep hedges that are load-bearing in academic prose.

### 25. Generic positive conclusions
**Problem:** vague upbeat endings ("The future looks bright. Exciting times lie ahead.").
**Fix:** replace with a concrete plan ("The company plans to open two more locations next year"), or cut.

### 26. Hyphenated word-pair overuse
**Watch:** third-party, cross-functional, client-facing, data-driven,
decision-making, well-known, high-quality, real-time, long-term, end-to-end.
**Problem:** AI hyphenates common pairs with perfect consistency; humans do not.
Less common or technical compound modifiers are fine to hyphenate, and in
academic / technical register, do not strip domain compounds (see Register
Awareness).

### 27. Persuasive-authority tropes
**Watch:** the real question is, at its core, in reality, what really matters,
fundamentally, the deeper issue, the heart of the matter.
**Problem:** these pretend to cut through noise, but the next sentence just
restates an ordinary point with extra ceremony. Drop the framing, keep the point.

### 28. Signposting and announcements
**Watch:** let's dive in, let's explore, let's break this down, here's what you
need to know, without further ado.
**Problem:** the model announces what it will do instead of doing it. Delete the
announcement; state the content.

### 29. Fragmented headers
**Problem:** a heading followed by a one-line paragraph that just restates the
heading before the real content. Delete the restatement.

## ARGUMENT-RHYTHM PATTERNS

The patterns above are local, a word, a phrase, one sentence. The two below live
at paragraph and section scale. Each instance is grammatical and often defensible
alone; the tell is density, the same argumentative move arriving sentence after
sentence. Judge with counts (see Density diagnosis) and thin toward a keep ratio,
never to zero.

### 30. Causal-tail chains
**Watch:** consequence clauses chained onto claim after claim with ", so ...",
", which means ...", ", meaning that ...".
**Problem:** the model attaches a consequence to nearly every claim (mechanism, so
implication). Any one is fine; the uniform cadence reads as generated. In one
13-page systems paper the pattern appeared 42 times in ~380 sentences.
**Fix:** keep the tail where the inference is non-obvious or closes a paragraph.
Rewrite the rest: split into two sentences and let the reader infer, fold the
consequence into a relative clause, prepose the cause with "Because...", or delete
a tail the main clause already implies.
**Before:** ...the client's TLS session terminates there, so the host never holds the interaction in the clear. The control call carries only numeric counters, so it cannot encode text.
**After:** ...the client's TLS session terminates there. The host never holds the interaction in the clear. The control call carries only numeric counters that cannot encode text.

### 31. Contrast-scaffold density
**Watch:** "A rather than B", "A, not B", "A instead of B" recurring through a
section.
**Problem:** the model pairs nearly every positive claim with a rejected
alternative. Rule 9 catches the conversational forms; this is the formal-register
sibling, and it survives most de-AI passes because each instance reads as scholarly
precision. One Results section carried 14 such pairs.
**Fix, triaged per instance:**
- Positive clause already implies the rejected alternative → delete the tail.
  "paid once per session rather than per request" → "paid once per session".
- Contrast separates two readings a careful reader could take → keep.
  "application-layer, not network-layer egress confinement".
- Contrast carries the thesis → keep. "removes the capability rather than
  detecting its use".

Cut roughly half. Cutting to zero erases boundaries the reader needs.

## Density diagnosis (documents over about two pages)

Rules 30, 31, and rule 10 at scale are density problems: instance-by-instance
editing misjudges them because no single instance is wrong. Measure first, then
edit to a target.

1. Count candidates with a grep pass: `, so `, `rather than`, `, not `, `instead`,
   and a triad pattern such as `\w+, [^,.]+, (and|or) `. Tally per section.
2. Flag hotspots: a paragraph with three or more hits, or a sentence carrying two
   patterns at once. Fix hotspots first.
3. Compute words-per-sentence mean and standard deviation per section. A standard
   deviation below roughly 40 percent of the mean suggests metronomic rhythm.
4. Set a keep ratio before editing, usually 30 to 50 percent of the rhetorical
   instances, so the survivors are the load-bearing ones: announced enumerations,
   thesis contrasts, substantive disambiguations, factual artifact lists. Driving
   a pattern to zero is over-editing, which is its own tell.
5. After editing, re-count and audit the replacements. If more than a third of the
   fixes share one substitute shape (all semicolon splices, say), the pattern has
   changed clothes, not left. Diversify: sentence splits, relative-clause folds,
   preposed causes, plain deletions.
