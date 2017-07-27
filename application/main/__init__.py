# coding: utf-8
from flask import Blueprint
from ..models import Permission

main=Blueprint('main',__name__)


@main.app_context_processor
def inject_permission():
    """
    :summary: 把Permission类加入上下文，这样不需要每次都要传一个参数
    :return:
    """
    return dict(Permission=Permission)



#循环导入的解决办法之一，还有在函数中导入，或分拆成不用循环导入的模式
from . import views

