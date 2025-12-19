import os.path
import platform
import subprocess

import requests
from filelock import FileLock

import settings
from core.logger_handler import get_logger

logger = get_logger()
os_name = platform.system()


def launch_edge_with_cdp() -> None:
    edge_path_mapping = {
        "Windows": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "Linux": r"/usr/bin/microsoft-edge-stable",
    }
    edge_path = edge_path_mapping.get(os_name)
    command = [
        edge_path,
        f"--remote-debugging-port={settings.BROWSER_CDP_PORT}",
        f"--user-data-dir={settings.BROWSER_PROFILE_DIR}",
        "--window-size=800,600",
        "--disable-extensions",
        "--disable-sync",
        "--no-first-run",
        "--disable-infobars",
        "--disable-gpu",
        "--no-session-restore",
        "--disable-session-crashed-bubble",
        "--mute-audio",
        "--disable-background-networking",
        "--no-default-browser-check",
        "--safeBrowse-disable-auto-update",
    ]
    if os_name == "Linux":
        xvfb_command = [
            "xvfb-run",
            "-a",
            "--server-args=-screen 0 800x600x24",
        ]
        command.append("--enable-unsafe-swiftshader")
        xvfb_command.extend(command)
        command = xvfb_command
    subprocess.Popen(command)
    logger.info(f"Edge browser started successfully, running on port {settings.BROWSER_CDP_PORT}")
    return None


def close_all_edge() -> None:
    logger.info("Terminating all Edge processes...")
    command = ["pkill", "msedge"] if os_name == "Linux" else ["taskkill", "/F", "/PID", "msedge.exe"]
    subprocess.run(command, capture_output=True)
    logger.info(f"Successfully terminated all Edge processes on {os_name}")
    return None


def get_edge_cdp_version():
    version_info_url = f"{settings.BROWSER_CDP_HOST}:{settings.BROWSER_CDP_PORT}/json/version"
    try:
        with FileLock(os.path.join(settings.TEMP_DIR, "get_edge_cdp_version.lock")):
            response = requests.get(version_info_url, timeout=2)
            version_info = response.json()
            logger.debug(f"Edge browser CDP version found: {version_info}")
            return version_info
    except requests.exceptions.ConnectionError:
        logger.warning("No available Edge browser found")
        return {}
