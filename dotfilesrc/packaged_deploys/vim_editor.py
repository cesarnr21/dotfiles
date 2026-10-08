"""
`update-alternatives --set editor` only applies on Debian/Ubuntu;
Fedora doesn't use the alternatives system for editor the same way, so
vim is just installed and left as-is there.
"""
from pathlib import Path

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import files, server

from dotfilesrc.helpers import is_debian_family
from . import TEMPLATE_DIRECTORY


@deploy("vim")
def vim_editor():
    if is_debian_family(host):
        # update-alternatives --set is idempotent, so this is safe to run
        # every time; it's a no-op if vim.basic isn't a registered
        # alternative (e.g. vim isn't installed) or is already selected.
        server.shell(
            name="Select vim as the default editor, if available",
            commands=[
                "update-alternatives --list editor 2>/dev/null | grep -m1 vim.basic "
                "| xargs -r update-alternatives --set editor"
            ],
            _sudo=True
        )

    files.template(
        name="Deploy ~/.vimrc",
        src=str(TEMPLATE_DIRECTORY / "vim/vimrc.lua"),
        dest=f"{host.data.user_home}/.vimrc",
        user=host.data.target_user,
        group=host.data.target_user,
        mode="644",
    )
