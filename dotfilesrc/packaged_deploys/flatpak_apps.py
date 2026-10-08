"""Installs flatpak, adds Flathub, installs your app list"""

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import apt, dnf, server
from pyinfra.operations import flatpak as flatpak_ops

from dotfilesrc.helpers import is_debian_family, is_fedora_family


@deploy("Flatpak")
def flatpak_apps():
    if is_debian_family(host):
        apt.packages(
            name="Install flatpak",
            packages=["flatpak", "gnome-software-plugin-flatpak"],
        )
    elif is_fedora_family(host):
        # Fedora ships flatpak by default, but make sure.
        dnf.packages(
            name="Install flatpak",
            packages=["flatpak"],
            # _su_user=host.data.target_user,
            _sudo=True
        )

    if host.data.flatpak_add_flathub:
        server.shell(
            name="Add the Flathub remote",
            commands=[
                "flatpak remote-add --if-not-exists flathub "
                "https://dl.flathub.org/repo/flathub.flatpakrepo"
            ],
        )

    if host.data.flatpak_apps:
        flatpak_ops.packages(
            name="Install flatpak applications",
            packages=host.data.flatpak_apps,
            remote="flathub" if host.data.flatpak_add_flathub else None,
        )
