"""Tools for pretty-printing."""
import textwrap
from typing import Any, List, Tuple

import tabulate

import terra_sdk
import terra_sdk.util.serdes

__all__ = [
    "MAX_ROWHEADER_LEN",
    "MAX_ROWSTRING_LEN",
    "see",
    "pretty_repr",
    "PrettyPrintable",
]

MAX_ROWHEADER_LEN = 28
MAX_ROWSTRING_LEN = 45

# TODO: fix display when inside ipython console
try:
    in_ipython = __IPYTHON__
except NameError:
    in_ipython = False

if in_ipython:
    style = "html"
    sep = "<br/>"
else:
    style = "fancy_grid"
    sep = "\n"


def see(obj):
    print(pretty_repr(obj))


def terminal_title(text):
    return f"[{text}]"


def html_bold(name):
    """Adds boldface if in ipython."""
    if in_ipython:
        return "<b>" + name + "</b>"
    return name


def pretty_repr(obj, path=""):
    if isinstance(obj, list):
        if all(isinstance(x, str) for x in obj):
            return sep.join(textwrap.wrap(", ".join(obj), width=MAX_ROWSTRING_LEN))
        if len(obj) >= 1:
            rst = (
                f"{sep}... +{len(obj)-1} more (see {path.rstrip('[]')})"
                if len(obj) > 1
                else sep + ""
            )
            return pretty_repr(obj[0], path=path) + rst
    if isinstance(obj, dict) and not isinstance(obj, terra_sdk.util.serdes.terra_sdkBox):
        return terra_sdk.util.serdes.terra_sdkBox(obj)._pretty_repr_(path)
    if isinstance(obj, str):
        return sep.join(textwrap.wrap(obj, width=MAX_ROWSTRING_LEN))
    if hasattr(obj, "_pretty_repr_"):
        return obj._pretty_repr_(path)
    else:
        return repr(obj)


class PrettyPrintable:
    """Mixin for pretty-printable classes, includes a default pretty-printer that
    shows a table of attributes and their values.
    """

    def _repr_html_(self) -> str:
        """Table HTML repr() for Jupyter."""
        return self._pretty_repr_()

    @property
    def pretty_data(self) -> List[Tuple[str, Any]]:
        """A list of (name, data) pairs desired for inclusion in the pretty output.
        Override this to use default pretty printer, override `_pretty_repr_` to do otherwise.
        """
        return self.__dict__.items()

    @property
    def pretty_header(self) -> str:
        """A title that will be displayed for the default pretty printer."""
        return self.__class__.__name__

    @property
    def pretty_iterable(self) -> bool:
        """Override if the object is iterable, for the default pretty printer."""
        return False

    def _pretty_output(self, path: str = "") -> List[Tuple[str, str]]:
        """Override this if you want to customize how to render child elements for
        the for the default pretty printer."""
        items = []
        for d in self.pretty_data:
            name, data = d
            revised_name = html_bold(
                name[:12] + "..." + name[-4:] if len(name) > MAX_ROWHEADER_LEN else name
            )
            if (
                isinstance(d[1], list)
                or isinstance(d[1], dict)
                or getattr(d[1], "pretty_iterable", False)
            ):
                if isinstance(d[1], list) or getattr(d[1], "pretty_iterable", False):
                    name = f"{name}[]"
                items.append((revised_name, pretty_repr(data, f"{path}.{name}")))
            else:
                items.append((revised_name, pretty_repr(data, path)))
        return items

    def _pretty_repr_(self, path: str = "") -> str:
        """Default pretty printer which formats items as a table. Override this to
        customize pretty-printing.
        """
        if path == "":  # we are at root
            path = self.__class__.__name__
        if self.pretty_header:
            title = (
                "<b><u>" + self.pretty_header + "</u></b>"
                if in_ipython
                else terminal_title(self.pretty_header)
            )
            header = title + sep
        else:
            header = ""
        return header + tabulate.tabulate(
            self._pretty_output(path), tablefmt=style, disable_numparse=True
        )

    @property
    def _pp(self):
        """Shortcut for seeing pretty-printing output."""
        see(self)
        return None
