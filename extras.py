import sys

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.widgets
import StetsonHomeAutomation.plugins
import importlib
import pkgutil
from kivy.uix.accordion import AccordionItem


def iterNamespace(pkgNs):
    return pkgutil.iter_modules(pkgNs.__path__, pkgNs.__name__ + ".")


allPlugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iterNamespace(StetsonHomeAutomation.plugins)
}

print(allPlugins)


class ExtrasPanel(StetsonHomeAutomation.widgets.AccordionWithBg):
    def __init__(self, caller, **kwargs):
        super(ExtrasPanel, self).__init__(**kwargs)
        self.orientation = "vertical"
        for plugin in allPlugins:
            wid = allPlugins[plugin].MainWidget()
            item = AccordionItem(title=wid.title)
            item.add_widget(wid)
            self.add_widget(item)


