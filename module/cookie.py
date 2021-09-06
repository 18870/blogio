# -*- encoding=utf8 -*-
from module.config.config import config
from module.logger import logger
from pywebio.session import run_js, eval_js

SETTING = ''
if config.PATH:
    SETTING += f'; path={config.PATH}'
if config.SAMESITE:
    SETTING += f'; SameSite={config.SAMESITE}'
if config.SECURE:
    SETTING += f'; Secure'
if config.DOMAIN:
    SETTING += f'; domain={config.DOMAIN}'

logger.info(f"Cookie settings: {SETTING[2:]}")

def set_cookie(key, value="", expire=-1):
    run_js("setCookie(key, value, sec, setting)", key=key, value=value, sec=expire, setting=SETTING)
def get_cookie(key):
    return eval_js("getCookie(key)", key=key)

def init():
    # Note: I am not sure whether arguments pass to run_js(**args) can used by functions later.
    run_js(r"""
        window.setCookie = function(name,value,sec,setting) {
            var expires = "";
            if (sec) {
                var date = new Date();
                date.setTime(date.getTime() + (sec*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "")  + expires + setting;
        }
        window.getCookie = function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }""")