#!/usr/bin/env python3
"""
Extract images from sessions.ndjson file
Images are stored as base64 encoded data in the previewcontent field
"""

import json
import base64
import os
from pathlib import Path

def extract_images():
    # Set up paths
    data_file = Path("./data/sessions.ndjson")
    output_dir = Path("./extracted-content")
    
    print(f"Reading from: {data_file}")
    print(f"Extracting to: {output_dir}")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    image_count = 0
    metadata_list = []
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    session = json.loads(line.strip())
                    
                    # Check if this session has image preview content
                    preview_type = session.get('previewcontenttype', '')
                    if preview_type.startswith('image/'):
                        preview_content = session.get('previewcontent', '')
                        
                        if preview_content:
                            # Extract metadata
                            session_guid = session.get('sessionguid', 'unknown')
                            session_number = session.get('sessionnumber', 'unknown')
                            start_time = session.get('starttime', 'unknown')
                            content_type = preview_type
                            
                            # Determine file extension
                            ext = 'png' if 'png' in content_type else 'jpg'
                            
                            # Create filename
                            filename = f"session_{session_number}_{session_guid[:8]}.{ext}"
                            filepath = output_dir / filename
                            
                            try:
                                # Decode base64 and save image
                                image_data = base64.b64decode(preview_content)
                                
                                with open(filepath, 'wb') as img_file:
                                    img_file.write(image_data)
                                
                                image_count += 1
                                
                                # Store metadata
                                metadata = {
                                    'filename': filename,
                                    'session_guid': session_guid,
                                    'session_number': session_number,
                                    'start_time': start_time,
                                    'content_type': content_type,
                                    'file_size': len(image_data),
                                    'source_line': line_num,
                                    'extracted_to': str(filepath)
                                }
                                metadata_list.append(metadata)
                                
                                print(f"Extracted: {filename} ({len(image_data)} bytes, {content_type})")
                                
                            except Exception as e:
                                print(f"Error decoding image on line {line_num}: {e}")
                                continue
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error on line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
    
    except FileNotFoundError:
        print(f"Error: Could not find {data_file}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Save metadata
    metadata_file = output_dir / "extracted_images_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extraction complete!")
    print(f"   Total images extracted: {image_count}")
    print(f"   Metadata saved to: {metadata_file}")
    
    # Create summary
    summary_file = output_dir / "image_extraction_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Image Extraction Summary\n\n")
        f.write(f"**Date**: 2025-07-08\n")
        f.write(f"**Source**: `{data_file}`\n")
        f.write(f"**Total Images Extracted**: {image_count}\n\n")
        
        f.write("## Extracted Images\n\n")
        for img in metadata_list:
            f.write(f"### {img['filename']}\n")
            f.write(f"- **Session GUID**: {img['session_guid']}\n")
            f.write(f"- **Session Number**: {img['session_number']}\n")
            f.write(f"- **Start Time**: {img['start_time']}\n")
            f.write(f"- **Content Type**: {img['content_type']}\n")
            f.write(f"- **File Size**: {img['file_size']:,} bytes\n")
            f.write(f"- **Source Line**: {img['source_line']}\n\n")
        
        f.write("## Analysis\n\n")
        png_count = sum(1 for img in metadata_list if img['content_type'] == 'image/png')
        jpg_count = sum(1 for img in metadata_list if img['content_type'] == 'image/jpeg')
        
        f.write(f"- **PNG Images**: {png_count}\n")
        f.write(f"- **JPEG Images**: {jpg_count}\n")
        
        total_size = sum(img['file_size'] for img in metadata_list)
        f.write(f"- **Total Size**: {total_size:,} bytes ({total_size/1024:.1f} KB)\n")
        
        # Time range analysis
        times = [img['start_time'] for img in metadata_list if img['start_time'] != 'unknown']
        if times:
            f.write(f"- **Time Range**: {min(times)} to {max(times)}\n")
    
    print(f"   Summary saved to: {summary_file}")

if __name__ == "__main__":
    extract_images()