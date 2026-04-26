# Venue-Specific Style and Formatting Guide

## Overview

This document consolidates venue-specific writing conventions, structural expectations, and formatting requirements for the most common computer-science publication targets: ML conferences, systems conferences, HCI and software-engineering venues, and journals (both broad-audience and ACM/IEEE Transactions). Use it alongside your target venue's official author guidelines. The guidance here covers the decisions that matter most during drafting and revision: structure, page limits, anonymization, voice, and the implicit expectations reviewers apply.

## Venue Class Decision

Before you write, decide which venue class you are targeting. The class determines structure, length, voice, and even which sections are required.

**Journal vs. Conference.** Journals (Nature, ACM TOCS, IEEE TPAMI) have generous or no page limits, separate Results and Discussion, and expect a polished narrative arc. Conferences have hard page caps (typically 8--12 pages plus unlimited appendices), combine Results and Discussion into a single Experiments section, and front-load contributions.

**ML vs. Systems vs. HCI.** ML venues (NeurIPS, ICML, ICLR, CVPR) emphasize novelty claims, ablation studies, and reproducibility checklists. Systems venues (SOSP, OSDI, ASPLOS, NSDI, SIGCOMM, ATC, EuroSys) emphasize end-to-end evaluation, artifact evaluation, and artifact reproducibility badges. HCI and SE venues (CHI, UIST, ICSE, FSE) emphasize study design validity, participant demographics, and qualitative reporting rigor (SRQR, COREQ).

**Quick triage questions:**
1. Is there a hard page limit? If yes, it is a conference or symposium.
2. Does the call for papers mention "artifact evaluation" or "AE"? If yes, it is a systems venue.
3. Does the call for papers require a "broader impact" or "ethics" section? If yes, it is likely an ML venue (NeurIPS, ICML, ICLR).
4. Does the call for papers mention "reflexivity" or "qualitative analysis"? If yes, it is an HCI or SE venue.

## Conference Papers

All CS conferences share a set of generic expectations regardless of subfield.

**Page limits.** Most top-tier CS conferences allow 8--12 pages of main content (text + figures + tables) plus unlimited supplementary material. The page limit is strict; exceeding it is a desk-reject trigger at most venues. References may or may not count toward the limit. Check the call for papers carefully.

**Double-blind review.** The majority of top CS venues use double-blind review. You must anonymize your paper: remove author names and affiliations from the title page, redact self-references that would identify you ("in our previous work [1]" becomes "prior work [1]"), and avoid grant numbers or institution-identifying details. Supplementary code repositories should also be anonymized (e.g., use a throwaway GitHub account). Some systems venues (e.g., SOSP, OSDI) are exceptions and use single-blind review, but the trend is moving toward double-blind.

**Supplementary material.** Appendices, supplementary PDFs, and code repositories are standard. Reviewers are not obligated to read supplementary material, so all claims essential to the paper's contribution must be supported in the main text. Use appendices for proofs, extended experimental tables, and additional qualitative examples.

**Camera-ready vs. submission.** The submitted version must be anonymized. The camera-ready version (accepted paper) adds author names, affiliations, and funding acknowledgments. Budget time for this conversion; it is more than cosmetic when you have redacted self-citations throughout. Camera-ready papers also need to incorporate reviewer feedback, which may require restructuring sections or adding experiments requested during the rebuttal.

**Formatting templates.** Use the official LaTeX template for the venue (e.g., `neurips_2024.sty`, `acmart.cls` with the appropriate conference option). Do not fight the template. Reviewers notice formatting violations and interpret them as carelessness. Common mistakes include changing margins, adjusting font sizes, or using non-standard packages that alter the template layout.

**Rebuttal phase.** Most top CS conferences include a rebuttal period (typically 7--14 days) where authors respond to reviewer questions. During this period, you may run additional experiments requested by reviewers and post results in the rebuttal. Keep responses concise and address every reviewer concern directly. Do not dismiss reviewer criticisms; acknowledge them and explain how you will address them in the camera-ready version.

## ML Conferences

This section covers NeurIPS, ICML, ICLR, and CVPR (and their variants such as NeurIPS Datasets, ICML Workshop, CVPR Vision-and-Language). These venues share a common structural DNA.

### Page limits and template

- **NeurIPS**: 9-page main text + 1-page ethics statement; references and appendix unlimited. Uses `neurips_2024.sty` (or the current year's equivalent). Single-column.
- **ICML**: 8-page main text; references and appendix unlimited. Uses `icml2024.sty`. Single-column.
- **ICLR**: Similar to ICML; exact page count varies by year. Uses OpenReview for submission and discussion.
- **CVPR**: 8-page main text + 2 pages of references. Uses `cvpr.sty`. Double-column.

### Expected section structure

The canonical order is: Abstract, Introduction, Related Work (sometimes moved to appendix), Method, Experiments, Conclusion, Broader Impact / Ethics (if required). Some venues allow Related Work after Method or at the end; check recent accepted papers for conventions.

**Abstract** (150--200 words). State the problem, method, and key quantitative result in one paragraph. No citations, no undefined abbreviations. The abstract should stand alone and make sense to someone who reads only the title and abstract. Keep it direct: "We propose X, which achieves Y% improvement on benchmark Z."

**Introduction** (roughly 1 page). State the problem, motivate it, preview the solution, and list contributions as a numbered list: "Our contributions are: (1) ..., (2) ..., (3) ..." This numbered-contribution list is a near-universal convention at ML venues and reviewers look for it. Each contribution should be concrete and verifiable: "We propose a sparse attention mechanism that reduces memory from O(n^2) to O(n log n)" is better than "We improve efficiency."

**Method** (2--3 pages). Present the technical approach with equations and optionally pseudocode. Use consistent mathematical notation. Architecture diagrams are expected. Complexity analysis (time and space) is common. Structure this section to map onto your contribution list: if contribution (1) is the sparse attention mechanism, the Method should describe it in detail. Use Algorithm environments for pseudocode. Define all notation in a table if you introduce many symbols.

**Experiments** (2--3 pages). This section replaces the journal's separate Results and Discussion. Typical subsections:
- Experimental setup: datasets, baselines, hyperparameters, compute resources (GPU count, training time). Report random seeds and number of runs.
- Main results: comparison with baselines on standard benchmarks. Use tables with bold-best and underlined-second-best conventions.
- Ablation studies: systematically removing or replacing components to demonstrate each one matters. Ablations are considered essential; omitting them is a common reviewer complaint. Each ablation should isolate a single design choice.
- Analysis: error analysis, qualitative examples, failure cases (especially at CVPR). Show that the method works across different settings and discuss when it fails.

**Conclusion** (0.25--0.5 pages). Brief summary, acknowledged limitations, future work. Do not introduce new claims. Be honest about limitations; reviewers respect this more than sweeping them under the rug.

**Broader Impact / Ethics.** NeurIPS requires a separate ethics statement (typically 1 page, does not count toward the main page limit). ICML and ICLR encourage it. Discuss societal implications, potential misuse, and limitations. Keep it substantive, not boilerplate. Generic statements like "our model could be misused" without specific analysis of how are worse than no statement.

### Checklist items

ML venues increasingly require or strongly encourage the following:
- **Reproducibility checklist**: NeurIPS and ICML require completing a reproducibility checklist (random seeds, hyperparameter tables, compute budget, code release URL). Fill this out honestly and completely.
- **Datasheets for datasets**: If you introduce a dataset, include a datasheet following Gebru et al. (2021). Cover motivation, composition, collection process, preprocessing, uses, distribution, and maintenance.
- **Model cards**: If you release a trained model, include a model card following Mitchell et al. (2019). Cover intended use, out-of-scope use, performance metrics, and ethical considerations.
- **Code release**: Expected. An anonymous code repository linked in the paper is now standard practice. Ensure the code is runnable with a single command and includes a README with dependencies.
- **License**: State the license for any released code or data (e.g., MIT, Apache 2.0, CC-BY).
- **Compute budget**: Report GPU hours, total training time, and estimated cost. This is increasingly required for environmental-impact transparency.

### Common ML reviewer complaints

Understanding what reviewers commonly flag helps you preempt issues:
- Missing ablation studies or ablations that do not isolate individual design choices.
- Unfair baselines (outdated methods, different hyperparameter tuning effort, different compute budgets).
- Insufficient number of random seeds (3 is the minimum; 5 is preferred for variance reporting).
- Claims not supported by the experiments (e.g., claiming generalization when only tested on one dataset).
- Missing error bars or confidence intervals on performance numbers.
- Related work section that is superficial or fails to discuss the closest competing methods in detail.

### Figure conventions

- Figures count toward the page limit. Information density matters. Aim for each figure to communicate one clear message.
- Use vector graphics (PDF) for plots and diagrams. Raster for photographs only.
- Figures must be legible in grayscale (many reviewers print papers). Use hatch patterns or markers in addition to color.
- Ablation tables should be compact: bold the best result, underline the second-best. Include standard deviation across runs.
- Architecture diagrams should be clear and professional. Avoid clip-art quality. Use consistent visual language across all diagrams.
- Qualitative examples (especially at CVPR) should show diverse, representative samples including failure cases.
- Captions should be self-contained: "Architecture of the proposed model. (a) Encoder module with 12 transformer layers. (b) Sparse attention pattern. (c) Performance comparison on ImageNet (error bars: 95% CI over 5 runs)."
- For CVPR / computer-vision papers: side-by-side visual comparisons are standard. Show your method, baselines, and ground truth. Include failure cases as a separate figure or subsection.

### Citation style

Most ML venues use natbib with a numeric bibliography (`plainnat.bst` or `icml.bst`). Some use ACL-style author-year formatting. Check the template. Self-citations in double-blind submissions must be anonymized: cite as "[Author, Year]" without identifying which author is you.

### Section length proportions

Understanding how much space to allocate to each section helps with page-budget planning:

| Section | Approximate pages | Proportion |
|---|---|---|
| Abstract | 0.25 | 3% |
| Introduction | 1.0 | 12--15% |
| Method | 2.0--2.5 | 30--35% |
| Experiments | 2.5--3.0 | 35--40% |
| Conclusion | 0.25--0.5 | 5--8% |
| Broader Impact / Ethics | 0.5 (NeurIPS) | 5% |

The Experiments section typically gets the most space. Within Experiments, allocate roughly equal space to main results and ablation studies. Do not shortchange ablations; they are the most scrutinized subsection.

## Systems Conferences

This section covers SOSP, OSDI, ATC, EuroSys, ASPLOS, ISCA, MICRO, NSDI, and SIGCOMM.

### Page limits and template

- **SOSP / OSDI**: 14 pages (no separate appendix limit for SOSP; OSDI allows unlimited appendix). Use `acmart.cls` with the `sigconf` option, double-column.
- **ASPLOS**: 12 pages main text. `acmart.cls`, double-column.
- **ISCA / MICRO**: 12--14 pages. IEEE conference format, double-column.
- **NSDI / SIGCOMM**: 12--13 pages. `acmart.cls`, double-column.
- **ATC / EuroSys**: 12 pages. `usenix2019_v3.2.tex` (ATC) or `acmart.cls` (EuroSys).

Double-column ACM/IEEE templates are the norm. The format is denser than the single-column ML style. Figures and tables must be designed for the narrow column width (approximately 3.3 inches per column).

### Structure expectations

Systems papers follow a structure closer to traditional IMRAD than ML papers do, but with systems-specific conventions. The structure is typically: Introduction, Background / Motivation, Design, Implementation, Evaluation, Related Work, Conclusion.

**Introduction** (1--1.5 pages). State the problem, motivate with real-world workload or deployment context, state the key idea, and present results at a high level. A figure showing the system architecture is often placed in the introduction to give reviewers an immediate mental model. Contribution lists are used but are less formulaic than in ML papers. Example: "We make three contributions: (i) a new scheduling algorithm, (ii) an implementation in the Linux kernel, and (iii) an evaluation showing 2x throughput improvement."

**Background / Motivation** (0.5--1 page). Explain the context necessary to understand the problem. Include measurements of existing system behavior that motivate the need for a new approach. Quantify the problem: "Current systems waste 40% of GPU memory due to fragmentation" is more convincing than "Current systems are inefficient."

**Design / Architecture** (2--3 pages). Describe the system design, key data structures, algorithms, and protocol. Architecture diagrams are essential. This section often interleaves design rationale with the description. Walk through the key operations step by step. Use numbered or labeled steps in architecture diagrams. Discuss design alternatives you considered and explain why you chose your approach.

**Implementation** (0.5--1 page). Brief summary of the implementation: lines of code, language, key libraries, and any engineering trade-offs. Be specific about what you changed in existing systems (e.g., "We modified 2,300 lines in the Linux kernel's network stack"). This signals engineering depth and helps AE reviewers assess complexity.

**Evaluation** (3--4 pages). The evaluation section is the heart of a systems paper. Typical subsections:
- Experimental setup: hardware specs, software stack, benchmarks, workloads, comparison systems. Be specific about machine configurations (CPU model, RAM, NIC, storage).
- Microbenchmarks: isolated component performance. Shows you understand where time is spent.
- Macrobenchmarks: end-to-end system performance under realistic workloads. Use established benchmarks where available (e.g., YCSB for key-value stores, SPEC for CPUs).
- Scalability: performance as the system scales (nodes, cores, data size). This is essential for distributed systems papers.
- Comparison with prior work: head-to-head with the closest competing system. Use the same workloads and hardware for fair comparison.
- Overhead analysis: resource cost of your approach (CPU overhead, memory overhead, network overhead).

Systems evaluations emphasize statistical rigor less than ML papers but expect thoroughness: multiple workloads, breakdowns, and headroom analysis. Report throughput, latency (mean, median, P99 tail), and resource utilization. Present latency as a distribution (CDF plots are standard), not just point estimates.

### Artifact evaluation (AE)

Many systems venues (SOSP, OSDI, ASPLOS, EuroSys, ATC, NSDI, SIGCOMM) run an Artifact Evaluation process. After the paper is accepted, a separate committee evaluates whether the artifacts (code, data, scripts) can reproduce the paper's claims. This is optional at some venues and mandatory at others. The AE process is increasingly seen as a mark of quality: papers with AE badges are cited more often.

**AE badges:**
- **Artifacts Available**: Artifacts are publicly accessible (e.g., on GitHub, Zenodo). Use a permanent archive (Zenodo with a DOI) rather than just a GitHub link.
- **Artifacts Evaluated -- Functional**: Reviewers can build and run the artifacts. The artifact works as described.
- **Artifacts Evaluated -- Reproduced**: Reviewers can reproduce the paper's main results using the artifacts.
- **Results Reproduced**: Independent team replicates results using a different setup or implementation.

**AE preparation best practices:**
- Provide a self-contained artifact with a clear README, minimal dependency requirements (preferably a Docker container or VM image), and a script that runs the key experiments end-to-end.
- Include a step-by-step guide that an AE reviewer can follow in under 2 hours.
- Provide a "quick demo" script that produces a small-scale result in minutes, and a separate script for the full experiments.
- Pre-build binaries for common platforms. AE reviewers may not have the exact same compiler or library versions.
- Document expected resource requirements (minimum RAM, disk space, number of machines).
- If your system requires specific hardware (e.g., particular NICs, FPGAs), clearly state this and offer remote access if possible.

### Double-blind anonymization

Most systems venues now use double-blind review (SOSP, OSDI, EuroSys, NSDI, SIGCOMM). ATC and some ISCA/MICRO submissions use single-blind. When double-blind:
- Anonymize code repositories using a throwaway account.
- Redact institution-identifying details in the paper (e.g., "a large cloud provider" instead of the company name).
- Cite your own prior work in the third person: "Smith et al. [1] proposed..." not "In our previous work [1]..."
- Avoid disclosing the scale of your deployment if it identifies the institution (e.g., "a cluster with 10,000 GPUs" may narrow the field).

### Common systems reviewer complaints

- Missing comparison with the most recent or most relevant prior system.
- Evaluation on only synthetic or toy workloads; lack of real-world workload validation.
- Insufficient explanation of why the system works: reviewers want mechanistic understanding, not just "it is faster."
- Claims of generality tested on only one workload class or one hardware configuration.
- Missing overhead analysis: every optimization has a cost, and reviewers expect you to report it.
- Vague scalability claims without data: "scales linearly" should be backed by a scalability plot.

### Writing style

Systems papers use a direct, engineering-oriented voice. Sentences tend to be shorter and more active than in journal papers. First-person plural ("we") is standard. Claims about performance gains should be specific and backed by numbers: "reduces median tail latency by 2.3x" rather than "significantly improves performance." Avoid vague superlatives.

### Section length proportions

| Section | Approximate pages | Proportion |
|---|---|---|
| Introduction | 1.0--1.5 | 10% |
| Background / Motivation | 0.5--1.0 | 5--7% |
| Design / Architecture | 2.5--3.0 | 20--25% |
| Implementation | 0.5--1.0 | 5--7% |
| Evaluation | 3.0--4.0 | 25--30% |
| Related Work | 1.0--1.5 | 10% |
| Conclusion | 0.5 | 5% |

The Evaluation section is typically the largest. Within Evaluation, macrobenchmarks and scalability analysis deserve the most space. Do not skimp on the scalability subsection; it is often what distinguishes a strong systems paper from a weak one.

## HCI / Software-Engineering Conferences

This section covers CHI, UIST, ICSE, FSE, and related venues.

### Page limits and template

- **CHI**: 10-page main text (references do not count) + 2-page appendix. `acmart.cls` with `sigchi` option. Single-column.
- **UIST**: 10 pages. `acmart.cls` with `sigchi` option.
- **ICSE**: 10 pages. IEEE conference format, double-column.
- **FSE**: 12 pages. `acmart.cls` with `sigsoft` option, double-column.

### Structure expectations

HCI and SE papers use varied structures depending on the paper type (empirical study, tool paper, theory paper, mixed-methods). Empirical papers follow an IMRAD-like structure but with discipline-specific additions. Tool papers have a different structure centered on the tool's design and validation.

**Empirical study structure.** Follow IMRAD with these additions:
- Participants / Subjects section in Methods: recruitment method, sample size with justification (power analysis for quantitative, saturation for qualitative), demographics, compensation, IRB approval number.
- Data Collection: instruments, interview protocols, survey instruments. Include the actual instrument in an appendix if space allows.
- Data Analysis: analysis method (thematic analysis, grounded theory, affinity diagramming), coding process, inter-rater reliability.
- Results: present findings organized by research questions. Include both quantitative measures and qualitative themes.

**Tool paper structure.** Common at ICSE and FSE:
- Introduction: problem the tool addresses and why existing tools are insufficient.
- Tool Design: architecture, key features, how it differs from prior tools.
- Implementation: technologies used, availability, license.
- Evaluation: user study or case study demonstrating the tool's effectiveness.
- Discussion: limitations, future development plan.

**Qualitative reporting (SRQR / COREQ).** When reporting qualitative findings (interviews, think-aloud studies, open-ended survey responses), follow the Standards for Reporting Qualitative Research (SRQR) or COREQ guidelines. Key elements:
- Describe the analysis method (thematic analysis, grounded theory, affinity diagramming) with enough detail for replication.
- Report inter-rater reliability if coding (Cohen's kappa, Krippendorff's alpha). A threshold of kappa >= 0.7 is typically expected.
- Include representative quotes with participant identifiers (e.g., "P5, senior developer, 10 years experience").
- Discuss reflexivity: the researchers' positionality and how it may influence interpretation. This is increasingly expected at CHI and not optional.
- Describe how you handled negative or disconfirming cases.

**Mixed methods.** Many HCI and SE papers combine quantitative and qualitative methods. The structure should make the methodological triangulation explicit: state what each method contributes and how findings converge or diverge. Use a convergent design (both methods in parallel), explanatory design (quantitative first, qualitative explains), or exploratory design (qualitative first, quantitative tests) and state which you chose.

### Threats to validity

Both CHI and ICSE/FSE papers are expected to include an explicit Threats to Validity section. Organize by type:
- **Internal validity**: confounding variables, maturation effects, selection bias.
- **External validity**: generalizability of participants, tasks, and settings.
- **Construct validity**: whether measures accurately capture the constructs of interest.
- **Reliability**: consistency of measurements and analysis procedures.

### Writing style

HCI papers allow a slightly more engaging voice than systems papers. Motivation through concrete scenarios or user stories is common in the introduction. CHI papers often begin with a vignette: "Imagine a user who..." SE papers tend toward more formal, structured prose. Both value clear threats-to-validity discussions, typically organized as internal validity, external validity, construct validity, and reliability.

**Participant description.** CHI papers should include a participant table with demographics (age, gender, occupation, relevant experience). ICSE papers should describe developer participants by experience level, programming languages, and professional context.

**Figures and tables.** CHI papers often include interface screenshots, study setup photos, and interaction flow diagrams. SE papers commonly include system architecture diagrams, code snippet examples, and process flow diagrams. Both use more figures than typical systems papers.

## Journals

This section covers broad-audience journals (Science, Nature, PNAS) and ACM/IEEE Transactions.

### Broad-audience journals (Science, Nature, PNAS)

These journals target readers across disciplines. The writing must be accessible to a non-specialist.

**Length.** Typically 2,000--4,500 words for the main text, with detailed Methods in supplementary material. Nature allows approximately 3,000 words; Science is similar. PNAS allows up to 6,000 words for Direct Submission. The word count is strict; exceeding it is a desk-reject trigger.

**Structure.** A modified IMRAD: the main text tells a story, and the detailed methods are relegated to a supplementary section or appendix. Nature and Science use a "strand" format where the narrative flows continuously without rigid section headings, though subheadings are used for long papers. The key difference from specialty journals is that the main text reads as a narrative, with the first paragraph establishing broad significance and the last paragraph stating implications.

**Voice.** Active voice, first-person plural ("we"). Engaging, story-driven. The opening paragraph must convey broad significance to a general scientist audience. Technical terms should be defined on first use. Equations are minimized in the main text. Nature and Science favor sentences in the 15--20 word range. Avoid jargon even when writing about a technical topic; replace "stochastic gradient descent" with "an optimization algorithm" in the main text if the audience is not ML researchers.

**Figures.** Strictly limited (4--6 main figures). Each figure should be information-rich and self-contained. Multi-panel figures are standard. Extended Data figures go in the supplement. Figures are often the first thing editors and reviewers look at, so invest heavily in figure quality. Use large labels, clear legends, and consistent color schemes.

**Submission requirements.** These journals require specific formatting: Nature asks for a one-paragraph abstract (approximately 150 words) without citations, a separate "First paragraph" that serves as the introductory summary, and an "Author contributions" statement. PNAS requires a 250-word abstract and a significance statement. Science requires a structured abstract and a separate "Summary" paragraph for the table of contents. Check the specific journal's guidelines carefully; requirements differ substantially.

**Editorial screening.** Unlike most CS venues, Nature and Science pre-screen papers before sending them to reviewers. An editor decides whether the paper is of sufficient general interest. This means the abstract and first paragraph carry enormous weight; they must convince a non-specialist editor that the work matters.

### ACM / IEEE Transactions

Transactions journals (e.g., ACM TOCS, IEEE TPAMI, ACM Computing Surveys, IEEE TSE, IEEE TC, ACM TECS) are the archival backbone of CS.

**Length.** No strict page limit, but papers typically run 20--35 pages (double-column). Survey papers can be longer (40--60 pages). Check the specific journal; some impose soft limits or charge overpage fees.

**Structure.** Full IMRAD or a close variant. Separate Results and Discussion sections. A thorough Related Work section is expected, typically spanning 2--4 pages. Methods should be detailed enough for replication in the main text (not just supplementary material). Many Transactions papers include a formal Problem Statement or Preliminaries section that defines notation and the problem formulation.

**Voice.** Formal, third-person or first-person plural. Technical depth is valued over accessibility. Equations, proofs, and formal analysis are welcome in the main text. Sentences tend to be longer (18--25 words) than in conference papers. Passive voice is more acceptable than in conference papers, particularly in Methods.

**Formatting.** Use `acmart.cls` with the `acmtocs` (or appropriate journal) option for ACM journals. Use `IEEEtran.cls` for IEEE journals. Both are double-column. ACM journals use their own citation format via `ACM-Reference-Format.bst`. IEEE journals use IEEEtran.bst.

**Review process.** Journal reviews are typically not double-blind (though some ACM journals offer it as an option). Reviewers expect thoroughness over novelty. A journal paper that merely reproduces a conference paper without significant additional content will be rejected; the expectation is 30--50% new material. Journal review cycles are long (6--18 months for a first decision), so plan accordingly.

**Journal extension of conference papers.** When extending a conference paper to a journal version, you must: (a) clearly state in the introduction that this extends the conference version, (b) cite the conference paper, (c) describe the significant new contributions, and (d) ensure the new content is at least 30--50% of the journal paper. Some journals (e.g., IEEE TPAMI) have explicit requirements for journal extensions.

## Voice and Length per Venue

| Venue class | Voice | Hedge level | "Novel" / "first" claims | Typical length |
|---|---|---|---|---|
| ML conferences | "We propose...", numbered contributions | Low: claim gains directly | Expected; quantify ("15% faster") | 8--9 pages |
| Systems conferences | "We design / build / implement..." | Moderate: back claims with numbers | Acceptable with strong evaluation | 12--14 pages |
| HCI / SE conferences | "We conducted a study..." | Moderate to high | Use sparingly; prefer evidence | 10--12 pages |
| Broad journals (Nature, Science) | "Here we show..." | Moderate | Use judiciously; overstatement triggers reviewer resistance | 2,000--4,500 words |
| ACM / IEEE Transactions | "We present / investigate..." | Moderate to high | Acceptable if well-supported | 20--35 pages |

**Hedging guidance.** ML venues tolerate the most direct claims ("our method outperforms all baselines") because the experiments section is expected to substantiate them. Journal papers require more hedging ("our results suggest that...") because claims must be defensible beyond the specific experimental setup. Systems papers sit in the middle: direct claims about performance are fine if backed by measurement, but causal claims about why the system works should be hedged. HCI and SE papers require the most hedging when making generalization claims, because study samples are often small and context-dependent.

**"Novel" and "first" claims.** ML reviewers expect you to state novelty explicitly in the contribution list. Systems reviewers are more skeptical and prefer the evaluation to speak for itself. Journal reviewers are the most skeptical; "to the best of our knowledge, this is the first..." is the standard hedge. At HCI and SE venues, novelty claims are less important than rigor and validity of the study design.

**Sentence length norms.** Nature and Science target 15--20 words per sentence. ML conference papers are similar. Systems papers average 18--25 words. Journal papers allow the longest sentences (20--25 words). HCI and SE papers vary: empirical sections tend toward shorter sentences, theoretical sections toward longer ones. Across all venues, vary sentence length for readability; a monotonous rhythm hurts clarity regardless of venue.

**Active vs. passive voice.** ML and systems conferences strongly prefer active voice ("we propose", "we implement"). Nature and Science also prefer active voice. IEEE Transactions are more tolerant of passive voice in Methods sections. Use passive voice when the action matters more than the actor: "The system was deployed on a 16-node cluster" is fine. Avoid passive voice that obscures agency: "It was decided that..." should become "We decided to..."

## Quick-Adaptation Checklist

Use this checklist when converting a draft from one venue class to another.

**Journal to conference:**
- [ ] Condense introduction to fit page limit; add numbered contribution list (ML) or architecture figure early (systems).
- [ ] Combine Results and Discussion into a single Experiments section.
- [ ] Move detailed methods, proofs, and extended tables to supplementary material.
- [ ] Anonymize self-references and remove author-identifying details.
- [ ] Compress figures for information density; ensure grayscale readability.
- [ ] Add reproducibility details (seeds, hyperparameters, code URL).
- [ ] Check that all essential claims are in the main text, not buried in supplementary material.

**Conference to journal:**
- [ ] Expand introduction with more background and motivation.
- [ ] Separate Experiments into distinct Results and Discussion sections.
- [ ] Move supplementary material (proofs, extended tables) into the main text.
- [ ] Remove contribution numbering; weave contributions into narrative prose.
- [ ] Expand the related work section with comprehensive coverage.
- [ ] Strengthen the limitations discussion beyond the brief conference version.
- [ ] Add author names, affiliations, and funding acknowledgments.
- [ ] Verify 30--50% new content beyond the conference version.

**ML conference to systems conference:**
- [ ] Replace emphasis on ablation studies with end-to-end system evaluation.
- [ ] Add implementation details section (LOC, language, engineering trade-offs).
- [ ] Include scalability and headroom analysis under realistic workloads.
- [ ] Prepare artifacts for Artifact Evaluation (Docker, README, run script).
- [ ] Switch template from single-column ML style to double-column ACM/IEEE.

**Systems conference to ML conference:**
- [ ] Add numbered contribution list in introduction.
- [ ] Add ablation studies if not already present.
- [ ] Report computational requirements (GPU hours, training time, parameter count).
- [ ] Compress evaluation to fit 8--9 pages; move detailed breakdowns to appendix.
- [ ] Add broader impact or ethics statement if required by the venue.
- [ ] Switch template from double-column ACM/IEEE to single-column ML style.

**Conference to HCI / SE conference:**
- [ ] Add participant demographics table if the paper includes a user study.
- [ ] Add Threats to Validity section covering internal, external, construct, and reliability.
- [ ] Ensure qualitative analysis section describes method, inter-rater reliability, and reflexivity.
- [ ] Replace system benchmark evaluation with user study or controlled experiment where appropriate.
- [ ] Include representative quotes with participant identifiers.

**HCI / SE conference to journal:**
- [ ] Expand the Related Work section to be comprehensive (2--4 pages).
- [ ] Separate Results and Discussion into distinct sections.
- [ ] Expand the Methods section with full protocol detail.
- [ ] Add a Discussion section that relates findings to theory and prior work.
- [ ] Include 30--50% new content beyond the conference version.
- [ ] Extend the study (additional participants, new analysis) to strengthen validity claims.
