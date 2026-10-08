"""
Installs & enables sshd, installs your public keys, disables password auth
(only once a key is installed, so you can't lock yourself out)

installs and hardens sshd itself, so the first connection to a brand-new
remote box still needs password auth or a key you've already trusted
- you can't SSH-key your way in before the deploy has run once.
"""
from pyinfra.context import host
from pyinfra.api.deploy import deploy
from pyinfra.operations import apt, dnf, files, server, systemd

from dotfilesrc.helpers import is_debian_family, is_fedora_family, ssh_service_name


@deploy("SSH server")
def ssh_server():
    if is_debian_family(host):
        apt.packages(
            name="Install openssh-server",
            packages=["openssh-server"],
        )
    elif is_fedora_family(host):
        dnf.packages(
            name="Install openssh-server",
            packages=["openssh-server"],
        )

    systemd.service(
        name="Enable and start sshd",
        service=ssh_service_name(host),
        running=True,
        enabled=True,
    )

    server.user(
        name="Install authorized SSH keys",
        user=host.data.target_user,
        home=host.data.user_home,
        public_keys=host.data.ssh_public_keys,
    )

    if host.data.ssh_public_keys:
        sshd_dropin = files.put(
            name="Disable SSH password authentication (a key is installed)",
            src=_password_auth_dropin(),
            dest="/etc/ssh/sshd_config.d/99-disable-password-auth.conf",
            _sudo=True,
            mode="644",
        )
        if sshd_dropin.changed:
            systemd.service(
                name="Restart sshd to apply the password-auth change",
                service=ssh_service_name(host),
                restarted=True,
            )
    else:
        host.noop(
            "No ssh_public_keys configured in group_data/all.py - leaving "
            "password authentication enabled so you don't lock yourself out."
        )


def _password_auth_dropin():
    import io

    return io.StringIO(
        "# Managed by pyinfra - do not edit by hand\n"
        "PasswordAuthentication no\n"
        "KbdInteractiveAuthentication no\n"
        "ChallengeResponseAuthentication no\n"
    )
