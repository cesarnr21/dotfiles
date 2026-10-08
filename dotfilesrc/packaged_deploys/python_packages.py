"""pip-installs numpy/pandas/etc. into the Miniforge base env"""

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import pip


@deploy("Python packages (Miniforge base env)")
def python_packages():
    print(f"target user for pip install: {host.data.target_user}")
    pip.packages(
        name="Install Python packages into the Miniforge base environment",
        packages=host.data.pip_packages,
        pip=f"{host.data.miniforge_install_dir}/bin/pip",
        _sudo=True, # needed since pyinfra is running as sudo, but this will lower permissions to install as regular user
        _su_user=host.data.target_user,
    )
