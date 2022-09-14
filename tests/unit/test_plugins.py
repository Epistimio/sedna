import sedna.plugins
from sedna.core import discover_plugins


def test_plugins():
    plugins = discover_plugins(sedna.plugins)

    assert len(plugins) == 1
