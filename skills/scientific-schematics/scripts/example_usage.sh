#!/bin/bash
# Example usage of scientific schematic generation via image-gen
#
# Prerequisites:
# 1. Build the tool: cd tools/image-generator && npm install && npm run build
# 2. Authenticate: node tools/image-generator/dist/cli.js login

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_GEN="node $SCRIPT_DIR/../../../tools/image-generator/dist/cli.js"

echo "=========================================="
echo "Scientific Schematics - Image Generation"
echo "Example Usage Demonstrations"
echo "=========================================="
echo ""

# Check for credentials
if ! $IMAGE_GEN status 2>/dev/null; then
    echo "Error: Not authenticated. Run '$IMAGE_GEN login' first."
    exit 1
fi

echo "Credentials OK"
echo ""

# Create output directory
mkdir -p figures

# Example 1: Distributed system pipeline
echo "Example 1: Distributed Transaction Pipeline"
echo "--------------------------------------------"
$IMAGE_GEN generate \
  -p "Distributed transaction processing pipeline. Client layer (3 blue boxes) → API gateway (green) → consensus module (Raft, 3 nodes) → write-ahead log (orange cylinder) → storage backend. Left-to-right flow. Clean block-diagram style." \
  -o figures/txn_pipeline_example.png \
  --quality high

echo ""
echo "Generated: figures/txn_pipeline_example.png"
echo ""

# Example 2: Neural network
echo "Example 2: Transformer Architecture"
echo "------------------------------------"
$IMAGE_GEN generate \
  -p "Transformer encoder-decoder architecture. Encoder stack on left (input embedding, positional encoding, multi-head attention, feed-forward). Decoder stack on right (masked attention, cross-attention, feed-forward). Cross-attention connection with dashed line. Light blue encoder, light red decoder. All components labeled." \
  -o figures/transformer_example.png \
  --quality high

echo ""
echo "Generated: figures/transformer_example.png"
echo ""

# Example 3: Cache hierarchy
echo "Example 3: Cache Hierarchy"
echo "--------------------------"
$IMAGE_GEN generate \
  -p "Multi-tier cache hierarchy. Top: 4 CPU cores with private L1. Core pairs share L2. All share L3. Below: DRAM controller → DDR5. Bottom: NVMe → SSD. Include latency: 1ns L1, 4ns L2, 12ns L3, 80ns DRAM, 10us SSD. Vertical layout, top-to-bottom." \
  -o figures/cache_example.png

echo ""
echo "Generated: figures/cache_example.png"
echo ""

# Example 4: Review the generated image
echo "Example 4: Quality Review"
echo "--------------------------"
$IMAGE_GEN review -i figures/cache_example.png --doc-type conference

echo ""
echo "Review complete. See figures/cache_example_review.json for details."
echo ""

echo "=========================================="
echo "All examples completed!"
echo "=========================================="
echo ""
echo "Generated files:"
ls -lh figures/*example*.png 2>/dev/null || echo "  (no files found)"
echo ""
echo "Metadata files (*.meta.json) contain model info and timestamps."
echo ""
