"""
apt full-upgrade / dnf update, installs the CLI toolbox 
(curl, wget, meld, bat, htop, tmux, btop, etc.),
enables RPM Fusion on Fedora so ffmpeg is the full build, not ffmpeg-free
"""
from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, dnf

from dotfilesrc.helpers import core_packages, is_debian_family, is_fedora_family

RPMFUSION_FREE_URL_TEMPLATE = (
    "https://download1.rpmfusion.org/free/fedora/"
    "rpmfusion-free-release-{major}.noarch.rpm"
)


@deploy("Core packages")
def packages():
    if is_debian_family(host):
        print(f"running as user {host.data.target_user}")
        apt.update(name="Update apt cache", cache_time=3600,_sudo=True)
        apt.upgrade(name="Full-upgrade apt packages",_sudo=True)
        apt.packages(
            name="Install core packages",
            packages=core_packages(host),
            _sudo=True
        )

    elif is_fedora_family(host):
        dnf.update(name="Upgrade all packages (dnf update -y)")

        major = host.get_fact(LinuxDistribution)["major"]
        dnf.rpm(
            name="Enable RPM Fusion (free) so ffmpeg is the full build",
            src=RPMFUSION_FREE_URL_TEMPLATE.format(major=major),
        )

        dnf.packages(
            name="Install core packages",
            packages=core_packages(host),
        )
