import argparse
import asyncio
from lib.authorized_key import GithubAuthorizedKeyFile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "users",
        metavar="username",
        type=str,
        nargs="+",
        help="CSV String: A positional argument in CSV form, listing Github usernames. EXAMPLE: ssh-copy-id-from-github.py -a -f authorized_keys sally,sid,jasper",
    )
    parser.add_argument(
        "-a",
        "--annotate",
        dest="annotate",
        action="store_true",
        help="Boolean: Triggers any discovered metadata to be added as an annotation to the key data",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-O",
        "--to-stdout",
        dest="stdout",
        action="store_true",
        help="Boolean: Triggers results to be sent to standard out ONLY",
    )
    output_group.add_argument(
        "-f", 
        "--file", 
        type=str, 
        default=None, 
        help="String: The FILENAME that stores the results. "
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default=None,
        help="String: The LINUX USER that the ssh-keys gain access",
    )
    parser.set_defaults(stdout=False, annotate=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    ak = GithubAuthorizedKeyFile(
        github_users=args.users,
        annotate=args.annotate,
        user=args.user,
        filename=args.file,
    )
    loop.run_until_complete(ak.collect_keys())

    if args.stdout:
        print(ak.serialize())
    else:
        ak.writefile()
