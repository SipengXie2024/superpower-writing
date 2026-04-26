# Scientific Schematics - Image Generation

**Generate any scientific diagram by describing it in natural language.**

gpt-image-2 (via image-gen) creates publication-quality diagrams automatically — no coding, no templates, no manual drawing required. GPT-5.5 reviews quality automatically.

## Quick Start

### Generate Any Diagram

```bash
# Set CLI path
IMAGE_GEN="node $CLAUDE_PLUGIN_ROOT/tools/image-generator/dist/cli.js"

# Authenticate (one-time, opens browser)
$IMAGE_GEN login

# Generate a scientific diagram
$IMAGE_GEN generate -p "Distributed storage write path: client → gateway → consensus → WAL → memtable → SSTable" -o figures/write_path.png

# Neural network architecture
$IMAGE_GEN generate -p "Transformer encoder-decoder architecture with cross-attention" -o figures/transformer.png --quality high

# System pipeline
$IMAGE_GEN generate -p "Request processing pipeline with thread pool and query planner" -o figures/pipeline.png
```

### What You Get

- **Generated image** (PNG) following scientific diagram best practices
- **Metadata file** (`*.meta.json`) with model info and timestamp
- **Quality review** (`*_review.json`) scored by GPT-5.5 against document-type thresholds
- **Review log** (`*_review_log.json`) with iteration scores and critiques

## Features

### Quality Review Process

1. **Generation**: gpt-image-2 creates the diagram from your description
2. **Review**: GPT-5.5 reads the output PNG and scores on 5 criteria (0-2 each)
3. **Decision**: If score >= threshold → done. Otherwise, refine and retry (max 2 iterations)

Run a review manually:
```bash
$IMAGE_GEN review -i figures/diagram.png --doc-type conference
```

### Automatic Quality Standards

All diagrams are generated following:
- Clean white/light background
- High contrast for readability
- Clear labels (minimum 10pt font)
- Professional typography (sans-serif)
- Colorblind-friendly colors (Okabe-Ito)
- Proper spacing between elements
- No figure numbers or captions in the image

## Installation

```bash
# Build the image-gen tool (one-time)
cd $CLAUDE_PLUGIN_ROOT/tools/image-generator
npm install && npm run build

# Authenticate (opens browser for OAuth)
node dist/cli.js login
```

Requires a ChatGPT Plus/Pro account.

## Usage Examples

### Example 1: System Architecture

```bash
$IMAGE_GEN generate -p "Distributed transaction processing pipeline. \
   Client layer (3 nodes) → API gateway → consensus module (Raft, 3 nodes) \
   → write-ahead log → memtable → SSTable. \
   Show compaction thread merging SSTables. \
   Include throughput: 100K ops/sec client, 50K ops/sec consensus. \
   Dashed arrows for async, solid for sync. Left-to-right flow." \
  -o figures/txn_pipeline.png --quality high
```

**Output:**
- `figures/txn_pipeline.png` - Generated image
- `figures/txn_pipeline.meta.json` - Generation metadata
- `figures/txn_pipeline_review_log.json` - Quality review log

### Example 2: Neural Network Architecture

```bash
$IMAGE_GEN generate -p "Transformer encoder-decoder. \
   Encoder: input embedding → positional encoding → multi-head self-attention → \
   add & norm → feed-forward → add & norm. \
   Decoder: output embedding → positional encoding → masked self-attention → \
   add & norm → cross-attention → add & norm → feed-forward → add & norm → linear & softmax. \
   Dashed cross-attention connection from encoder to decoder. \
   Light blue encoder, light red decoder." \
  -o figures/transformer.png --quality high
```

### Example 3: Cache Hierarchy

```bash
$IMAGE_GEN generate -p "Multi-tier cache hierarchy for multi-core processor. \
   Top: 4 CPU cores (blue) with private L1 (light blue). \
   Core pairs share L2 (green). All share L3 (orange). \
   Below L3: DRAM controller (purple) → DDR5 (gray). \
   Bottom: NVMe controller (red) → SSD array. \
   Latency: 1ns L1, 4ns L2, 12ns L3, 80ns DRAM, 10us SSD. \
   Vertical layout, top-to-bottom." \
  -o figures/cache_hierarchy.png
```

### Example 4: IoT System

```bash
$IMAGE_GEN generate -p "IoT architecture. \
   Sensors (green) → ESP32 microcontroller (blue) → WiFi module (orange) + display (purple) \
   → cloud server (gray) → mobile app (light blue). \
   Label connections: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_system.png
```

## Command-Line Options

```bash
$IMAGE_GEN generate -p "description" -o output.png [OPTIONS]

Options:
  -p, --prompt <text>       Image generation prompt (required)
  -o, --output <path>       Output file path (required)
  --quality <level>         Quality: standard | high | auto (default: standard)
  --size <WxH>              Image dimensions (e.g. 1024x1024)
  --background <bg>         Background: transparent | opaque | auto
  --format <fmt>            Output format: png | jpeg | webp (default: png)
```

Other commands:
```bash
$IMAGE_GEN login             # Authenticate (opens browser)
$IMAGE_GEN status            # Check credential status
$IMAGE_GEN review -i <img> [--doc-type <type>]  # Review image quality via GPT-5.5
$IMAGE_GEN variant -i <img> -p "edit" -o <out>  # Create variant of existing image
$IMAGE_GEN edit -i <img> -p "edit" -o <out>     # Edit existing image
```

## Prompt Engineering Tips

### Be Specific About Layout
- "Flowchart with vertical flow, top to bottom"
- "Architecture diagram with encoder on left, decoder on right"
- Avoid: "Make a diagram" (too vague)

### Include Quantitative Details
- "Neural network: input (784), hidden (128), output (10)"
- "Pipeline: 500 req/s throughput, 150 dropped, 350 processed"
- Avoid: "Some numbers" (not specific)

### Specify Visual Style
- "Minimalist block diagram with clean lines"
- "Detailed system architecture with component interactions"
- "Technical schematic with engineering notation"

### Request Specific Labels
- "Label all arrows with data types"
- "Include layer dimensions in each box"
- "Show latency at each stage"

### Mention Color Requirements
- "Use colorblind-friendly colors"
- "Grayscale-compatible design"
- "Color-code by function: blue=input, green=processing, red=output"

## Review Log Format

Each generation produces a JSON review log:

```json
{
  "user_prompt": "Distributed storage write path...",
  "doc_type": "conference",
  "quality_threshold": 8.0,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/pipeline.png",
      "score": 8.0,
      "needs_improvement": false,
      "critique": "SCORE: 8.0\nSTRENGTHS: Clear flow, well-labeled..."
    }
  ],
  "final_score": 8.0,
  "early_stop": true,
  "early_stop_reason": "Quality score 8.0 meets threshold 8.0 for conference"
}
```

## Troubleshooting

### Authentication Issues

```bash
# Check credential status
$IMAGE_GEN status

# Re-authenticate if needed
$IMAGE_GEN login

# Remove stale credentials and re-login
$IMAGE_GEN logout
$IMAGE_GEN login
```

### Generation Fails

- Verify credentials: `$IMAGE_GEN status`
- Check network connectivity
- Try a simpler prompt first

### Low Quality Scores

If scores consistently fall below threshold:
1. Make your prompt more specific
2. Include more layout and label details
3. Specify visual requirements explicitly
4. Use `--quality high`

## Resources

- Full documentation: `SKILL.md`
- Quick reference: `QUICK_REFERENCE.md`
- Example script: `scripts/example_usage.sh`
