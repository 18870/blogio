# -*- encoding=utf8 -*-
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

from module.vaptcha.vaptcha import vaptcha as validate
from module.vaptcha.vaptcha import init as init_vaptcha
from module.cookie import init as init_cookie

def vaptcha_1():
    set_env(title="vaptcha-1")
    init_cookie()
    init_vaptcha()

    def func():
        if validate():
            put_success("验证成功", closable=True)
        else:
            put_error("验证失败", closable=True)

    put_buttons(["点我进行验证"], onclick=[func])
    hold()