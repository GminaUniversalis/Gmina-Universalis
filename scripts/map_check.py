# Map consistency check for Gmina Universalis.
#
# Compares map/definition.csv against the colours actually painted in map/provinces.bmp
# and against the province lists in map/default.map, then reports:
#   - provinces declared in definition.csv with no pixels on the map  (the game logs these)
#   - colours painted on the map that no province declares             (the game logs these too)
#   - duplicate colours, duplicate ids, ids above max_provinces
#
# Usage:
#   python scripts/map_check.py                 report only
#   python scripts/map_check.py --sort          also rewrite definition.csv sorted by province id
#   python scripts/map_check.py --csv out.csv   write the full per-province report to a csv

import argparse
import collections
import os
import re
import struct
import sys

MAP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "map")


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def read_default_map(path):
    """max_provinces plus the province id lists (sea_starts, lakes, ...)."""
    with open(path, "r", encoding="cp1252", errors="replace") as handle:
        text = re.sub(r"#[^\n]*", "", handle.read())
    out = {"max_provinces": None, "lists": {}}
    match = re.search(r"max_provinces\s*=\s*(\d+)", text)
    if match:
        out["max_provinces"] = int(match.group(1))
    for key in ("sea_starts", "lakes", "only_used_for_random", "force_coastal"):
        block = re.search(key + r"\s*=\s*\{([^}]*)\}", text)
        out["lists"][key] = set(int(x) for x in re.findall(r"\d+", block.group(1))) if block else set()
    return out


def read_definitions(path):
    """[(id, (r, g, b), name, line_number, raw_line)] plus the header line."""
    with open(path, "r", encoding="cp1252", errors="replace") as handle:
        lines = handle.read().split("\n")
    header = lines[0] if lines and lines[0].lower().startswith("province") else None
    rows, broken = [], []
    for number, line in enumerate(lines[1:] if header else lines, start=2 if header else 1):
        if not line.strip():
            continue
        parts = line.split(";")
        if len(parts) < 4 or not parts[0].strip().isdigit():
            broken.append((number, line))
            continue
        rgb = tuple(int(parts[i]) if parts[i].strip().isdigit() else -1 for i in (1, 2, 3))
        name = parts[4] if len(parts) > 4 else ""
        rows.append((int(parts[0]), rgb, name, number, line))
    return header, rows, broken


def read_bmp_colours(path):
    """{(r, g, b): pixel_count} for a 24-bit uncompressed bmp."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:2] != b"BM":
        sys.exit("provinces.bmp is not a bitmap")
    offset, width, height, bpp, compression = (
        struct.unpack("<I", blob[10:14])[0],
        struct.unpack("<i", blob[18:22])[0],
        struct.unpack("<i", blob[22:26])[0],
        struct.unpack("<H", blob[28:30])[0],
        struct.unpack("<I", blob[30:34])[0],
    )
    if bpp != 24 or compression != 0:
        sys.exit("expected an uncompressed 24-bit bmp, got bpp=%d compression=%d" % (bpp, compression))
    rows = abs(height)
    stride = (width * 3 + 3) // 4 * 4
    counts = collections.Counter()
    try:
        import numpy
    except ImportError:
        numpy = None
    if numpy is not None:
        pixels = numpy.frombuffer(blob, dtype=numpy.uint8, count=stride * rows, offset=offset)
        pixels = pixels.reshape(rows, stride)[:, : width * 3].reshape(-1, 3).astype(numpy.uint32)
        packed = (pixels[:, 0] << 16) | (pixels[:, 1] << 8) | pixels[:, 2]  # bmp stores bgr
        values, totals = numpy.unique(packed, return_counts=True)
        for value, total in zip(values.tolist(), totals.tolist()):
            counts[(value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF)] = total
    else:
        for row in range(rows):
            start = offset + row * stride
            line = blob[start : start + width * 3]
            for index in range(0, len(line), 3):
                counts[(line[index + 2], line[index + 1], line[index])] += 1
    return counts, width, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", action="store_true", help="rewrite definition.csv sorted by province id")
    parser.add_argument("--csv", help="write the full per-province report to this file")
    args = parser.parse_args()

    definition_path = os.path.join(MAP_DIR, "definition.csv")
    default_map = read_default_map(os.path.join(MAP_DIR, "default.map"))
    header, rows, broken = read_definitions(definition_path)
    colours, width, height = read_bmp_colours(os.path.join(MAP_DIR, "provinces.bmp"))

    sea = default_map["lists"]["sea_starts"]
    lakes = default_map["lists"]["lakes"]
    random_only = default_map["lists"]["only_used_for_random"]
    max_provinces = default_map["max_provinces"]

    by_colour = collections.defaultdict(list)
    by_id = collections.defaultdict(list)
    for province_id, rgb, name, number, _ in rows:
        by_colour[rgb].append((province_id, name))
        by_id[province_id].append((rgb, name, number))

    def kind(province_id):
        if province_id in sea:
            return "sea"
        if province_id in lakes:
            return "lake"
        if province_id in random_only:
            return "random-only"
        return "land"

    missing = [(i, rgb, name, kind(i)) for i, rgb, name, _, _ in rows if rgb not in colours]
    undeclared = [(rgb, count) for rgb, count in colours.items() if rgb not in by_colour]
    duplicate_colours = {rgb: owners for rgb, owners in by_colour.items() if len(owners) > 1}
    duplicate_ids = {i: entries for i, entries in by_id.items() if len(entries) > 1}
    over_max = [i for i, _, _, _, _ in rows if max_provinces and i >= max_provinces]

    print("provinces.bmp      %d x %d, %d distinct colours" % (width, height, len(colours)))
    print("definition.csv     %d provinces declared (max_provinces = %s)" % (len(rows), max_provinces))
    print("default.map        %d sea, %d lakes, %d random-only" % (len(sea), len(lakes), len(random_only)))
    print()

    by_kind = collections.Counter(entry[3] for entry in missing)
    print("declared but not painted: %d  (%s)" % (len(missing), dict(by_kind) or "none"))
    for province_id, rgb, name, category in sorted(missing)[:25]:
        print("    %5d  %-28s rgb%-16s %s" % (province_id, name[:28], str(rgb), category))
    if len(missing) > 25:
        print("    ... and %d more" % (len(missing) - 25))
    print()

    print("painted but not declared: %d" % len(undeclared))
    for rgb, count in sorted(undeclared, key=lambda item: -item[1])[:15]:
        print("    rgb%-16s %d pixels" % (str(rgb), count))
    print()

    print("duplicate colours: %d" % len(duplicate_colours))
    for rgb, owners in list(duplicate_colours.items())[:15]:
        print("    rgb%-16s %s" % (str(rgb), ", ".join("%d (%s)" % (i, n) for i, n in owners)))
    print()

    print("duplicate ids: %d" % len(duplicate_ids))
    for province_id, entries in list(duplicate_ids.items())[:15]:
        print("    %d on lines %s" % (province_id, ", ".join(str(e[2]) for e in entries)))
    print()

    declared_ids = set(by_id)
    gaps = [i for i in range(1, (max_provinces or 0)) if i not in declared_ids]
    print("ids below max_provinces with no definition: %d" % len(gaps))
    if gaps:
        runs, start, previous = [], gaps[0], gaps[0]
        for value in gaps[1:]:
            if value != previous + 1:
                runs.append((start, previous))
                start = value
            previous = value
        runs.append((start, previous))
        print("    ranges: %s" % ", ".join("%d-%d" % r if r[0] != r[1] else str(r[0]) for r in runs[:12]))
        if len(runs) > 12:
            print("    ... and %d more ranges" % (len(runs) - 12))
        print("    the game logs each of these as 'has no pixels in provinces.bmp'")
    print()
    print("ids >= max_provinces: %s" % (sorted(over_max) or "none"))
    print("unparsable lines: %s" % ([number for number, _ in broken] or "none"))

    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as handle:
            handle.write("province;red;green;blue;name;kind;pixels\n")
            for province_id, rgb, name, _, _ in sorted(rows):
                handle.write(
                    "%d;%d;%d;%d;%s;%s;%d\n"
                    % (province_id, rgb[0], rgb[1], rgb[2], name, kind(province_id), colours.get(rgb, 0))
                )
        print("\nwrote %s" % args.csv)

    if args.sort:
        # Byte level on purpose: the file mixes cp1252 and utf-8 rows, so decoding would corrupt names.
        crlf, lf = b"\r\n", b"\n"
        with open(definition_path, "rb") as handle:
            raw_lines = handle.read().replace(crlf, lf).split(lf)
        head = raw_lines[0:1] if header else []
        body = [line for line in raw_lines[len(head):] if line.strip()]

        def sort_key(line):
            field = line.split(b";")[0].strip()
            return (0, int(field)) if field.isdigit() else (1, 0)

        body.sort(key=sort_key)
        with open(definition_path, "wb") as handle:
            handle.write(crlf.join(head + body) + crlf)
        print("\nsorted %s by province id (%d rows)" % (definition_path, len(body)))


if __name__ == "__main__":
    main()
