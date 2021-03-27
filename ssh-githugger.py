import argparse
import asyncio
from lib.authorized_key import GithubAuthorizedKeyFile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_users",
        metavar="source_users",
        type=str,
        nargs="+",
        help="CSV String: A positional argument in CSV form, listing Github usernames. EXAMPLE: ssh-githugger.py sally,sid,jasper",
    )
    parser.add_argument(
        "-a",
        "--annotate",
        dest="annotate",
        action="store_true",
        help="Boolean: Default=True Triggers any discovered metadata to be added as an annotation to the key data",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-O",
        "--to-stdout",
        dest="stdout",
        action="store_true",
        help="Boolean: Default=True Triggers results to be sent to standard out ONLY",
    )
    output_group.add_argument(
        "-f", 
        "--file", 
        type=str, 
        default=None, 
        help="String: The FILENAME that stores the results. "
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default="GITHUB_OAUTH_TOKEN", 
        help="String: Default: GITHUB_OAUTH_TOKEN. The NAME of the OAUTH token."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Boolean: Show HTTP headers and ratelimit information",
    )
    parser.set_defaults(stdout=False, annotate=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    ak = GithubAuthorizedKeyFile(
        github_users=args.source_users,
        annotate=args.annotate,
        verbose=args.verbose,
        filename=args.file,
        token=args.token,
    )
    loop.run_until_complete(ak.collect_keys())

    if args.stdout:
        print(ak.serialize())
    else:
        ak.writefile()
