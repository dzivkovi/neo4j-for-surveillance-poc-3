#!/usr/bin/env python3
"""
Clean markdown files for LLM consumption by handling embedded images.

Options:
1. Strip images completely (default)
2. Extract images to files and replace with links
3. Create both versions
"""

import argparse
import base64
import re
import os
from pathlib import Path
from typing import Tuple, List


def extract_base64_images(content: str, output_dir: Path = None) -> Tuple[str, List[str]]:
    """
    Extract base64 images from markdown content.
    
    Args:
        content: Markdown content with embedded images
        output_dir: Directory to save extracted images (if provided)
    
    Returns:
        Tuple of (cleaned content, list of extracted image paths)
    """
    # Pattern to match markdown images with base64 data
    pattern = r'!\[([^\]]*)\]\(data:image/([^;]+);base64,([^)]+)\)'
    
    extracted_images = []
    image_counter = 0
    
    def replace_image(match):
        nonlocal image_counter
        alt_text = match.group(1) or f"Image{image_counter}"
        image_format = match.group(2)
        base64_data = match.group(3)
        
        if output_dir:
            # Save image to file
            image_counter += 1
            filename = f"image_{image_counter:03d}.{image_format}"
            filepath = output_dir / filename
            
            try:
                # Decode and save image
                image_data = base64.b64decode(base64_data)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                extracted_images.append(str(filepath))
                # Return markdown link to the extracted image
                return f"![{alt_text}]({filename})"
            except Exception as e:
                print(f"Warning: Failed to extract image {image_counter}: {e}")
                return f"[{alt_text} - Image extraction failed]"
        else:
            # Just return placeholder text
            return f"[{alt_text}]"
    
    # Replace all base64 images
    cleaned_content = re.sub(pattern, replace_image, content)
    
    return cleaned_content, extracted_images


def process_markdown_file(input_path: Path, mode: str = 'strip') -> None:
    """
    Process a markdown file to handle embedded images.
    
    Args:
        input_path: Path to the markdown file
        mode: Processing mode - 'strip', 'extract', or 'both'
    """
    print(f"Processing: {input_path.name}")
    
    # Read the original file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # Create output paths
    base_dir = input_path.parent
    stem = input_path.stem
    
    if mode in ['extract', 'both']:
        # Create directory for extracted images
        images_dir = base_dir / f"{stem}_images"
        images_dir.mkdir(exist_ok=True)
        
        # Extract images and create linked version
        linked_content, extracted = extract_base64_images(content, images_dir)
        
        linked_path = base_dir / f"{stem}_linked.md"
        with open(linked_path, 'w', encoding='utf-8') as f:
            f.write(linked_content)
        
        print(f"  ✓ Created linked version: {linked_path.name}")
        print(f"  ✓ Extracted {len(extracted)} images to: {images_dir.name}/")
    
    if mode in ['strip', 'both']:
        # Create text-only version
        text_content, _ = extract_base64_images(content, output_dir=None)
        
        text_path = base_dir / f"{stem}_text.md"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        text_size = len(text_content)
        reduction = (1 - text_size / original_size) * 100
        
        print(f"  ✓ Created text-only version: {text_path.name}")
        print(f"  ✓ Size reduction: {reduction:.1f}% ({original_size:,} → {text_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(
        description="Clean markdown files for LLM consumption by handling embedded images"
    )
    parser.add_argument(
        'files', 
        nargs='+', 
        type=Path,
        help='Markdown files to process'
    )
    parser.add_argument(
        '--mode', 
        choices=['strip', 'extract', 'both'],
        default='strip',
        help='Processing mode: strip (text-only), extract (with links), or both'
    )
    
    args = parser.parse_args()
    
    print(f"Processing mode: {args.mode}")
    print(f"Files to process: {len(args.files)}\n")
    
    for file_path in args.files:
        if file_path.exists() and file_path.suffix == '.md':
            process_markdown_file(file_path, args.mode)
        else:
            print(f"Skipping: {file_path} (not a markdown file or doesn't exist)")
        print()


if __name__ == "__main__":
    main()