"""KDE system settings in search"""

from pathlib import Path
from typing import List, Dict
import os
import shutil
import subprocess
import sys
import time
import traceback

from albert import Item, QueryHandler, runDetachedProcess, Action

md_iid = "0.5"
md_version = "1.0"
md_name = "KDE System Settings"
md_description = "Search KDE System Settings"
md_url = "https://github.com/albertlauncher/python/"
md_bin_dependencies = "systemsettings"

icon_path = str(Path(__file__).parent / "kde_systemsettings")


class Plugin(QueryHandler):
    def id(self):
        return md_iid

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return ""

    def handleQuery(self, query):
        """Hook that is called by albert with *every new keypress*."""  # noqa
        stripped = query.string.strip().lower()
        results = []

        if stripped:
            matches = get_matching_settings_modules(stripped)
            for name, desc in matches:
                print(name, desc)
                item = Item(
                    id=name,
                    text=f"{desc} - {md_name}",
                    subtext=name,
                    icon=["xdg:preferences-system"],
                    actions=[
                        Action(
                            "run",
                            text=name,
                            callable=lambda: runDetachedProcess(
                                ["systemsettings", name]
                            ),
                        ),
                    ],
                )

                query.add(item)


def get_matching_settings_modules(query):
    cmd = ["systemsettings", "--list"]
    proc = subprocess.run(cmd, capture_output=True, check=False)
    stdout = proc.stdout.decode("utf-8")
    settings_modules = stdout.split("\n")[1:-1]
    matching = []
    for module in settings_modules:
        try:
            name, desc = module.split("-")
        except ValueError:
            continue
        if query in module:
            matching.append([name.strip(), desc.strip()])

    return matching
