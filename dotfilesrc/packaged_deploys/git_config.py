"""Sets user.name/email, editor, diff/merge tool, and aliases"""

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import server


@deploy("Git configuration")
def git_config():
    settings = {
        "user.email": host.data.git_user_email,
        "user.name": host.data.git_user_name,
        "core.editor": host.data.git_editor,
        "diff.tool": host.data.git_difftool,
        "merge.tool": host.data.git_mergetool,
        "alias.graph": "-c core.pager='less -SRF' log --oneline --graph --decorate",
    }

    server.shell(
        name="Set global git config values",
        commands=[
            f"git config --global {key} '{value}'" for key, value in settings.items()
        ],
        _su_user=host.data.target_user,
        _sudo=True
    )
