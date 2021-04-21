#!/usr/bin/env python3
import zipfile
import json

def parse_apk(apk_path):
    """Parse APK to identify the Framework used

    :param apk_path: Full path to the IPA
    """
    result = {}
    parser = open("settings.json", "r").read()
    fram_dict = json.loads(parser)

    zipf = zipfile.ZipFile(apk_path)
    zip_file_list = zipf.namelist()

    for frame_info in fram_dict:
        file, framework = frame_info["file"], frame_info["framework"]

        if file in zip_file_list:
            if framework in result:
                current = result[framework]
                result[framework] = current + 1

            else:
                result[framework] = 1

    return result

def get_result(apk_path):
    """Get best result

    :param apk_path: Full path to the IPA
    """
    apk_parsed = parse_apk(apk_path)

    if apk_parsed:
        new_d = dict(sorted(apk_parsed.items(), key=lambda t: t[0], reverse=True))
        print("[!] %s seems to be the best answer" % next(iter(new_d)))

    else:
        print("[!] No framework detected")
