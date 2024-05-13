""" This is a Firefox cli profile manager.
    Create, clone or remove a profile.
"""

import argparse
import os
from argparse import RawTextHelpFormatter
from pprint import pprint

from geckordp.profile import ProfileManager
from geckordp.settings import GECKORDP


def main():
    env_names = [
        "PROFILE_PATH",
        "FIREFOX_PATH",
    ]
    epilog = """available environment variables:\n\t"""

    parser = argparse.ArgumentParser(
        description="",
        formatter_class=RawTextHelpFormatter,
        epilog=epilog + "\n\t".join(env_names),
    )
    parser.add_argument(
        "-n",
        "--new",
        type=str,
        default="",
        metavar="<profile-name>",
        help="Creates a new firefox profile",
    )
    parser.add_argument(
        "-c",
        "--clone",
        action="append",
        nargs=2,
        metavar=("<source-profile-name>", "<clone-profile-name>"),
        help="Clones an existing profile with a different name",
    )
    parser.add_argument(
        "-rm",
        "--remove",
        type=str,
        default="",
        metavar="<profile-name>",
        help="Removes a profile",
    )
    parser.add_argument("-ls", "--list", action="store_true", help="List all profiles")
    args, _ = parser.parse_known_args()

    env_vars = {}
    for env_name in env_names:
        env_vars[env_name] = os.environ.get(env_name, "")

    GECKORDP.DEBUG = 1
    pm = ProfileManager(env_vars["FIREFOX_PATH"], env_vars["PROFILE_PATH"])

    if args.new != "":
        profile = pm.create(args.new)
        if profile == None:
            return 1
        profile.set_required_configs()
        return 0

    if args.clone != None:
        if not isinstance(args.clone, list):
            print("'--clone' expected 2 strings")
            return 1

        if len(args.clone) != 1:
            print("'--clone' encountered an unknown error")
            return 1

        for n in args.clone[0]:
            if str(n).isdecimal():
                print(f"'--clone' expected a string value not '{n}'")
                return 1

        profile = pm.clone(args.clone[0][0], args.clone[0][1])
        if profile == None:
            print(f"cloning profile failed")
            return 1

        profile.set_required_configs()
        return 0

    if args.remove != "":
        if pm.remove(args.remove):
            return 0
        return 1

    if args.list is True:
        pprint(pm.list_profiles())
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    main()
