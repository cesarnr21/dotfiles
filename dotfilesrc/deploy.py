import logging
from pyinfra import logger

from pyinfra.context import host

from helpers import require_supported_distro

require_supported_distro(host)

from packaged_deploys.ssh_server import ssh_server
from packaged_deploys.packages import packages
from packaged_deploys.flatpak_apps import flatpak_apps

# fish_shell MUST run before miniforge: it deploys config.fish from a
# template (overwriting the file), and `conda init fish` (in the miniforge
# deploy) appends its hook to that same file afterwards. Running them the
# other way around would wipe out the conda init block.
from packaged_deploys.fish_shell import fish_shell
from packaged_deploys.miniforge import miniforge
from packaged_deploys.python_packages import python_packages
from packaged_deploys.vim_editor import vim_editor
from packaged_deploys.git_config import git_config
from packaged_deploys.dns import dns
from packaged_deploys.docker import docker
from packaged_deploys.xdg_dirs import xdg_dirs



# Control pyinfra's internal log level if needed
logging.getLogger("pyinfra").setLevel(logging.INFO)

# Standard logging handler configuration
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))


# logger.info("running ssh")
# ssh_server()
logger.info("installing packages, message coming from logger")
packages()
# logger.info("installing flatpaks")
# flatpak_apps()
logger.info("installing fish shell")
fish_shell()
logger.info("installing miniforge")
miniforge()
logger.info("installing python packages")
python_packages()
logger.info("set up vim editor")
vim_editor()
logger.info("set up git")
git_config()
logger.info("set up DNS")
dns()
logger.info("installing docker")
docker()
logger.info("removing default directories")
xdg_dirs()
