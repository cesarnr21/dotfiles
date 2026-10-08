"""
Only touches hosts actually running systemd-resolved (e.g. Ubuntu, Fedora);
leaves NetworkManager-only hosts (e.g. stock Debian) alone, since
"""
from . import TEMPLATE_DIRECTORY

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.systemd import SystemdStatus
from pyinfra.operations import files, systemd


@deploy("DNS (systemd-resolved only)")
def dns():
    status = host.get_fact(SystemdStatus, services=["systemd-resolved.service"])
    uses_systemd_resolved = status.get("systemd-resolved.service", False)

    if not uses_systemd_resolved:
        host.noop(
            "systemd-resolved is not running on this host (e.g. stock Debian "
            "using NetworkManager for DNS). Nothing to do here - configure "
            "DNS via NetworkManager instead if needed."
        )
        return

    resolved_conf = files.template(
        name="Template /etc/systemd/resolved.conf",
        src= str(TEMPLATE_DIRECTORY / "templates/resolved.conf.j2"),
        dest="/etc/systemd/resolved.conf",
        mode="644",
        dns_server=host.data.dns_server,
        dns_domains=host.data.dns_domains,
    )

    resolv_conf_link = files.link(
        name="Point /etc/resolv.conf at the systemd-resolved uplink stub",
        path="/etc/resolv.conf",
        target="/run/systemd/resolve/resolv.conf",
        force=True,
    )

    if resolved_conf.changed or resolv_conf_link.changed:
        systemd.service(
            name="Restart systemd-resolved",
            service="systemd-resolved",
            restarted=True,
        )
