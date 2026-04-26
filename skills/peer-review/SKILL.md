---
name: peer-review
description: Structured manuscript/grant review with checklist-based evaluation for systems, ML, and HCI venues. Use when writing formal peer reviews covering methodology, statistical validity, reproducibility, and constructive feedback. Clinical reporting standards (CONSORT, STROBE, etc.) are optional and only invoked for clinical/medical venues. For evaluating claims/evidence quality use scientific-critical-thinking; for quantitative scoring frameworks use scholar-evaluation.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Scientific Critical Evaluation and Peer Review

## Overview

Peer review is a systematic process for evaluating scientific manuscripts. This skill defaults to **systems, ML, and HCI venue** review: assessing methodology, experimental design, reproducibility, statistical rigor, and constructive feedback for computational and engineering-oriented research.

Clinical reporting standards (CONSORT, STROBE, PRISMA, ARRIVE, MIAME) are listed as **optional domain-specific checklists**. They are only invoked when `.writing/metadata.yaml` declares the target venue as clinical or medical. For all other venues, no clinical reporting standard is applied.

## When to Use This Skill

This skill should be used when:
- Conducting peer review of manuscripts targeting systems, ML, or HCI venues
- Evaluating grant proposals and research applications in computing disciplines
- Assessing methodology, experimental design, and benchmarking rigor
- Reviewing statistical analyses, ablation studies, and significance tests
- Evaluating reproducibility: code availability, dataset provenance, hyperparameter reporting
- Checking compliance with ML reproducibility checklists (NeurIPS/ICML/ICLR style)
- Reviewing manuscripts for clinical/medical venues (optional clinical checklists apply)
- Providing constructive feedback on scientific writing

## Peer Review Workflow

Conduct peer review systematically through the following stages, adapting depth and focus based on the manuscript type and discipline.

### Stage 1: Initial Assessment

Begin with a high-level evaluation to determine the manuscript's scope, novelty, and overall quality.

**Key Questions:**
- What is the central research question or hypothesis?
- What are the main findings and conclusions?
- Is the work scientifically sound and significant?
- Is the work appropriate for the intended venue?
- Are there any immediate major flaws that would preclude publication?

**Output:** Brief summary (2-3 sentences) capturing the manuscript's essence and initial impression.

### Stage 2: Detailed Section-by-Section Review

Conduct a thorough evaluation of each manuscript section, documenting specific concerns and strengths.

#### Abstract and Title
- **Accuracy:** Does the abstract accurately reflect the study's content and conclusions?
- **Clarity:** Is the title specific, accurate, and informative?
- **Completeness:** Are key findings and methods summarized appropriately?
- **Accessibility:** Is the abstract comprehensible to a broad scientific audience?

#### Introduction
- **Context:** Is the background information adequate and current?
- **Rationale:** Is the research question clearly motivated and justified?
- **Novelty:** Is the work's originality and significance clearly articulated?
- **Literature:** Are relevant prior studies appropriately cited?
- **Objectives:** Are research aims/hypotheses clearly stated?

#### Methods
- **Reproducibility:** Can another researcher replicate the study from the description provided?
- **Rigor:** Are the methods appropriate for addressing the research questions?
- **Detail:** Are protocols, reagents, equipment, and parameters sufficiently described?
- **Ethics:** Are ethical approvals, consent, and data handling properly documented?
- **Statistics:** Are statistical methods appropriate, clearly described, and justified?
- **Validation:** Are controls, replicates, and validation approaches adequate?

**Critical elements to verify:**
- Sample sizes and power calculations
- Randomization and blinding procedures
- Inclusion/exclusion criteria
- Data collection protocols
- Computational methods and software versions
- Statistical tests and correction for multiple comparisons

#### Results
- **Presentation:** Are results presented logically and clearly?
- **Figures/Tables:** Are visualizations appropriate, clear, and properly labeled?
- **Statistics:** Are statistical results properly reported (effect sizes, confidence intervals, p-values)?
- **Objectivity:** Are results presented without over-interpretation?
- **Completeness:** Are all relevant results included, including negative results?
- **Reproducibility:** Are raw data or summary statistics provided?

**Common issues to identify:**
- Selective reporting of results
- Inappropriate statistical tests
- Missing error bars or measures of variability
- Over-fitting or circular analysis
- Batch effects or confounding variables
- Missing controls or validation experiments

#### Discussion
- **Interpretation:** Are conclusions supported by the data?
- **Limitations:** Are study limitations acknowledged and discussed?
- **Context:** Are findings placed appropriately within existing literature?
- **Speculation:** Is speculation clearly distinguished from data-supported conclusions?
- **Significance:** Are implications and importance clearly articulated?
- **Future directions:** Are next steps or unanswered questions discussed?

**Red flags:**
- Overstated conclusions
- Ignoring contradictory evidence
- Causal claims from correlational data
- Inadequate discussion of limitations
- Mechanistic claims without mechanistic evidence

#### References
- **Completeness:** Are key relevant papers cited?
- **Currency:** Are recent important studies included?
- **Balance:** Are contrary viewpoints appropriately cited?
- **Accuracy:** Are citations accurate and appropriate?
- **Self-citation:** Is there excessive or inappropriate self-citation?

### Stage 3: Methodological and Statistical Rigor

Evaluate the technical quality and rigor of the research with particular attention to common pitfalls.

**Statistical Assessment:**
- Are statistical assumptions met (normality, independence, homoscedasticity)?
- Are effect sizes reported alongside p-values?
- Is multiple testing correction applied appropriately?
- Are confidence intervals provided?
- Is sample size justified with power analysis?
- Are parametric vs. non-parametric tests chosen appropriately?
- Are missing data handled properly?
- Are exploratory vs. confirmatory analyses distinguished?

**Experimental Design:**
- Are controls appropriate and adequate?
- Is replication sufficient (biological and technical)?
- Are potential confounders identified and controlled?
- Is randomization properly implemented?
- Are blinding procedures adequate?
- Is the experimental design optimal for the research question?

**Computational/Bioinformatics:**
- Are computational methods clearly described and justified?
- Are software versions and parameters documented?
- Is code made available for reproducibility?
- Are algorithms and models validated appropriately?
- Are assumptions of computational methods met?
- Is batch correction applied appropriately?

### Stage 4: Reproducibility and Transparency

Assess whether the research meets modern standards for reproducibility and open science.

**Data Availability:**
- Are raw data deposited in appropriate repositories?
- Are accession numbers provided for public databases?
- Are data sharing restrictions justified (e.g., patient privacy)?
- Are data formats standard and accessible?

**Code and Materials:**
- Is analysis code made available (GitHub, Zenodo, etc.)?
- Are unique materials available or described sufficiently for recreation?
- Are protocols detailed in sufficient depth?

**Reporting Standards (optional, clinical venues only):**
- Clinical reporting guidelines (CONSORT, PRISMA, ARRIVE, MIAME, MINSEQE, etc.) apply only when the manuscript targets a clinical or medical venue. See `references/reporting_standards.md` for the full list.
- For systems/ML/HCI papers, no clinical reporting standard is required; use the ML reproducibility checklist in Stage 3 instead.
- **TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis):** Applies when the paper presents a predictive model as a primary product. Covers participant selection, predictor definitions, missing-data handling, model specification, and performance evaluation. Optional for ML papers that include a deployed model; otherwise not applicable.
- **SRQR (Standards for Reporting Qualitative Research):** A 21-item checklist for studies with qualitative components. Useful for HCI and systems papers that include user studies, think-aloud protocols, or interview-based evaluations. Covers research question framing, data collection methodology, analyst roles, and trustworthiness criteria. Optional; apply when the manuscript includes qualitative methods.

### Stage 5: Figure and Data Presentation

Evaluate the quality, clarity, and integrity of data visualization.

**Quality Checks:**
- Are figures high resolution and clearly labeled?
- Are axes properly labeled with units?
- Are error bars defined (SD, SEM, CI)?
- Are statistical significance indicators explained?
- Are color schemes appropriate and accessible (colorblind-friendly)?
- Are scale bars included for images?
- Is data visualization appropriate for the data type?

**Integrity Checks:**
- Are there signs of image manipulation (duplications, splicing)?
- (Clinical/medical venues only) Are Western blots, gels, and microscopy images appropriately presented?
- Are representative images truly representative?
- Are all conditions shown (no selective presentation)?

**Clarity:**
- Can figures stand alone with their legends?
- Is the message of each figure immediately clear?
- Are there redundant figures or panels?
- Would data be better presented as tables or figures?

### Stage 6: Ethical Considerations

Verify that the research meets ethical standards relevant to systems, ML, and HCI work.

**Dual-Use and Security:**
- Does the system have potential for misuse (e.g., surveillance, automated weaponization, scalable social engineering)?
- Are dual-use risks acknowledged and mitigations discussed?
- Is responsible disclosure practiced for discovered vulnerabilities?

**Environmental Impact and Energy Reporting:**
- Is training or inference compute cost reported (GPU-hours, energy consumption, carbon estimate)?
- For large-scale systems, is there a discussion of resource efficiency vs. performance trade-offs?
- Are comparisons to baselines fair in terms of compute budget?

**Data Ethics:**
- When user data is involved, is it properly de-identified or anonymized?
- Are dataset licenses and provenance documented?
- Is there a discussion of dataset biases and their potential impact on results?
- For scraped or crowd-sourced data, are consent and terms-of-service compliance addressed?

**Broader-Impact Statement (NeurIPS-style):**
- Does the paper discuss potential societal consequences of the work?
- Are both positive applications and foreseeable misuse scenarios addressed?
- Is the statement substantive rather than boilerplate?

**Research Integrity:**
- Is authorship appropriate and justified?
- Are competing interests disclosed?
- Is funding source disclosed?
- Are there concerns about plagiarism, duplicate publication, or data fabrication?
- For benchmark results, is selective reporting of favorable metrics avoided?

### Stage 7: Writing Quality and Clarity

Assess the manuscript's clarity, organization, and accessibility.

**Structure and Organization:**
- Is the manuscript logically organized?
- Do sections flow coherently?
- Are transitions between ideas clear?
- Is the narrative compelling and clear?

**Writing Quality:**
- Is the language clear, precise, and concise?
- Are jargon and acronyms minimized and defined?
- Is grammar and spelling correct?
- Are sentences unnecessarily complex?
- Is the passive voice overused?

**Accessibility:**
- Can a non-specialist understand the main findings?
- Are technical terms explained?
- Is the significance clear to a broad audience?

## ML / Systems Reproducibility Checklist

Use this checklist when reviewing manuscripts at systems, ML, or HCI venues. It adapts the NeurIPS/ICML/ICLR reproducibility requirements for a broader computational-research audience.

### Datasets

- [ ] **Source and version:** Dataset name, version number or commit hash, and download URL or access mechanism are stated.
- [ ] **License:** Dataset license is specified (e.g., CC-BY-4.0, Apache-2.0, custom research-only).
- [ ] **Splits:** Train/validation/test split strategy is documented. If standard benchmarks are used, the split convention is named (e.g., "ImageNet ILSVRC2012 train/val split").
- [ ] **Collection methodology:** For new datasets, the collection process, inclusion/exclusion criteria, and annotator instructions are described or referenced.
- [ ] **Preprocessing:** Any normalization, tokenization, filtering, or augmentation steps are listed with parameter values.

### Code and Artifacts

- [ ] **Code availability:** A public repository URL or a statement explaining why code cannot be released.
- [ ] **Version pinning:** Commit hash, tag, or release version that reproduces the reported results.
- [ ] **Dependencies:** Full dependency list with versions (e.g., `requirements.txt`, `Cargo.lock`, Dockerfile). Framework versions (PyTorch, TensorFlow, CUDA) are explicit.
- [ ] **Build and run instructions:** Step-by-step commands to train and evaluate, including expected wall-clock time and disk usage.
- [ ] **Trained model checkpoints:** If applicable, downloadable checkpoint URLs or a statement that they are not released (with reason).

### Hyperparameters

- [ ] **Full hyperparameter table:** Every tunable parameter with its search space (or final value) is listed in the paper or appendix. Includes learning rate, batch size, optimizer, weight decay, dropout, number of layers/units, etc.
- [ ] **Selection method:** How hyperparameters were chosen (grid search, random search, Bayesian optimization, defaults) is stated.

### Random Seeds and Determinism

- [ ] **Seed declaration:** All random seeds used for the reported results are listed (e.g., seeds = {42, 123, 456}).
- [ ] **Per-result mapping:** It is clear which seed corresponds to which table entry or figure panel.
- [ ] **Determinism caveats:** Known sources of non-determinism (GPU nondeterminism, data-ordering effects) are acknowledged.

### Computational Resources

- [ ] **Hardware:** GPU/CPU model and count (e.g., "4 x NVIDIA A100 80 GB"), RAM, and interconnect if relevant.
- [ ] **Runtime:** Training and inference wall-clock time for each experiment.
- [ ] **Energy estimate:** If available, an energy or carbon estimate (e.g., kWh consumed, or tons CO2 using a regional grid-emission factor).

### Statistical-Significance Reporting

- [ ] **Multiple runs:** Results are averaged over at least 3 independent runs with different seeds; individual-run values or standard deviations are reported.
- [ ] **Error bars:** Figures include error bars (SD, SEM, or 95% CI) and the measure is defined.
- [ ] **Confidence intervals:** Key claims are supported by CIs or bootstrap intervals where appropriate.
- [ ] **Significance tests:** When statistical tests are used (t-test, Wilcoxon, bootstrap), the test name, p-value, and correction for multiple comparisons are stated.
- [ ] **Effect sizes:** Beyond p-values, effect sizes or practical significance are discussed.

### Broader-Impact Statement

- [ ] If the venue requires a broader-impact or societal-impact statement, verify that it is present and substantive (not boilerplate).
- [ ] Positive applications and foreseeable misuse scenarios are both addressed.

## Structuring Peer Review Reports

Organize feedback in a hierarchical structure that prioritizes issues and provides actionable guidance.

### Summary Statement

Provide a concise overall assessment (1-2 paragraphs):
- Brief synopsis of the research
- Overall recommendation (accept, minor revisions, major revisions, reject)
- Key strengths (2-3 bullet points)
- Key weaknesses (2-3 bullet points)
- Bottom-line assessment of significance and soundness

### Major Comments

List critical issues that significantly impact the manuscript's validity, interpretability, or significance. Number these sequentially for easy reference.

**Major comments typically include:**
- Fundamental methodological flaws
- Inappropriate statistical analyses
- Unsupported or overstated conclusions
- Missing critical controls or experiments
- Serious reproducibility concerns
- Major gaps in literature coverage
- Ethical concerns

**For each major comment:**
1. Clearly state the issue
2. Explain why it's problematic
3. Suggest specific solutions or additional experiments
4. Indicate if addressing it is essential for publication

### Minor Comments

List less critical issues that would improve clarity, completeness, or presentation. Number these sequentially.

**Minor comments typically include:**
- Unclear figure labels or legends
- Missing methodological details
- Typographical or grammatical errors
- Suggestions for improved data presentation
- Minor statistical reporting issues
- Supplementary analyses that would strengthen conclusions
- Requests for clarification

**For each minor comment:**
1. Identify the specific location (section, paragraph, figure)
2. State the issue clearly
3. Suggest how to address it

### Specific Line-by-Line Comments (Optional)

For manuscripts requiring detailed feedback, provide section-specific or line-by-line comments:
- Reference specific page/line numbers or sections
- Note factual errors, unclear statements, or missing citations
- Suggest specific edits for clarity

### Questions for Authors

List specific questions that need clarification:
- Methodological details that are unclear
- Seemingly contradictory results
- Missing information needed to evaluate the work
- Requests for additional data or analyses

## Tone and Approach

Maintain a constructive, professional, and collegial tone throughout the review.

**Best Practices:**
- **Be constructive:** Frame criticism as opportunities for improvement
- **Be specific:** Provide concrete examples and actionable suggestions
- **Be balanced:** Acknowledge strengths as well as weaknesses
- **Be respectful:** Remember that authors have invested significant effort
- **Be objective:** Focus on the science, not the scientists
- **Be thorough:** Don't overlook issues, but prioritize appropriately
- **Be clear:** Avoid ambiguous or vague criticism

**Avoid:**
- Personal attacks or dismissive language
- Sarcasm or condescension
- Vague criticism without specific examples
- Requesting unnecessary experiments beyond the scope
- Demanding adherence to personal preferences vs. best practices
- Revealing your identity if reviewing is double-blind

## Special Considerations by Manuscript Type

### Original Research Articles
- Emphasize rigor, reproducibility, and novelty
- Assess significance and impact
- Verify that conclusions are data-driven
- Check for complete methods and appropriate controls

### Reviews and Meta-Analyses
- Evaluate comprehensiveness of literature coverage
- Assess search strategy and inclusion/exclusion criteria
- Verify systematic approach and lack of bias
- Check for critical analysis vs. mere summarization
- For meta-analyses, evaluate statistical approach and heterogeneity

### Methods Papers
- Emphasize validation and comparison to existing methods
- Assess reproducibility and availability of protocols/code
- Evaluate improvements over existing approaches
- Check for sufficient detail for implementation

### Short Reports/Letters
- Adapt expectations for brevity
- Ensure core findings are still rigorous and significant
- Verify that format is appropriate for findings

### Preprints
- Recognize that these have not undergone formal peer review
- May be less polished than journal submissions
- Still apply rigorous standards for scientific validity
- Consider providing constructive feedback to help authors improve before journal submission

### Presentations and Slide Decks

**⚠️ CRITICAL: For presentations, NEVER read the PDF directly. ALWAYS convert to images first.**

When reviewing scientific presentations (PowerPoint, Beamer, slide decks):

#### Mandatory Image-Based Review Workflow

**NEVER attempt to read presentation PDFs directly** - this causes buffer overflow errors and doesn't show visual formatting issues.

**Required Process:**
1. Convert PDF to images using Python:
   ```bash
   python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150
   # Creates: review/slide-001.jpg, review/slide-002.jpg, etc.
   ```
2. Read and inspect EACH slide image file sequentially
3. Document issues with specific slide numbers
4. Provide feedback on visual formatting and content

**Print when starting review:**
```
[HH:MM:SS] PEER REVIEW: Presentation detected - converting to images for review
[HH:MM:SS] PDF REVIEW: NEVER reading PDF directly - using image-based inspection
```

#### Presentation-Specific Evaluation Criteria

**Visual Design and Readability:**
- [ ] Text is large enough (minimum 18pt, ideally 24pt+ for body text)
- [ ] High contrast between text and background (4.5:1 minimum, 7:1 preferred)
- [ ] Color scheme is professional and colorblind-accessible
- [ ] Consistent visual design across all slides
- [ ] White space is adequate (not cramped)
- [ ] Fonts are clear and professional

**Layout and Formatting (Check EVERY Slide Image):**
- [ ] No text overflow or truncation at slide edges
- [ ] No element overlaps (text over images, overlapping shapes)
- [ ] Titles are consistently positioned
- [ ] Content is properly aligned
- [ ] Bullets and text are not cut off
- [ ] Figures fit within slide boundaries
- [ ] Captions and labels are visible and readable

**Content Quality:**
- [ ] One main idea per slide (not overloaded)
- [ ] Minimal text (3-6 bullets per slide maximum)
- [ ] Bullet points are concise (5-7 words each)
- [ ] Figures are simplified and clear (not copy-pasted from papers)
- [ ] Data visualizations have large, readable labels
- [ ] Citations are present and properly formatted
- [ ] Results/data slides dominate the presentation (40-50% of content)

**Structure and Flow:**
- [ ] Clear narrative arc (introduction → methods → results → discussion)
- [ ] Logical progression between slides
- [ ] Slide count appropriate for talk duration (~1 slide per minute)
- [ ] Title slide includes authors, affiliation, date
- [ ] Introduction cites relevant background literature (3-5 papers)
- [ ] Discussion cites comparison papers (3-5 papers)
- [ ] Conclusions slide summarizes key findings
- [ ] Acknowledgments/funding slide at end

**Scientific Content:**
- [ ] Research question clearly stated
- [ ] Methods adequately summarized (not excessive detail)
- [ ] Results presented logically with clear visualizations
- [ ] Statistical significance indicated appropriately
- [ ] Conclusions supported by data shown
- [ ] Limitations acknowledged where appropriate
- [ ] Future directions or broader impact discussed

**Common Presentation Issues to Flag:**

**Critical Issues (Must Fix):**
- Text overflow making content unreadable
- Font sizes too small (<18pt)
- Element overlaps obscuring data
- Insufficient contrast (text hard to read)
- Figures too complex or illegible
- No citations (completely unsupported claims)
- Slide count drastically mismatched to duration

**Major Issues (Should Fix):**
- Inconsistent design across slides
- Too much text (walls of text, not bullets)
- Poorly simplified figures (axis labels too small)
- Cramped layout with insufficient white space
- Missing key structural elements (no conclusion slide)
- Poor color choices (not colorblind-safe)
- Minimal results content (<30% of slides)

**Minor Issues (Suggestions for Improvement):**
- Could use more visuals/diagrams
- Some slides slightly text-heavy
- Minor alignment inconsistencies
- Could benefit from more white space
- Additional citations would strengthen claims
- Color scheme could be more modern

#### Review Report Format for Presentations

**Summary Statement:**
- Overall impression of presentation quality
- Appropriateness for target audience and duration
- Key strengths (visual design, content, clarity)
- Key weaknesses (formatting issues, content gaps)
- Recommendation (ready to present, minor revisions, major revisions)

**Layout and Formatting Issues (By Slide Number):**
```
Slide 3: Text overflow - bullet point 4 extends beyond right margin
Slide 7: Element overlap - figure overlaps with caption text
Slide 12: Font size - axis labels too small to read from distance
Slide 18: Alignment - title not centered
```

**Content and Structure Feedback:**
- Adequacy of background context and citations
- Clarity of research question and objectives
- Quality of methods summary
- Effectiveness of results presentation
- Strength of conclusions and implications

**Design and Accessibility:**
- Overall visual appeal and professionalism
- Color contrast and readability
- Colorblind accessibility
- Consistency across slides

**Timing and Scope:**
- Whether slide count matches intended duration
- Appropriate level of detail for talk type
- Balance between sections

#### Example Image-Based Review Process

```
[14:30:00] PEER REVIEW: Starting review of presentation
[14:30:05] PEER REVIEW: Presentation detected - converting to images
[14:30:10] PDF REVIEW: Running pdf_to_images.py on presentation.pdf
[14:30:15] PDF REVIEW: Converted 25 slides to images in review/ directory
[14:30:20] PDF REVIEW: Inspecting slide 1/25 - title slide
[14:30:25] PDF REVIEW: Inspecting slide 2/25 - introduction
...
[14:35:40] PDF REVIEW: Inspecting slide 25/25 - acknowledgments
[14:35:45] PDF REVIEW: Completed image-based review
[14:35:50] PEER REVIEW: Found 8 layout issues, 3 content issues
[14:35:55] PEER REVIEW: Generating structured feedback by slide number
```

**Remember:** For presentations, the visual inspection via images is MANDATORY. Never attempt to read presentation PDFs as text - it will fail and miss all visual formatting issues.

## Resources

This skill includes reference materials to support comprehensive peer review:

### references/reporting_standards.md
Guidelines for reporting standards (CONSORT, PRISMA, ARRIVE, MIAME, STROBE, TRIPOD, SRQR, etc.) to evaluate completeness of methods and results reporting. These are optional clinical-domain checklists invoked only when the manuscript targets a clinical or medical venue.

### references/common_issues.md
Catalog of frequent methodological and statistical issues encountered in peer review, with guidance on identifying and addressing them.

## Final Checklist

Before finalizing the review, verify:

- [ ] Summary statement clearly conveys overall assessment
- [ ] Major concerns are clearly identified and justified
- [ ] Suggested revisions are specific and actionable
- [ ] Minor issues are noted but properly categorized
- [ ] Statistical methods have been evaluated
- [ ] Reproducibility and data availability assessed
- [ ] Ethical considerations verified
- [ ] Figures and tables evaluated for quality and integrity
- [ ] Writing quality assessed
- [ ] Tone is constructive and professional throughout
- [ ] Review is thorough but proportionate to manuscript scope
- [ ] Recommendation is consistent with identified issues

