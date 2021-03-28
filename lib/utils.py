from dataclasses import dataclass
from framework.utils import is_empty
from typing import Optional, TypeVar

C = TypeVar("C", bound="EASConfig")


@dataclass(frozen=True)
class EASConfig:
    environment: str
    port: int
    listen_interface: str
    routable_host: str
    public_fqdn: str
    http_scheme: str
    db_path: str
    # Maestro
    stub_maestro: bool = True
    maestro_host: Optional[str] = None
    maestro_port: Optional[str] = None
    maestro_api_key: Optional[str] = None
    # ACI
    stub_aci: bool = True
    aci_routable_host: Optional[str] = None
    aci_port: Optional[str] = None
    # Mail Chimp
    mail_chimp_api_key: Optional[str] = None
    mail_chimp_from_email: Optional[str] = None

    @classmethod
    def from_env(cls, environ) -> C:

        port = int(environ.get("EAS_PORT"))
        assert port is not None, "Provide EAS_PORT"

        listen_interface = environ.get("EAS_LISTEN_INTERFACE")
        assert listen_interface is not None, "Provide EAS_LISTEN_INTERFACE"

        routable_host = environ.get("EAS_ROUTABLE_HOST")
        assert routable_host is not None, "Provide EAS_ROUTABLE_HOST"

        public_fqdn = environ.get("EAS_PUBLIC_FQDN")
        assert public_fqdn is not None, "Provide EAS_PUBLIC_FQDN"

        http_scheme = environ.get("EAS_HTTP_SCHEME")
        assert http_scheme is not None, "Provide EAS_HTTP_SCHEME"

        db_path = environ.get("EAS_DB_PATH")
        assert db_path is not None, "Provide EAS_DB_PATH"

        return cls(
            environment=environment,
            routable_host=routable_host,
            port=port,
            listen_interface=listen_interface,
            public_fqdn=public_fqdn,
            http_scheme=http_scheme,
            db_path=db_path,
            stub_maestro=stub_maestro,
            maestro_host=maestro_host,
            maestro_port=maestro_port,
            maestro_api_key=maestro_api_key,
            stub_aci=stub_aci,
            aci_routable_host=aci_routable_host,
            aci_port=aci_port,
            mail_chimp_api_key=mail_chimp_api_key,
            mail_chimp_from_email=mail_chimp_from_email,
        )

