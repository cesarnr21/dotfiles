"""Installs Miniforge3, runs conda init for bash and fish"""

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.files import File
from pyinfra.facts.server import Arch, Kernel
from pyinfra.operations import files, server


@deploy("Miniforge / conda")
def miniforge():
    install_dir = host.data.miniforge_install_dir
    conda_bin = f"{install_dir}/bin/conda"

    already_installed = host.get_fact(File, path=conda_bin) is not None

    if not already_installed:
        kernel = host.get_fact(Kernel)  # e.g. "Linux"
        arch = host.get_fact(Arch)  # e.g. "x86_64", "aarch64"

        files.download(
            name="Download the Miniforge installer",
            src=f"https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-{kernel}-{arch}.sh",
            dest="/tmp/miniforge-installer.sh",
            mode="755",
        )

        server.shell(
            name="Run the Miniforge installer (batch mode, non-interactive)",
            commands=[f"bash /tmp/miniforge-installer.sh -b -p {install_dir}"],
            _su_user=host.data.target_user,
            _sudo=True
        )

    server.shell(
        name="Initialize conda for bash (required before `conda init fish` works)",
        commands=[f"{conda_bin} init bash"],
        _su_user=host.data.target_user,
        _sudo=True
    )

    server.shell(
        name="Initialize conda for fish",
        commands=[f'bash -c "{conda_bin} init fish"'],
        _su_user=host.data.target_user,
        _sudo=True
    )

    files.file(
        name="Clean up the installer script",
        path="/tmp/miniforge-installer.sh",
        present=False,
    )
