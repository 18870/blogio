# -*- encoding=utf8 -*-
from module.config.config import config

from os import path

# Replace template
from pywebio.platform.utils import _here_dir, _index_page_tpl
_index_page_tpl.__init__(open(path.join(_here_dir, 'tpl', 'index.html'), encoding='utf8').read()
    .replace(
        r'<footer class="footer">',
        r'<!-- <footer class="footer">')
    .replace(
        r"</footer>",
        r"</footer> -->"
    )
)

from pywebio.platform.fastapi import start_server
from module.vaptcha import vaptcha_1

start_server(
    {
        "vaptcha-1": vaptcha_1
    },
    port = 10011,
    debug = True,
)