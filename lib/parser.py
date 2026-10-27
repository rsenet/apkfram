#!/usr/bin/env python3
import os
import zipfile
import json

# settings.json lives at the project root, next to apkfram.py
SETTINGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings.json")

# Bytes read at a time when scanning an inner file (assembly store, blobs, ...)
SCAN_CHUNK = 1024 * 1024


def rule_matches(rule, zipf, zip_file_list):
    """Tell whether a single detection rule matches the APK

    :param rule: one entry from settings.json ({"file", "framework", "match"?, "pattern"?})
    :param zipf: the opened zipfile.ZipFile
    :param zip_file_list: cached zipf.namelist()
    """
    match = rule.get("match", "exact")
    target = rule["file"]

    # Exact path match (default, backward compatible)
    if match == "exact":
        return target in zip_file_list

    # Substring match on any entry path: ABI-agnostic, survives extra path prefixes
    if match == "contains":
        return any(target in entry for entry in zip_file_list)

    # Content scan: look for a byte pattern inside a packaged file (e.g. the
    # .NET assembly store blob, where individual assemblies are not listed)
    if match == "scan":
        if target not in zip_file_list:
            return False

        needle = rule.get("pattern", target).encode()

        with zipf.open(target) as inner:
            tail = b""
            while True:
                chunk = inner.read(SCAN_CHUNK)
                if not chunk:
                    return False

                if needle in tail + chunk:
                    return True

                # keep an overlap so a needle split across chunks is still found
                tail = chunk[-len(needle):]

    return False


def parse_apk(apk_path):
    """Parse APK to identify the Framework used

    :param apk_path: Full path to the APK
    """
    result = {}

    with open(SETTINGS, "r") as f:
        fram_dict = json.loads(f.read())

    zipf = zipfile.ZipFile(apk_path)
    zip_file_list = zipf.namelist()

    for frame_info in fram_dict:
        framework = frame_info["framework"]

        # Score each framework by its matching signals. A rule may carry a
        # "weight" so a decisive marker outranks ambiguous ones shared by
        # several frameworks (e.g. the .NET assembly store used by both
        # Xamarin and .NET MAUI).
        if rule_matches(frame_info, zipf, zip_file_list):
            result[framework] = result.get(framework, 0) + frame_info.get("weight", 1)

    return result


def get_result(apk_path):
    """Get best result

    :param apk_path: Full path to the APK
    """
    apk_parsed = parse_apk(apk_path)

    if apk_parsed:
        # Highest total weight wins; framework name only breaks ties
        best = max(apk_parsed.items(), key=lambda t: (t[1], t[0]))
        print("[!] %s seems to be the best answer" % best[0])

    else:
        print("[!] No framework detected")
