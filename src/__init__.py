import os
from typing import Any, List, Tuple

from aqt import gui_hooks, mw
from aqt.webview import WebContent
from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import qtMenuShortcutWorkaround


addon_dir = os.path.dirname(__file__)
config = mw.addonManager.getConfig(__name__)
config_defaults = mw.addonManager.addonConfigDefaults(__name__)
mw.addonManager.setWebExports(__name__, r".*\.js")


def load_web(webcontent: WebContent, context: Any):
    if isinstance(context, Editor):
        addon_package = mw.addonManager.addonFromModule(__name__)
        base_path = f"/_addons/{addon_package}/"
        webcontent.js.append(f"{base_path}/bidi.js")


def wrap_block_in_dir(editor: Editor, direction: str) -> None:
    editor.web.eval(f'BidiToolsSetBlockDir("{direction}");')

def wrap_inline_in_dir(editor: Editor, direction: str) -> None:
    editor.web.eval(f'BidiToolsSetInlineDir("{direction}");')

def ltr_block_action(editor: Editor):
    wrap_block_in_dir(editor, "ltr")

def rtl_block_action(editor: Editor):
    wrap_block_in_dir(editor, "rtl")

def ltr_inline_action(editor: Editor):
    wrap_inline_in_dir(editor, "ltr")

def rtl_inline_action(editor: Editor):
    wrap_inline_in_dir(editor, "rtl")


chars = (
    ("Left-to-Right Mark (LRM)", "\u200e"),
    ("Right-to-Left Mark (RLM)", "\u200f"),
    ("Left-to-Right Embedding (LRE)", "\u202a"),
    ("Right-to-Left Embedding (RLE)", "\u202b"),
    ("Left-to-Right Override (LRO)", "\u202d"),
    ("Right-to-Left Override (RLO)", "\u202e"),
    ("Pop Directional Format (PDF)", "\u202c"),
    ("Arabic Letter Mark (ALM)", "\u061c"),
    ("Left-to-Right Isolate (LRI)", "\u2066"),
    ("Right-to-Left Isolate (RLI)", "\u2067"),
    ("First Strong Isolate (FSI)", "\u2068"),
    ("Pop Directional Isolate (PDI)", "\u2069"),
)

def insert_char(editor: Editor, char: str):
    editor.web.eval(f"document.execCommand('inserttext', false, '{char}');")


def create_insert_menu(editor: Editor) -> QMenu:
    m = QMenu(editor.mw)
    for name, char in chars:
        a = m.addAction(name)
        qconnect(a.triggered, lambda t, char=char: insert_char(editor, char))
    m.setTitle("Insert Characters")

    return m


actions = (
    ("Left-To-Right", ltr_block_action, config.get("ltr_block_shortcut", config_defaults["ltr_block_shortcut"])),
    ("Right-To-Left", rtl_block_action, config.get("rtl_block_shortcut", config_defaults["rtl_block_shortcut"])),
    ("LTR inline", ltr_inline_action, config.get("ltr_inline_shortcut", config_defaults["ltr_inline_shortcut"])),
    ("RTL inline", rtl_inline_action, config.get("rtl_inline_shortcut", config_defaults["rtl_inline_shortcut"])),
)

editor_button_labels = ("ltr", "rtl")

def on_button_click(editor: Editor):
    m = QMenu(editor.mw)
    for text, handler, shortcut in actions[2:]:
        a = m.addAction(text)
        qconnect(a.triggered, lambda t, cb=handler: cb(editor))
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))

    m.addMenu(create_insert_menu(editor))
    qtMenuShortcutWorkaround(m)
    m.exec(QCursor.pos())


def add_editor_button(buttons: List[str], editor: Editor) -> None:
    for i, (text, handler, shortcut) in enumerate(actions[0:2]):
        label = editor_button_labels[i]
        btn = editor.addButton(
            icon=os.path.join(addon_dir, f"icons/{label}.svg"),
            cmd=f"bidi_tools_{label}",
            tip=f"{text} ({shortcut})",
            func=handler,
            keys=shortcut,
        )
        buttons.append(btn)

    button = editor.addButton(
        icon=os.path.join(addon_dir, "icons/icon.svg"),
        cmd="bidi_tools",
        tip="Bidirectional Text Tools",
        func=on_button_click
    )
    buttons.append(button)


def add_shortcuts(shortcuts: List[Tuple], editor: Editor) -> None:
    for text, handler, shortcut in actions[2:]:
        if shortcut:
            shortcuts.append((shortcut, lambda cb=handler: cb(editor)))


gui_hooks.editor_did_init_buttons.append(add_editor_button)
gui_hooks.editor_did_init_shortcuts.append(add_shortcuts)
gui_hooks.webview_will_set_content.append(load_web)
