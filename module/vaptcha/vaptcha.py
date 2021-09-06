# -*- encoding=utf8 -*-
import random
import string
import time

from module.aes import aes
from module.config.config import config
from module.cookie import get_cookie, set_cookie
from module.logger import logger

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *


def vaptcha(timeout=60):
    with use_scope("validating"):
        validate_key = ''.join(random.sample(string.ascii_lowercase + string.digits, 4))
        set_cookie("validate", aes.encrypt(validate_key), timeout + 30)
        text = output("请在 {0} 秒内完成验证. ".format(timeout))
        load = output(put_loading(color="primary"))
        put_row([text, load], size='auto 1fr')
        put_text("如果没有自动弹出验证窗口请手动点击按钮")
        put_buttons(["进行验证"], onclick=[_validate])
        _validate()
        start_time = time.time()
        time.sleep(3)
        while True:
            key = get_cookie("validated")
            if key:
                validated_key = aes.decrypt(key)
                if validated_key == validate_key + "/pass":
                    clear()
                    set_cookie("validated")
                    return True
                else:
                    put_error("验证失败：{0}，请重试。".format(validated_key.split("/")[1]), 
                        closable=True)
                    set_cookie("validated")
            else:
                time.sleep(1)
                if time.time() - start_time > timeout:
                    clear()
                    return False

def _validate():
    run_js(r"""
        vaptcha({
            vid: vid,
            type: 'invisible',
            scene: scene,
            area: 'cn'
        }).then(function (vaptchaObj) {
            vobj = vaptchaObj
            vaptchaObj.listen('pass', function () {
                serverToken=vaptchaObj.getServerToken()
                var data = {
                    server: serverToken.server,
                    token: serverToken.token,
                    scene: scene
                }
                $.ajaxSetup({
                    crossDomain: true,
                    xhrFields: {
                        withCredentials: true
                    }
                });
                $.post(server, data)
            })
            vaptchaObj.listen('close', function () {
                vaptchaObj.reset()
            })
            vobj.validate()
        })""",
        vid=config.VID,
        server=config.SERVER,
        scene=config.SCENE)

def init():
    run_js(r"""$('head').append('<script src="https://v-cn.vaptcha.com/v3.js"></script>')""")
