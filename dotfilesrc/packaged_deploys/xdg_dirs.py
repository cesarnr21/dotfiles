"""
Keeps only a lowercase ~/downloads, 
removes the other default folders if they're empty 
(never touches ones with files in them)
"""

from pathlib import Path

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.files import Directory
from pyinfra.operations import files, server

from . import TEMPLATE_DIRECTORY

DEFAULT_XDG_DIRS = ["Desktop", "Documents", "Music", "Pictures", "Public", "Templates", "Videos"]


@deploy("xdg-user-dirs (keep only downloads)")
def xdg_dirs():
    keep_only_download = host.data.xdg_keep_only_download
    download_name = host.data.xdg_download_dirname
    home = host.data.user_home

    if keep_only_download:
        files.template(
            _sudo=True,
            name="Template /etc/xdg/user-dirs.defaults (system-wide)",
            src=str(TEMPLATE_DIRECTORY / "templates/user-dirs.defaults.j2"),
            dest="/etc/xdg/user-dirs.defaults",
            mode="644",
            xdg_download_dirname=download_name,
        )

        files.directory(
            _sudo=True,
            name="Ensure ~/.config exists",
            path=f"{home}/.config",
            user=host.data.target_user,
            group=host.data.target_user,
        )

        files.template(
            _sudo=True,
            name="Template ~/.config/user-dirs.dirs (per-user override)",
            src=str(TEMPLATE_DIRECTORY / "templates/user-dirs.dirs.j2"),
            dest=f"{home}/.config/user-dirs.dirs",
            user=host.data.target_user,
            group=host.data.target_user,
            mode="644",
            xdg_download_dirname=download_name,
        )

    if download_name != "Downloads":
        server.shell(
            name=f"Rename ~/Downloads to ~/{download_name} if needed",
            commands=[
                f"test -d {home}/Downloads && ! test -e {home}/{download_name} "
                f"&& mv {home}/Downloads {home}/{download_name} || true"
            ],
        )

    if host.data.xdg_remove_empty_default_dirs:
        for dirname in DEFAULT_XDG_DIRS:
            path = f"{home}/{dirname}"
            if host.get_fact(Directory, path=path) is not None:
                # rmdir only succeeds on empty directories - anything with
                # files in it is silently left alone via `|| true`.
                server.shell(
                    name=f"Remove {dirname} if it's empty",
                    commands=[f"rmdir {path} 2>/dev/null || true"],
                )

    server.shell(
        name="Re-sync xdg user dirs",
        commands=["xdg-user-dirs-update"],
        _su_user=host.data.target_user,
        _sudo=True
    )
