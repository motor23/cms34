import sys, os, logging.config

def add_paths(paths):
    for path in paths:
        if path not in sys.path:
            sys.path.insert(0, path)


def manage(modules, paths=[]):
    add_paths(paths)
    from iktomi.cli import manage
    commands = {}
    for module in modules:
        m = __import__(module)
        commands.update(m.Application.cli_dict)
    manage(commands)
