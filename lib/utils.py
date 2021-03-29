from dataclasses import dataclass
from framework.utils import is_empty
from typing import Optional, TypeVar

C = TypeVar("C", bound="EASConfig")


@dataclass(frozen=True)
class SSHGHConfig:
    source_user: str
    annotate: str
    stdout: str
    file: str
    token: str
    verbose: str


    @classmethod
    def from_env(envs, environ) -> envs:

        source_user = environ.get("GHUGGER_SOURCE_USER")
        annotate = environ.get("GHUGGER_ANNOTATE")
        stdout = environ.get("GHUGGER_STDOUT")
        file = environ.get("GHUGGER_FILE")
        token = int(environ.get("GHUGGER_TOKEN"))
        verbose = int(environ.get("GHUGGER_VERBOSE"))

        return envs(
            ghugger_source_user=ghugger_source_user,
            ghugger_annotate=ghugger_annotate,
            ghugger_stdout,ghugger_stdout,
            ghugger_file=ghugger_file,
            ghugger_token=ghugger_token,
            ghugger_verbose,ghugger_verbose,
        )
