---
name: scientific-schematics
description: Create publication-quality scientific diagrams using gpt-image-2 via the image-gen tool, with GPT-5.5 quality review and iterative refinement. Specialized in neural network architectures, system diagrams, data-flow pipelines, and complex scientific visualizations.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Scientific Schematics and Diagrams

## Overview

Scientific schematics and diagrams transform complex concepts into clear visual representations for publication. **This skill uses gpt-image-2 (via image-gen) for diagram generation with GPT-5.5 quality review.**

**How it works:**
- Describe your diagram in natural language
- gpt-image-2 generates publication-quality images automatically
- **GPT-5.5 reviews quality** against document-type thresholds
- **Smart iteration**: Only regenerates if quality is below threshold
- Publication-ready output in minutes
- One-time OAuth login (no per-request API key needed)

**Quality Thresholds by Document Type:**
| Document Type | Threshold | Description |
|---------------|-----------|-------------|
| journal | 8.5/10 | Nature, Science, peer-reviewed journals |
| conference | 8.0/10 | Conference papers |
| thesis | 8.0/10 | Dissertations, theses |
| grant | 8.0/10 | Grant proposals |
| preprint | 7.5/10 | arXiv, bioRxiv, etc. |
| report | 7.5/10 | Technical reports |
| poster | 7.0/10 | Academic posters |
| presentation | 6.5/10 | Slides, talks |
| default | 7.5/10 | General purpose |

**Simply describe what you want, and gpt-image-2 creates it.** All diagrams are stored in the figures/ subfolder and referenced in papers/posters.

**Supported figure modalities for systems papers.** Beyond raster image generation via the image-gen tool (which is opt-in), this skill supports TikZ and pgfplots (in-LaTeX vector graphics compiled with the manuscript), matplotlib and seaborn (Python scripts producing PDF/PNG), plotly (interactive HTML figures), and Inkscape SVG (hand-drawn vector diagrams). Use whichever tool best matches the figure type: TikZ/pgfplots for architecture and data-plot figures that must stay in sync with LaTeX styling; matplotlib/seaborn for scripted statistical plots; the image-gen tool when a quick raster mock-up suffices.

## Quick Start: Generate Any Diagram

Create any scientific diagram by simply describing it. gpt-image-2 handles everything automatically with **smart iteration**.

Set the CLI path once:
```
IMAGE_GEN="node $CLAUDE_PLUGIN_ROOT/tools/image-generator/dist/cli.js"
```

```bash
# Generate for journal paper (highest quality threshold: 8.5/10)
$IMAGE_GEN generate -p "Distributed transaction processing pipeline: client request through load balancer, consensus module, write-ahead log, and storage backend" -o figures/txn_pipeline.png --quality high

# Generate for presentation (standard quality, faster)
$IMAGE_GEN generate -p "Transformer encoder-decoder architecture showing multi-head attention" -o figures/transformer.png

# Generate for poster
$IMAGE_GEN generate -p "Multi-tier cache hierarchy diagram: L1, L2, shared L3, DRAM controller, and NVMe storage layers" -o figures/cache_hierarchy.png
```

**What happens behind the scenes:**
1. **Generation**: gpt-image-2 creates the image following scientific diagram best practices
2. **Review**: GPT-5.5 reads the output PNG and evaluates quality against the document-type threshold
3. **Decision**: If quality >= threshold → **DONE**
4. **If below threshold**: Improved prompt based on critique, regenerate (max 2 iterations total)
5. **Repeat**: Until quality meets threshold OR max iterations reached

**Smart Iteration Benefits:**
- Saves API calls if first generation is good enough
- Higher quality standards for journal papers
- Faster turnaround for presentations/posters
- Appropriate quality for each use case

**Output**: Image file plus a detailed review log with quality scores, critiques, and early-stop information.

### Configuration

One-time OAuth login (opens browser):
```bash
$IMAGE_GEN login
```

Verify credentials:
```bash
$IMAGE_GEN status
```

### AI Generation Best Practices

**Effective Prompts for Scientific Diagrams:**

Good prompts (specific, detailed):
- "Distributed storage write path: client → API gateway → consensus module (Raft) → write-ahead log → memtable → SSTable flush to disk"
- "Transformer neural network architecture with encoder stack on left, decoder stack on right, showing multi-head attention and cross-attention connections"
- "Multi-threaded request processing pipeline: incoming socket → thread pool dispatcher → parser → query planner → execution engine → response serializer"
- "Block diagram of IoT system: sensors → microcontroller → WiFi module → cloud server → mobile app"

Avoid vague prompts:
- "Make a flowchart" (too generic)
- "Neural network" (which type? what components?)
- "System diagram" (which system? what components?)

**Key elements to include:**
- **Type**: Flowchart, architecture diagram, pipeline, circuit, etc.
- **Components**: Specific elements to include
- **Flow/Direction**: How elements connect (left-to-right, top-to-bottom)
- **Labels**: Key annotations or text to include
- **Style**: Any specific visual requirements

## When to Use This Skill

This skill should be used when:
- Creating neural network architecture diagrams (Transformers, CNNs, RNNs, etc.)
- Illustrating system architectures and data flow diagrams
- Drawing system architecture diagrams, data-flow pipelines, and build/deploy flows
- Visualizing algorithm workflows, state machines, and request processing pipelines
- Creating circuit diagrams and electrical schematics
- Depicting system architectures, data pipelines, and algorithm flows
- Generating network topologies and hierarchical structures
- Illustrating conceptual frameworks and theoretical models
- Designing block diagrams for technical papers

**Graphical abstracts are OPTIONAL.** Systems papers typically do not include one. Generate only when the venue explicitly requests it (some life-science journals, certain Nature-family venues, some popular-press summary requests).

## How to Use This Skill

**Simply describe your diagram in natural language.** gpt-image-2 generates it automatically:

```bash
$IMAGE_GEN generate -p "your diagram description" -o output.png
```

**That's it!** The AI handles:
- Layout and composition
- Labels and annotations
- Colors and styling
- Publication-ready output

**Works for all diagram types:**
- Flowcharts (request routing, CI/CD pipelines, etc.)
- Neural network architectures
- System architectures
- Circuit diagrams
- Block diagrams
- Any scientific visualization

**No coding, no templates, no manual drawing required.**

---

# AI Generation Mode (gpt-image-2 + Claude Review)

## Generation Procedure

When generating a scientific diagram, follow these steps:

### Step 1: Construct the enriched prompt

Combine the user's diagram description with these scientific diagram guidelines:

**VISUAL QUALITY:**
- Clean white or light background (no textures or gradients)
- High contrast for readability and printing
- Professional, publication-ready appearance
- Sharp, clear lines and text
- Adequate spacing between elements to prevent crowding

**TYPOGRAPHY:**
- Clear, readable sans-serif fonts (Arial, Helvetica style)
- Minimum 10pt font size for all labels
- Consistent font sizes throughout
- All text horizontal or clearly readable
- No overlapping text

**SCIENTIFIC STANDARDS:**
- Accurate representation of concepts
- Clear labels for all components
- Include scale bars, legends, or axes where appropriate
- Use standard scientific notation and symbols
- Include units where applicable

**ACCESSIBILITY:**
- Colorblind-friendly color palette (use Okabe-Ito colors if using color)
- High contrast between elements
- Redundant encoding (shapes + colors, not just colors)
- Works well in grayscale

**LAYOUT:**
- Logical flow (left-to-right or top-to-bottom)
- Clear visual hierarchy
- Balanced composition
- Appropriate use of whitespace
- No clutter or unnecessary decorative elements

**NO FIGURE NUMBERS:**
- Do NOT include "Figure 1:", "Fig. 1", or any figure numbering in the image
- Do NOT add captions or titles like "Figure: ..." at the top or bottom
- Figure numbers and captions are added separately in the document/LaTeX
- The diagram should contain only the visual content itself

Prepend these guidelines to the user's prompt, then generate.

### Step 2: Generate the image

```bash
$IMAGE_GEN generate -p "<enriched_prompt>" -o <output_path> --quality high
```

Use `--quality high` for journal/conference/thesis/grant doc-types.
Use default quality for poster/presentation/report/preprint doc-types.

### Step 3: Review the generated image

Run the review command to get a structured quality evaluation from GPT 5.5:

```bash
$IMAGE_GEN review -i <output_path> --doc-type <doc_type>
```

The review command sends the image to GPT 5.5 for multimodal analysis. It scores on 5 criteria (0-2 points each):

1. **Scientific Accuracy** — correct representation, proper notation, accurate relationships
2. **Clarity and Readability** — easy to understand, clear visual hierarchy, no ambiguity
3. **Label Quality** — all elements labeled, readable fonts, consistent style
4. **Layout and Composition** — logical flow, balanced space, no overlapping
5. **Professional Appearance** — publication-ready, clean lines, appropriate colors

The command writes a `_review.json` file next to the image containing:
- `review_json`: structured scores, strengths, issues, and passes/fails verdict
- `total`: combined score (0-10)
- `passes`: whether the score meets the document-type threshold

Read the `_review.json` file to check the score and verdict.

### Step 4: Decision

Read the review output JSON. Check `passes` (true means score >= threshold).

If `passes: true`: **DONE**. Report the score and output path.
If `passes: false` and iterations remain (max 2 total): proceed to Step 5.

### Step 5: Refinement (max 2 iterations total)

Use `image-gen variant` to improve based on the `issues` field from the review:
```bash
$IMAGE_GEN variant -i <current_image> -p "<critique-based improvement prompt>" -o <output_path>
```

Or re-generate with an improved prompt that addresses specific issues. Then return to Step 3.

### Step 6: Write review log

After completion, save a review log at `<output_stem>_review_log.json` using the Write tool:
```json
{
  "user_prompt": "<original prompt>",
  "doc_type": "<doc_type>",
  "quality_threshold": <threshold>,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "<path>",
      "score": <score>,
      "needs_improvement": <bool>,
      "critique": "<review text>"
    }
  ],
  "final_score": <score>,
  "early_stop": <bool>,
  "early_stop_reason": "<reason or null>"
}
```

## Example Review Output

```
SCORE: 8.0

STRENGTHS:
- Clear flow from top to bottom
- All components properly labeled
- Professional typography

ISSUES:
- Some labels slightly small
- Minor spacing inconsistency

VERDICT: ACCEPTABLE (for conference, threshold 8.0)
```

## AI Generation Examples

### Example 1: Distributed System Architecture
```bash
$IMAGE_GEN generate -p "Distributed transaction processing pipeline architecture diagram. \
   Left: Client layer with three application nodes in light blue boxes. \
   Middle: API gateway (green box) routing to consensus module (Raft cluster, 3 nodes). \
   Consensus module connects to write-ahead log (orange cylinder). \
   Right: Storage backend with memtable in RAM (purple box) and SSTables on disk (gray cylinders). \
   Show compaction thread (red arrow) merging SSTables in background. \
   Include throughput annotations: 100K ops/sec at client, 50K ops/sec at consensus. \
   Use dashed arrows for async paths, solid for synchronous. \
   Clean block-diagram style with left-to-right data flow." \
  -o figures/txn_pipeline.png --quality high
```

### Example 2: Neural Network Architecture
```bash
$IMAGE_GEN generate -p "Transformer encoder-decoder architecture diagram. \
   Left side: Encoder stack with input embedding, positional encoding, \
   multi-head self-attention, add & norm, feed-forward, add & norm. \
   Right side: Decoder stack with output embedding, positional encoding, \
   masked self-attention, add & norm, cross-attention (receiving from encoder), \
   add & norm, feed-forward, add & norm, linear & softmax. \
   Show cross-attention connection from encoder to decoder with dashed line. \
   Use light blue for encoder, light red for decoder. \
   Label all components clearly." \
  -o figures/transformer.png --quality high
```

### Example 3: Multi-Tier Cache Hierarchy
```bash
$IMAGE_GEN generate -p "Multi-tier cache hierarchy diagram for a multi-core processor. \
   Top: Four CPU cores (blue squares) each with private L1 cache (light blue). \
   Each core pair shares an L2 cache (green rounded rectangles). \
   All cores connect to a shared L3 cache (large orange rectangle). \
   Below L3: DRAM controller (purple box) connected to DDR5 modules (gray rectangles). \
   Bottom: NVMe storage controller (red box) connected to SSD array. \
   Show cache-line transfer sizes between each level: 64B (L1-L2), 64B (L2-L3), 64B (L3-DRAM), 4KB (DRAM-SSD). \
   Include latency annotations: 1ns (L1), 4ns (L2), 12ns (L3), 80ns (DRAM), 10us (SSD). \
   Use decreasing-size arrows to represent bandwidth narrowing. \
   Vertical layout, top-to-bottom hierarchy." \
  -o figures/cache_hierarchy.png
```

### Example 4: System Architecture
```bash
$IMAGE_GEN generate -p "IoT system architecture block diagram. \
   Bottom layer: Sensors (temperature, humidity, motion) in green boxes. \
   Middle layer: Microcontroller (ESP32) in blue box. \
   Connections to WiFi module (orange box) and Display (purple box). \
   Top layer: Cloud server (gray box) connected to mobile app (light blue box). \
   Show data flow arrows between all components. \
   Label connections with protocols: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_architecture.png
```

---

## Prompt Engineering Tips

**1. Be Specific About Layout:**
- "Flowchart with vertical flow, top to bottom"
- "Architecture diagram with encoder on left, decoder on right"
- "Circular pipeline diagram with clockwise flow"

**2. Include Quantitative Details:**
- "Neural network with input layer (784 nodes), hidden layer (128 nodes), output (10 nodes)"
- "Flowchart showing 500 requests/sec throughput, 150 dropped, 350 processed"
- "Circuit with 1kΩ resistor, 10µF capacitor, 5V source"

**3. Specify Visual Style:**
- "Minimalist block diagram with clean lines"
- "Detailed system architecture with component interactions"
- "Technical schematic with engineering notation"

**4. Request Specific Labels:**
- "Label all arrows with data types"
- "Include layer dimensions in each box"
- "Show time progression with timestamps"

**5. Mention Color Requirements:**
- "Use colorblind-friendly colors"
- "Grayscale-compatible design"
- "Color-code by function: blue for input, green for processing, red for output"

## Common Failure Modes and Prompt Locks

Two specific prompt-level failure modes recur often enough to deserve their own
dedicated locks at the top of any non-trivial diagram prompt. Both have been
observed to slip past the GPT-5.5 reviewer with a passing score, so they
cannot be relied on to be caught downstream — they must be prevented in the
prompt itself.

### Failure mode 1: Cross-view inconsistency

When the same conceptual entity (a data layout, a fixed mapping, an enum
partition) appears across multiple views of one figure — say, source-side
illustration plus a table plus a runtime trace plus a final artifact — a
plain prompt that re-describes the entity in each view will let the
generation model independently re-invent specifics in each view. The
typical symptom is that one view shows a 1-invariant + 2-variant split
while another view shows a 2-invariant + 1-variant split, producing an
internal contradiction that auditors and reviewers catch as an accuracy
error.

The fix is to reserve a `CRITICAL CONSISTENCY` block at the very top of
the prompt that defines the entity once, then have each view reference it
rather than redefining it.

Example:

```
== CRITICAL CONSISTENCY ==
The contract has exactly 3 PUSH positions:
- PUSH 1 = variant
- PUSH 2 = invariant (value 0xCC)
- PUSH 3 = variant
This 1-invariant + 2-variant split must hold consistently in every view
where it appears: member cards, per-member constant table, classifier
chips, runtime variant tables, shared compiled artifact.
```

Subsequent view descriptions should refer to this lock ("orange variant,
green invariant per the consistency block"), not re-state the partition
from scratch.

### Failure mode 2: Discontinuous arrows

A prompt that says "an arrow goes from A, crosses the divider, and reaches
B" lets the generation model render two disconnected stub arrows, one
ending at the divider and another beginning on the other side. The visual
gap reads as a broken connection. This is particularly common when the
arrow path crosses any visual element (divider line, quadrant boundary,
text label).

The fix is to mandate single-polyline continuity explicitly:

```
== CRITICAL ARROW CONTINUITY ==
Every arrow must be a single continuous unbroken polyline from its source
box to an arrowhead at its target box. Arrows must not have gaps, breaks,
or detached segments. Bends are allowed at right angles, but every bend
must be a single connected joint, not two separate arrows.
```

For arrows that span large regions (across a divider, across a quadrant
boundary), additionally specify the path geometry rather than the
endpoints alone: "starts at the bottom of X, goes straight down crossing
the divider, makes ONE left turn, ends with its arrowhead pointing at the
top of Y; this must be one connected polyline, not two separate
segments."

### Why these belong at the top of the prompt

Both failure modes have produced 10/10 GPT-5.5 review scores while
exhibiting the defect, because the reviewer evaluates accuracy at the
view level (each table looks correct on its own) and clarity at the
local arrow level (each stub looks like a clean arrow on its own) rather
than auditing cross-view facts or end-to-end arrow paths. Catching these
at review time is therefore not reliable; preventing them at prompt time
is.

## Programmatic Access

The image-gen CLI is the recommended interface for diagram generation. For direct Node.js usage (e.g. scripting or integration), see `tools/image-generator/README.md`.

## Best Practices Summary

### Design Principles

1. **Clarity over complexity** - Simplify, remove unnecessary elements
2. **Consistent styling** - Use templates and style files
3. **Colorblind accessibility** - Use Okabe-Ito palette, redundant encoding
4. **Appropriate typography** - Sans-serif fonts, minimum 7-8 pt
5. **Vector format** - Always use PDF/SVG for publication

### Technical Requirements

1. **Resolution** - Vector preferred, or 300+ DPI for raster
2. **File format** - PDF for LaTeX, SVG for web, PNG as fallback
3. **Color space** - RGB for digital, CMYK for print (convert if needed)
4. **Line weights** - Minimum 0.5 pt, typical 1-2 pt
5. **Text size** - 7-8 pt minimum at final size

### Integration Guidelines

1. **Include in LaTeX** - Use `\includegraphics{}` for generated images
2. **Caption thoroughly** - Describe all elements and abbreviations
3. **Reference in text** - Explain diagram in narrative flow
4. **Maintain consistency** - Same style across all figures in paper
5. **Version control** - Keep prompts and generated images in repository

## Troubleshooting Common Issues

### AI Generation Issues

**Problem**: Overlapping text or elements
- Make your prompt more specific about spacing and layout
- Request explicit spacing between elements in the prompt

**Problem**: Elements not connecting properly
- Make your prompt more specific about connections and data flow
- Specify arrow types (solid, dashed) and directions

### Image Quality Issues

**Problem**: Text too small
- Explicitly request "minimum 10pt font" in the prompt
- Specify label sizes relative to the diagram

**Problem**: Low quality for print
- Use `--quality high` flag
- Request "publication-ready, 300 DPI equivalent" in the prompt

### Authentication Issues

**Problem**: "No saved credentials" error
- Run `$IMAGE_GEN login` to authenticate via browser (one-time)
- Verify with `$IMAGE_GEN status`

**Problem**: Token expired
- Tokens auto-refresh, but if refresh fails, run `$IMAGE_GEN login` again

## Resources and References

### Detailed References

Load these files for comprehensive information on specific topics:

- **`references/best_practices.md`** - Publication standards and accessibility guidelines

### External Resources

**Python Libraries**
- Schemdraw Documentation: https://schemdraw.readthedocs.io/
- NetworkX Documentation: https://networkx.org/documentation/
- Matplotlib Documentation: https://matplotlib.org/

**Publication Standards**
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- IEEE Graphics Guidelines: https://www.ieee.org/publications/reviewers/graphics.html

## Integration with Other Skills

This skill works synergistically with:

- **Scientific Writing** - Diagrams follow figure best practices
- **LaTeX Posters** - Generate diagrams for poster presentations
- **Research Grants** - Methodology diagrams for proposals
- **Peer Review** - Evaluate diagram clarity and accessibility

## Quick Reference Checklist

Before submitting diagrams, verify:

### Visual Quality
- [ ] High-quality image format (PNG from image-gen)
- [ ] No overlapping elements
- [ ] Adequate spacing between all components
- [ ] Clean, professional alignment
- [ ] All arrows connect properly to intended targets

### Accessibility
- [ ] Colorblind-safe palette (Okabe-Ito) used
- [ ] Works in grayscale
- [ ] Sufficient contrast between elements
- [ ] Redundant encoding where appropriate (shapes + colors)

### Typography and Readability
- [ ] Text minimum 7-8 pt at final size
- [ ] All elements labeled clearly and completely
- [ ] Consistent font family and sizing
- [ ] No text overlaps or cutoffs
- [ ] Units included where applicable

### Publication Standards
- [ ] Consistent styling with other figures in manuscript
- [ ] Comprehensive caption written with all abbreviations defined
- [ ] Referenced appropriately in manuscript text
- [ ] Meets journal-specific dimension requirements
- [ ] Exported in required format for journal (PDF/EPS/TIFF)

### Documentation and Version Control
- [ ] Source prompts saved for future regeneration
- [ ] Quality review log archived with figure files
- [ ] Git commit includes prompt, output, and review log
- [ ] README or comments explain how to regenerate figure

### Final Integration Check
- [ ] Figure displays correctly in compiled manuscript
- [ ] Cross-references work (`\ref{}` points to correct figure)
- [ ] Figure number matches text citations
- [ ] Caption appears on correct page relative to figure
- [ ] No compilation warnings or errors related to figure

## Environment Setup

```bash
# One-time setup
cd $CLAUDE_PLUGIN_ROOT/tools/image-generator && npm install && npm run build
node dist/cli.js login  # Opens browser for OAuth
```

## Getting Started

**Simplest possible usage:**
```bash
IMAGE_GEN="node $CLAUDE_PLUGIN_ROOT/tools/image-generator/dist/cli.js"
$IMAGE_GEN generate -p "your diagram description" -o output.png
```

---

Use this skill to create clear, accessible, publication-quality diagrams that effectively communicate complex scientific concepts. The AI-powered workflow with GPT-5.5 iterative review ensures diagrams meet professional standards.
