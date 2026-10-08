"""
Shared helpers for branching on OS family. Unlike a static "vars per distro"
file, these read the actual LinuxDistribution fact from each host, so a
single deploy run against a mixed inventory (some Ubuntu, some Fedora boxes)
does the right thing on each host automatically.
"""

from pyinfra.facts.server import LinuxDistribution
from pyinfra.api.host import Host

def _release_meta(host: Host):
    # return host.get_fact(LinuxDistribution).get("release_meta", {})
    distro_info = host.get_fact(LinuxDistribution) or {}
    return distro_info.get("release_meta", {})

def is_debian_family(host) -> bool:
    meta = _release_meta(host)
    os_id = meta.get("ID", "").lower()
    id_like = meta.get("ID_LIKE", "").lower()
    return os_id == "debian" or "debian" in id_like


def is_fedora_family(host) -> bool:
    meta = _release_meta(host)
    os_id = meta.get("ID", "").lower()
    id_like = meta.get("ID_LIKE", "").lower()
    return os_id == "fedora" or "fedora" in id_like


def require_supported_distro(host: Host):
    if not (is_debian_family(host) or is_fedora_family(host)):
        distro = host.get_fact(LinuxDistribution)
        raise ValueError(
            "This deploy only supports Debian-family (Ubuntu, Debian) and "
            f"Fedora hosts. Detected: {distro.get('name')} on {host.name}."
        )


# ---------------------------------------------------------------------------
# Per-distro values that differ just enough to not be worth a whole separate
# "vars" file each - mirrors the intent of Ansible's vars/Debian.yml /
# vars/RedHat.yml, just resolved live instead of loaded from disk.
# ---------------------------------------------------------------------------

CORE_PACKAGES = {
    "debian": [
        "python3-pip",
        "curl",
        "wget",
        "meld",
        "git",
        "bat",
        "vim",
        "fish",
        "fastfetch",
        "ncdu",
        "cmatrix",
        "autojump",
        "htop",
        "tree",
        "tmux",
        "gparted",
        "ffmpeg",
        "btop",
    ],
    "fedora": [
        "python3-pip",
        "curl",
        "wget",
        "meld",
        "git",
        "bat",
        "vim-enhanced",
        "fish",
        "fastfetch",
        "ncdu",
        "cmatrix",
        "autojump",
        "htop",
        "tree",
        "tmux",
        "gparted",
        "ffmpeg",
        "btop",
    ],
}

DOCKER_PACKAGES = [
    "docker-ce",
    "docker-ce-cli",
    "containerd.io",
    "docker-buildx-plugin",
    "docker-compose-plugin",
]


def ssh_service_name(host) -> str:
    # Debian/Ubuntu ship the systemd unit as "ssh"; Fedora/RHEL as "sshd".
    return "ssh" if is_debian_family(host) else "sshd"


def bat_binary_name(host) -> str:
    # Debian/Ubuntu install the `bat` package's binary as `batcat` to avoid
    # a name clash with another package; Fedora's is just `bat`.
    return "batcat" if is_debian_family(host) else "bat"


def core_packages(host) -> list:
    return CORE_PACKAGES["debian"] if is_debian_family(host) else CORE_PACKAGES["fedora"]
