#!/usr/bin/env python3
import os
import zipfile
import json

# settings.json / tools.json live at the project root, next to apkfram.py
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS = os.path.join(ROOT, "settings.json")
TOOLS = os.path.join(ROOT, "tools.json")

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


def scan_apk(apk_path):
    """Scan an APK and return, per framework, its score and matched signals

    :param apk_path: Full path to the APK
    :return: dict framework -> {"score": int, "signals": [matched files]}
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
            entry = result.setdefault(framework, {"score": 0, "signals": []})
            entry["score"] += frame_info.get("weight", 1)
            entry["signals"].append(frame_info["file"])

    return result


def parse_apk(apk_path):
    """Parse APK to identify the Framework used

    :param apk_path: Full path to the APK
    :return: dict framework -> score
    """
    return {fw: info["score"] for fw, info in scan_apk(apk_path).items()}


def print_tools(framework):
    """Print the tools needed to read the source code of a given framework

    :param framework: the detected framework name
    """
    try:
        with open(TOOLS, "r") as f:
            tools = json.loads(f.read())
    except (OSError, ValueError):
        return

    info = tools.get(framework)
    if not info:
        print("    No tooling reference available for this framework yet")
        return

    if info.get("source"):
        print("[*] Source code location: %s" % info["source"])

    print("[*] Tools to read the source code:")
    for tool in info.get("tools", []):
        print("     - %-22s %s" % (tool["name"], tool.get("ref", "")))


def get_result(apk_path, verbose=False):
    """Get best result

    :param apk_path: Full path to the APK
    :param verbose: also print detected signals and the reversing toolkit
    """
    apk_scan = scan_apk(apk_path)

    if apk_scan:
        # Highest total weight wins; framework name only breaks ties
        best = max(apk_scan.items(), key=lambda t: (t[1]["score"], t[0]))
        framework = best[0]
        print("[!] %s seems to be the best answer" % framework)

        if verbose:
            print("[*] Signals matched: %s" % ", ".join(best[1]["signals"]))
            print_tools(framework)

    else:
        print("[!] No framework detected")

        if verbose:
            print("[*] Likely a native app (Java/Kotlin). Tools: jadx, apktool, Ghidra")
