#!/usr/bin/env python
"""
Extract and transform surveillance NDJSON sessions for Neo4j import.

This utility provides a flexible way to extract specific fields from large
surveillance NDJSON files, making them suitable for:
- Neo4j import pipelines
- AI/ML analysis (size-limited exports)
- Development/testing (minimal datasets)
- Data exploration and debugging

Unix philosophy: Transform NDJSON into focused, usable datasets.
"""

import argparse
import json
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, Optional, Set

# Core fields needed for investigative work in Neo4j
DEFAULT_FIELDS = {
    "sessionguid",  # Primary key
    "sessiontype",  # Telephony, Messaging, Email
    "starttime",  # Temporal analysis
    "stoptime",  # Session end time (actual field name)
    "durationinseconds",  # Call duration analysis
    "classification",  # Pertinent, Unknown
    "reviewstatus",  # Not Viewed, In Process, Completed
    "sourceid",  # Links to data source
    "displaytypeid",  # Links to phones/emails
    "targetname",  # Quick participant reference
    "involvements",  # CRITICAL for entity resolution (phones, emails, IMEIs)
}

# Fields that significantly increase file size
LARGE_FIELDS = {
    "products",  # Complex nested structures
    "previewcontent",  # Base64 encoded content
    "fulltext",  # Complete text content
    "enrichment_",  # AI/ML enrichments
    "trackpoints",  # Location data arrays
}

# Fields useful for debugging but not core functionality
DEBUG_FIELDS = {
    "createddate",
    "lastmodifydate",
    "decodestate",
    "isevidence",
    "attachmentstatus",
}


def get_json_size_mb(obj: Any) -> float:
    """Calculate JSON size in MB."""
    return len(json.dumps(obj)) / 1024 / 1024


def discover_fields(file_path: Path, sample_size: int = 100) -> Dict[str, int]:
    """
    Discover all unique fields in NDJSON file with occurrence counts.

    Args:
        file_path: Path to NDJSON file
        sample_size: Number of records to sample (0 for all)

    Returns:
        Dictionary of field names and their occurrence counts
    """
    field_counts = {}

    with open(file_path) as f:
        for i, line in enumerate(f):
            if sample_size > 0 and i >= sample_size:
                break

            try:
                record = json.loads(line.strip())
                for field in record.keys():
                    field_counts[field] = field_counts.get(field, 0) + 1
            except json.JSONDecodeError:
                print(f"⚠️  Skipping invalid JSON at line {i + 1}", file=sys.stderr)
                continue

    return field_counts


def extract_sessions(
    input_path: Path,
    output_path: Optional[Path],
    fields: Set[str],
    max_size_mb: Optional[float] = None,
    pretty: bool = True,
) -> Dict[str, Any]:
    """
    Extract specified fields from NDJSON sessions.

    Args:
        input_path: Input NDJSON file
        output_path: Output file (None for stdout)
        fields: Set of fields to extract
        max_size_mb: Maximum output size in MB
        pretty: Pretty-print JSON output

    Returns:
        Statistics about the extraction
    """
    stats = {
        "total_records": 0,
        "extracted_records": 0,
        "skipped_records": 0,
        "output_size_mb": 0,
        "sessiontype_counts": {},
        "classification_counts": {},
        "targetname_counts": {},
        "involvement_stats": {
            "total": 0,
            "with_msisdn": 0,
            "with_email": 0,
            "with_imei": 0,
            "with_personname": 0,
        },
    }

    extracted_sessions = []
    current_size_mb = 0

    with open(input_path) as f:
        for i, line in enumerate(f):
            stats["total_records"] += 1

            try:
                record = json.loads(line.strip())

                # Extract only requested fields
                extracted = {field: record[field] for field in fields if field in record}

                # Skip if no fields extracted
                if not extracted:
                    stats["skipped_records"] += 1
                    continue

                # Check size limit
                if max_size_mb:
                    record_size_mb = get_json_size_mb(extracted)
                    if current_size_mb + record_size_mb > max_size_mb:
                        print(f"⚠️  Size limit reached at record {i + 1}", file=sys.stderr)
                        break
                    current_size_mb += record_size_mb

                extracted_sessions.append(extracted)
                stats["extracted_records"] += 1

                # Collect statistics
                if "sessiontype" in extracted:
                    stype = extracted["sessiontype"]
                    stats["sessiontype_counts"][stype] = stats["sessiontype_counts"].get(stype, 0) + 1

                if "classification" in extracted:
                    ctype = extracted["classification"]
                    stats["classification_counts"][ctype] = stats["classification_counts"].get(ctype, 0) + 1

                if "targetname" in extracted:
                    tname = extracted["targetname"]
                    stats["targetname_counts"][tname] = stats["targetname_counts"].get(tname, 0) + 1

                # Analyze involvements for entity resolution
                if "involvements" in extracted:
                    for inv in extracted["involvements"]:
                        stats["involvement_stats"]["total"] += 1
                        if inv.get("msisdn"):
                            stats["involvement_stats"]["with_msisdn"] += 1
                        if inv.get("email"):
                            stats["involvement_stats"]["with_email"] += 1
                        if inv.get("imei"):
                            stats["involvement_stats"]["with_imei"] += 1
                        if inv.get("personname"):
                            stats["involvement_stats"]["with_personname"] += 1

            except json.JSONDecodeError:
                print(f"⚠️  Skipping invalid JSON at line {i + 1}", file=sys.stderr)
                stats["skipped_records"] += 1
                continue
            except Exception as e:
                print(f"⚠️  Error processing line {i + 1}: {e}", file=sys.stderr)
                stats["skipped_records"] += 1
                continue

    # Output results
    output_str = json.dumps(extracted_sessions, indent=2 if pretty else None, sort_keys=True)

    stats["output_size_mb"] = len(output_str) / 1024 / 1024

    if output_path:
        output_path.write_text(output_str)
        print(f"✅ Wrote {stats['extracted_records']} sessions to {output_path}", file=sys.stderr)
    else:
        print(output_str)

    return stats


def print_stats(stats: Dict[str, Any]) -> None:
    """Print extraction statistics to stderr."""
    print("\n📊 Extraction Statistics:", file=sys.stderr)
    print(f"   Total records read: {stats['total_records']:,}", file=sys.stderr)
    print(f"   Records extracted: {stats['extracted_records']:,}", file=sys.stderr)
    print(f"   Records skipped: {stats['skipped_records']:,}", file=sys.stderr)
    print(f"   Output size: {stats['output_size_mb']:.1f} MB", file=sys.stderr)

    if stats["sessiontype_counts"]:
        print("\n📞 Session Types:", file=sys.stderr)
        for stype, count in sorted(stats["sessiontype_counts"].items()):
            print(f"   {stype}: {count:,}", file=sys.stderr)

    if stats["classification_counts"]:
        print("\n🏷️  Classifications:", file=sys.stderr)
        for ctype, count in sorted(stats["classification_counts"].items()):
            print(f"   {ctype}: {count:,}", file=sys.stderr)

    if stats["targetname_counts"]:
        print("\n👤 Target Names (Entity Resolution):", file=sys.stderr)
        for tname, count in sorted(stats["targetname_counts"].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {tname}: {count:,} sessions", file=sys.stderr)
        if len(stats["targetname_counts"]) > 5:
            print(f"   ... and {len(stats['targetname_counts']) - 5} more unique targets", file=sys.stderr)

    if stats["involvement_stats"]["total"] > 0:
        print("\n🔗 Involvement Statistics (for Entity Resolution):", file=sys.stderr)
        inv = stats["involvement_stats"]
        print(f"   Total involvements: {inv['total']:,}", file=sys.stderr)
        print(
            f"   With phone (msisdn): {inv['with_msisdn']:,} ({inv['with_msisdn'] / inv['total'] * 100:.1f}%)",
            file=sys.stderr,
        )
        print(f"   With email: {inv['with_email']:,} ({inv['with_email'] / inv['total'] * 100:.1f}%)", file=sys.stderr)
        print(f"   With IMEI: {inv['with_imei']:,} ({inv['with_imei'] / inv['total'] * 100:.1f}%)", file=sys.stderr)
        print(
            f"   With person name: {inv['with_personname']:,} ({inv['with_personname'] / inv['total'] * 100:.1f}%)",
            file=sys.stderr,
        )


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          # Extract default fields to file
          %(prog)s sessions.ndjson -o sessions-core.json
          
          # Extract to stdout (for piping)
          %(prog)s sessions.ndjson | import-sessions.py --stdin
          
          # Add extra fields
          %(prog)s sessions.ndjson --add fulltext,previewcontent -o full.json
          
          # Remove fields from default set
          %(prog)s sessions.ndjson --remove targetname,sourceid -o minimal.json
          
          # Discover available fields
          %(prog)s sessions.ndjson --list-fields
          
          # Create AI-friendly export (size limited)
          %(prog)s sessions.ndjson --add fulltext --max-size 10 -o ai-data.json
          
          # Just show statistics
          %(prog)s sessions.ndjson --stats-only
          
          # Preview what would be extracted (dry run)
          %(prog)s sessions.ndjson --dry-run
          
          # Dry run with more samples
          %(prog)s sessions.ndjson --dry-run --sample 10
        """),
    )

    parser.add_argument("input", type=Path, help="Input NDJSON file")

    parser.add_argument("-o", "--output", type=Path, help="Output file (default: stdout)")

    parser.add_argument("--add", help="Comma-separated fields to add to default set")

    parser.add_argument("--remove", help="Comma-separated fields to remove from default set")

    parser.add_argument("--only", help="Comma-separated fields to extract (ignores defaults)")

    parser.add_argument("--list-fields", action="store_true", help="List all available fields and exit")

    parser.add_argument("--show-defaults", action="store_true", help="Show default field set and exit")

    parser.add_argument("--stats-only", action="store_true", help="Show statistics without extracting data")

    parser.add_argument("--max-size", type=float, help="Maximum output size in MB")

    parser.add_argument("--compact", action="store_true", help="Compact JSON output (no pretty printing)")

    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted without writing output")

    parser.add_argument(
        "--sample", type=int, default=5, help="Number of sample records to show in dry-run (default: 5)"
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress messages")

    args = parser.parse_args()

    # Validate input file
    if not args.input.exists():
        print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Show default fields
    if args.show_defaults:
        print("📋 Default Fields:", file=sys.stderr)
        for field in sorted(DEFAULT_FIELDS):
            print(f"   - {field}", file=sys.stderr)
        print("\n📦 Large Fields (not included by default):", file=sys.stderr)
        for field in sorted(LARGE_FIELDS):
            print(f"   - {field}", file=sys.stderr)
        sys.exit(0)

    # Discover fields
    if args.list_fields:
        if not args.quiet:
            print("🔍 Discovering fields...", file=sys.stderr)

        field_counts = discover_fields(args.input, sample_size=1000)

        print(f"\n📋 Found {len(field_counts)} unique fields:", file=sys.stderr)
        for field, count in sorted(field_counts.items()):
            marker = "📦" if field in LARGE_FIELDS else "✅" if field in DEFAULT_FIELDS else "  "
            print(f"   {marker} {field} ({count} occurrences)", file=sys.stderr)

        sys.exit(0)

    # Determine field set
    if args.only:
        fields = set(args.only.split(","))
    else:
        fields = DEFAULT_FIELDS.copy()

        if args.add:
            fields.update(args.add.split(","))

        if args.remove:
            fields.difference_update(args.remove.split(","))

    if not args.quiet:
        print(f"📋 Extracting {len(fields)} fields: {', '.join(sorted(fields))}", file=sys.stderr)

    # Dry run mode - show what would be extracted
    if args.dry_run:
        if not args.quiet:
            print("\n🔍 DRY RUN - Preview of extraction:", file=sys.stderr)

        # Get diverse samples across session types to avoid bias
        sample_records = []
        session_type_samples = {}

        with open(args.input) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    session_type = record.get("sessiontype", "Unknown")

                    # Collect diverse samples across session types
                    if len(session_type_samples.get(session_type, [])) < 2:  # Max 2 per type
                        extracted = {field: record[field] for field in fields if field in record}
                        if extracted:
                            if session_type not in session_type_samples:
                                session_type_samples[session_type] = []
                            session_type_samples[session_type].append(extracted)
                            sample_records.append(extracted)

                            if len(sample_records) >= args.sample:
                                break
                except:
                    continue

        if sample_records:
            print(f"\n📝 Sample extracted records ({len(sample_records)} of {args.sample}):", file=sys.stderr)
            for i, record in enumerate(sample_records[:3]):  # Show max 3 samples
                print(f"\n--- Record {i + 1} ---", file=sys.stderr)
                for key, value in sorted(record.items()):
                    if isinstance(value, str) and len(value) > 100:
                        print(f"   {key}: {value[:100]}... ({len(value)} chars)", file=sys.stderr)
                    else:
                        print(f"   {key}: {value}", file=sys.stderr)

            # Show field coverage across session types
            all_fields_found = set()
            field_by_type = {}

            for record in sample_records:
                all_fields_found.update(record.keys())
                # Track which session types have which fields
                record_type = record.get("sessiontype", "Unknown")
                if record_type not in field_by_type:
                    field_by_type[record_type] = set()
                field_by_type[record_type].update(record.keys())

            print("\n📊 Field Coverage Analysis:", file=sys.stderr)
            print(f"   Requested fields: {len(fields)}", file=sys.stderr)
            print(f"   Found in samples: {len(all_fields_found)}", file=sys.stderr)
            print(f"   Session types sampled: {', '.join(field_by_type.keys())}", file=sys.stderr)

            missing_fields = fields - all_fields_found
            if missing_fields:
                # Check if missing fields might exist in other session types
                print(f"   📋 Missing from samples: {', '.join(sorted(missing_fields))}", file=sys.stderr)
                print("   💡 Note: Fields may exist in other session types not sampled", file=sys.stderr)

            # Estimate output size
            sample_size = get_json_size_mb(sample_records)
            estimated_full_size = sample_size * (265 / len(sample_records)) if sample_records else 0
            print(f"   📦 Estimated output size: {estimated_full_size:.1f} MB", file=sys.stderr)

        else:
            print("❌ No records found matching field criteria", file=sys.stderr)

        print("\n✅ DRY RUN complete. Use without --dry-run to extract data.", file=sys.stderr)
        sys.exit(0)

    # Extract sessions
    if not args.stats_only:
        stats = extract_sessions(args.input, args.output, fields, max_size_mb=args.max_size, pretty=not args.compact)
    else:
        # Just collect stats without extraction
        stats = {
            "total_records": 0,
            "extracted_records": 0,
            "skipped_records": 0,
            "output_size_mb": 0,
            "sessiontype_counts": {},
            "classification_counts": {},
            "targetname_counts": {},
            "involvement_stats": {
                "total": 0,
                "with_msisdn": 0,
                "with_email": 0,
                "with_imei": 0,
                "with_personname": 0,
            },
        }
        with open(args.input) as f:
            for line in f:
                stats["total_records"] += 1
                try:
                    record = json.loads(line.strip())
                    if "sessiontype" in record:
                        stype = record["sessiontype"]
                        stats["sessiontype_counts"][stype] = stats["sessiontype_counts"].get(stype, 0) + 1
                    if "classification" in record:
                        ctype = record["classification"]
                        stats["classification_counts"][ctype] = stats["classification_counts"].get(ctype, 0) + 1
                    if "targetname" in record:
                        tname = record["targetname"]
                        stats["targetname_counts"][tname] = stats["targetname_counts"].get(tname, 0) + 1
                    if "involvements" in record:
                        for inv in record["involvements"]:
                            stats["involvement_stats"]["total"] += 1
                            if inv.get("msisdn"):
                                stats["involvement_stats"]["with_msisdn"] += 1
                            if inv.get("email"):
                                stats["involvement_stats"]["with_email"] += 1
                            if inv.get("imei"):
                                stats["involvement_stats"]["with_imei"] += 1
                            if inv.get("personname"):
                                stats["involvement_stats"]["with_personname"] += 1
                except:
                    stats["skipped_records"] += 1

    # Print statistics
    if not args.quiet:
        print_stats(stats)


if __name__ == "__main__":
    main()
