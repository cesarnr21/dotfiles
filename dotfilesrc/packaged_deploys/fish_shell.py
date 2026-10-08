"""
Sets fish as the login shell, deploys config.fish
(aliases bat→batcat on Debian/Ubuntu automatically, 
since that's what the package installs it as)
"""

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import files, server

from dotfilesrc.helpers import bat_binary_name
from . import TEMPLATE_DIRECTORY


@deploy("fish shell")
def fish_shell():
    # fish itself is already installed by the packages deploy; this just
    # makes it the login shell and drops in config.fish.
    server.user(
        name=f"Set fish as the default login shell for {host.data.target_user}",
        user=host.data.target_user,
        shell="/usr/bin/fish",
        _sudo=True
    )

    files.directory(
        name="Ensure ~/.config/fish exists",
        path=f"{host.data.user_home}/.config/fish",
        user=host.data.target_user,
        group=host.data.target_user,
    )

    files.template(
        name="Deploy config.fish",
        src=str(TEMPLATE_DIRECTORY / "fish/config.fish"),
        dest=f"{host.data.user_home}/.config/fish/config.fish",
        user=host.data.target_user,
        group=host.data.target_user,
        mode="644",
        editor_binary="/usr/bin/vim",
        bat_binary_name=bat_binary_name(host),
    )
