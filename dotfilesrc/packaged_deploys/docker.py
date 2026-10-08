"""
Installs Docker Engine from the official repo, 
creates the docker group, adds your user to it
"""
from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.server import Arch, LinuxDistribution
from pyinfra.operations import apt, dnf, files, server, systemd

from dotfilesrc.helpers import DOCKER_PACKAGES, is_debian_family, is_fedora_family


@deploy("Docker")
def docker():
    if is_debian_family(host):
        _install_docker_debian()
    elif is_fedora_family(host):
        _install_docker_fedora()

    systemd.service(
        name="Enable and start the docker service",
        service="docker",
        running=True,
        enabled=True,
    )

    server.group(
        name="Create the docker group",
        group="docker",
    )

    added = server.user(
        name=f"Add {host.data.target_user} to the docker group",
        user=host.data.target_user,
        groups=["docker"],
        append=True,
        _sudo=True
    )

    if added.changed:
        host.noop(
            f"{host.data.target_user} was just added to the docker group. "
            "Group membership only takes effect on a new login session - "
            "log out/in (or reboot) before running `docker` without sudo. "
            "`newgrp docker` also works for the current shell."
        )


def _install_docker_debian():
    meta = host.get_fact(LinuxDistribution)
    distro_id = meta["release_meta"].get("ID", "").lower()  # "ubuntu" / "debian"
    codename = meta["release_meta"].get("VERSION_CODENAME", "")

    apt.packages(
        name="Install prerequisites",
        packages=["ca-certificates", "gnupg"],
    )

    files.directory(
        name="Create the apt keyrings directory",
        path="/etc/apt/keyrings",
        mode="755",
    )

    files.download(
        name="Add Docker's GPG key",
        src=f"https://download.docker.com/linux/{distro_id}/gpg",
        dest="/etc/apt/keyrings/docker.asc",
        mode="644",
        _sudo=True,
    )

    arch = host.get_fact(Arch)
    deb_arch = "amd64" if arch == "x86_64" else arch

    apt.repo(
        name="Add the Docker apt repository",
        src=(
            f"deb [arch={deb_arch} signed-by=/etc/apt/keyrings/docker.asc] "
            f"https://download.docker.com/linux/{distro_id} {codename} stable"
        ),
        filename="docker",
        _sudo=True,
    )

    apt.update(name="Update apt cache after adding the Docker repo", _sudo=True,)

    apt.packages(
        name="Install Docker Engine",
        packages=DOCKER_PACKAGES,
        _sudo=True,
    )


def _install_docker_fedora():
    dnf.packages(
        name="Install dnf-plugins-core",
        packages=["dnf-plugins-core"],
        _sudo=True,
    )

    server.shell(
        name="Add the Docker CE repo",
        commands=[
            "dnf config-manager addrepo "
            "--from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo"
        ],
        _sudo=True,
    )

    dnf.packages(
        name="Install Docker Engine",
        packages=DOCKER_PACKAGES,
        _sudo=True,
    )
