# -*- encoding=utf8 -*-
from os import path

from module.config.config import config
from pywebio.platform.page import _here_dir, _index_page_tpl
from pywebio.platform.fastapi import start_server

# Replace template
_index_page_tpl.__init__(open(path.join(_here_dir, 'tpl', 'index.html'), encoding='utf8').read()
    .replace(
        r'<footer class="footer">',
        r'<!-- <footer class="footer">')
    .replace(
        r"</footer>",
        r"</footer> -->"
    )
)


from module.vaptcha import vaptcha_1

start_server(
    {
        "vaptcha-1": vaptcha_1
    },
    port = config.PORT,
    debug = config.DEBUG,
)