# Scientific Schematics - Quick Reference

**How it works:** Describe your diagram → gpt-image-2 generates it → GPT-5.5 reviews quality

## Setup (One-Time)

```bash
# Set CLI path
IMAGE_GEN="node $CLAUDE_PLUGIN_ROOT/tools/image-generator/dist/cli.js"

# Authenticate (opens browser, one-time)
$IMAGE_GEN login

# Verify credentials
$IMAGE_GEN status
```

Requires ChatGPT Plus/Pro account.

## Basic Usage

```bash
# Describe your diagram, gpt-image-2 creates it
$IMAGE_GEN generate -p "your diagram description" -o output.png

# Review quality via GPT-5.5
$IMAGE_GEN review -i output.png --doc-type conference
```

## Common Examples

### Cache Hierarchy
```bash
$IMAGE_GEN generate -p "Multi-tier cache hierarchy: L1, L2, shared L3, DRAM, NVMe" -o cache.png
```

### Neural Network
```bash
$IMAGE_GEN generate -p "Transformer encoder-decoder with multi-head attention" -o transformer.png
```

### System Pipeline
```bash
$IMAGE_GEN generate -p "Request processing pipeline: socket → dispatcher → parser → executor → response" -o pipeline.png
```

### Circuit Diagram
```bash
$IMAGE_GEN generate -p "Op-amp circuit with 1kΩ resistor and 10µF capacitor" -o circuit.png
```

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `-p, --prompt <text>` | Image generation prompt | `-p "cache hierarchy diagram"` |
| `-o, --output <path>` | Output file path | `-o figures/diagram.png` |
| `--quality <level>` | Quality: standard \| high \| auto | `--quality high` |
| `--size <WxH>` | Image size | `--size 1024x1024` |
| `--background <bg>` | Background: transparent \| opaque \| auto | `--background white` |
| `--format <fmt>` | Output format: png \| jpeg \| webp | `--format png` |

## Prompt Tips

### Good Prompts (Specific)
- "Cache hierarchy: L1 (private per core) → L2 (shared pair) → L3 (shared all) → DRAM, with latency annotations"
- "Transformer architecture: encoder on left with 6 layers, decoder on right, cross-attention connections"
- "Request pipeline: socket → thread pool → parser → query planner → executor → serializer, left-to-right"

### Avoid (Too Vague)
- "Make a flowchart"
- "Neural network"
- "System diagram"

## Output Files

For input `diagram.png`:
- `diagram.png` - Generated image
- `diagram.meta.json` - Generation metadata (model, timestamp, request ID)
- `diagram_review.json` - GPT-5.5 quality review (scores, critique, passes/fails)
- `diagram_review_log.json` - Iteration log with scores and critiques (written by Claude)

## Review Log

```json
{
  "iterations": [
    {
      "iteration": 1,
      "score": 8.0,
      "critique": "Good layout. Minor label spacing issues."
    }
  ],
  "final_score": 8.0,
  "early_stop": true,
  "early_stop_reason": "Quality score 8.0 meets threshold 8.0 for conference"
}
```

## Troubleshooting

### No Saved Credentials
```bash
$IMAGE_GEN login   # Re-authenticate
$IMAGE_GEN status  # Check credential status
```

### Low Quality Score
- Make prompt more specific about layout and spacing
- Include quantitative details (node counts, annotations)
- Specify visual style explicitly
- Use `--quality high`

### Generation Fails
- Verify credentials: `$IMAGE_GEN status`
- Check network connectivity
- Try a simpler prompt first

## Quick Start Checklist

- [ ] Run `$IMAGE_GEN login` (one-time)
- [ ] Verify: `$IMAGE_GEN status`
- [ ] Try: `$IMAGE_GEN generate -p "simple block diagram: A → B → C" -o test.png`
- [ ] Review output image and metadata
- [ ] Read SKILL.md for detailed documentation

## Resources

- Full documentation: `SKILL.md`
- Detailed guide: `README.md`
- Example script: `scripts/example_usage.sh`
