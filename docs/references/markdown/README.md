# Reference Documents in Markdown

This directory contains reference documents converted from PDF to Markdown format for LLM accessibility.

## File Types

### Original Files (with embedded images)
- `*.md` - Full markdown with base64-encoded images (large files, 2-4MB)
- Best for: Human viewing with full visual content

### LLM-Optimized Files
- `*_text.md` - Text-only versions with image placeholders (small files, 20-500KB)
- Best for: LLM processing, search, and analysis

## Size Comparison

| Document | Original PDF | Full Markdown | Text-Only | Reduction |
|----------|-------------|---------------|-----------|-----------|
| Neo4j Fraud Detection | ~1MB | 3.1MB | 22KB | 99.3% |
| OSCE Intelligence-Led Policing | ~2MB | 3.8MB | 245KB | 93.6% |
| POLE Data Standards | ~1MB | 2.9MB | 497KB | 82.7% |
| Social Network Analysis | ~500KB | 67KB | 42KB | 37.7% |

## Usage

### For LLMs (Claude, GPT, etc.)
Use the `*_text.md` files - they contain all the textual content without the overhead of embedded images.

### For Human Reading
Use the original `*.md` files if you need to see diagrams, charts, and other visual elements.

### Creating New Clean Versions
```bash
# Strip images (text-only)
python scripts/clean-markdown-for-llm.py document.md --mode strip

# Extract images to separate files
python scripts/clean-markdown-for-llm.py document.md --mode extract

# Create both versions
python scripts/clean-markdown-for-llm.py document.md --mode both
```

## Why This Matters

1. **Performance**: LLMs process text-only files 10-100x faster
2. **Token Efficiency**: Base64 images consume massive token counts
3. **Searchability**: Clean text is easier to search and index
4. **Version Control**: Smaller files work better with Git