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
        help="Public key source Github usernames",
    )
    parser.add_argument(
        "-a",
        "--annotate",
        dest="annotate",
        action="store_true",
        help="store public key source details in key annotation",
    )
    parser.add_argument("-m", "--mirror", default="10.10.2.2", help="Use the preconfigured mirror")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-O",
        "--to-stdout",
        dest="stdout",
        action="store_true",
        help="write results to standard output",
    )
    output_group.add_argument(
        "-f", "--file", type=str, default=None, help="store output in FILE"
    )
    output_group.add_argument("-j", "--jsonfile", action="store_true", default=False, help="write results to /home/ubuntu/keyfile.gh")
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default=None,
        help="store output for USER",
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
    if args.mirror:
        host = args.mirror
        port = "23456"
        ssl = False
    else:
        host = "api.github.com"
        ssl = True
        port = ""
    if args.jsonfile:
        with open("/home/ubuntu/github_users.txt") as f:
            txt = f.read().split(' ')
            g_users = [ u.strip() for u in txt]
        ak.github_users = g_users
        loop.run_until_complete(ak.jsonize())
        ak.json_to_file()
    else:
        loop.run_until_complete(ak.collect_keys(host=host, is_ssl=ssl, port=port))
    if args.stdout:
        print(ak.serialize())
    else:
        ak.writefile()
                                      
