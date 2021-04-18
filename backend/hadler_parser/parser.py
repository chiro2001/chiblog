from utils.logger import logger
from flask import Flask

import inspect
import re


def test(tid: int) -> int:
    """
    :param:
    :return:
    """
    return tid + 1


class TestClass:
    def test_func(self, my_id: int = 0) -> int:
        """
        测试函数
        :param my_id: 测试id
        :return:
        """
        return my_id * 2

    @staticmethod
    def test_func_static(text: str, my_id: int = 0) -> int:
        """
        测试static函数
        :param text: 测试参数1
        :param my_id: 测试参数2
        :return: 测试返回值
        """
        return my_id * 2 + int(text)


class WrapperInfo:
    class Return:
        def __init__(self, rtype=None, description: str = None):
            self.type, self.description = rtype, description

        def __str__(self):
            return str(self.__dict__)

    class Arg:
        def __init__(self, name: str, default_value=None, type_=None, description: str = None):
            self.name, self.type_, self.description, self.default_value = name, type_, description, default_value

        def __str__(self):
            return str(self.__dict__)

    def __init__(self, name: str, args: list = None, types: list = None, return_: Return = None, inner=None):
        self.name, self.args, self.types, self.return_, self.inner = name, args, types, return_, inner
        if self.args is None:
            self.args = []
        if self.types is None:
            self.types = []

    def get_base(self):
        base: WrapperInfo = self.inner
        while type(base) is type(WrapperInfo) and base.inner is not None:
            base = base.inner
        return base

    def __str__(self):
        return self.__class__.__name__ + str(self.to_dict())

    def to_dict(self):
        return {
            'name': self.name,
            'args': [t.__dict__ for t in self.args],
            'types': self.types,
            'return': self.return_.__dict__ if self.return_ is not None else None,
            'inner': self.inner.to_dict() if 'to_dict' in dir(self.inner) else (
                self.inner.__dict__ if self.inner is not None else None)
        }


def parse_wrapper_info(target) -> WrapperInfo:
    args_info = inspect.getfullargspec(target)
    logger.debug('args_info %s' % str(args_info))
    wrapper_info = WrapperInfo(target.__name__)
    if 'return' in args_info.annotations:
        ret = WrapperInfo.Return(rtype=args_info.annotations['return'])
        try:
            ret.description = re.compile(r":return:.*").search(target.__doc__).group()[
                              len(":return:"):].strip()
        except (AttributeError, TypeError):
            pass
        wrapper_info.return_ = ret
    for arg_name in args_info.args:
        arg = WrapperInfo.Arg(arg_name)
        # 拿到类型注释
        re_text = f":param {arg_name}:.*"
        re_start = len(f":param {arg_name}:")
        reg = re.compile(re_text)
        try:
            arg.description = reg.search(target.__doc__).group()[re_start:].strip()
        except (AttributeError, TypeError):
            pass
        wrapper_info.args.append(arg)
    # 找到 type 的值
    if 'mtype' in target.__doc__:
        types = re.compile(r":mtype [^:]*:").findall(target.__doc__)
        types = [line[7:-1] for line in types]
        wrapper_info.types = types
    if args_info.defaults is not None:
        for i in range(len(args_info.defaults)):
            arg_name = args_info.args[i + (len(args_info.args) - len(args_info.defaults))]
            for j in range(len(wrapper_info.args)):
                if wrapper_info.args[j].name == arg_name:
                    wrapper_info.args[j].default_value = args_info.defaults[i]
    for arg_name in args_info.annotations:
        for j in range(len(wrapper_info.args)):
            if wrapper_info.args[j].name == arg_name:
                wrapper_info.args[j].type_ = args_info.annotations[arg_name]
    if '__wrapper_info__' in dir(target):
        wrapper_info.inner = target.__wrapper_info__
    return wrapper_info


app = Flask("test")


def myself(func):
    func_data = parse_wrapper_info(func)
    logger.info('init: myself() %s' % func_data)

    def wrapper(self, *args, **kwargs):
        """
        :mtype wrapper:
        :mtype self_wrapper:
        """
        logger.info('calling: wrapper()')
        return func(self, *args, **kwargs)

    wrapper.__wrapper_info__ = func_data

    return wrapper


def parse_info(func):
    func_data = parse_wrapper_info(func)

    def wrapper(self, *args, **kwargs):
        """
        :mtype wrapper:
        :mtype parse_info_wrapper:
        """
        return func(self, *args, **kwargs)

    wrapper.__wrapper_info__ = func_data

    return wrapper


def parse_router_info(wrapper_info: WrapperInfo):
    route = f"/{wrapper_info.name}"


def use_router(func, url, methods=None):
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'] if methods is None else methods

    def wrapper(self, *args, **kwargs):
        """
        :mtype wrapper:
        :mtype parse_info_wrapper:
        """
        return func(self, *args, **kwargs)

    wrapper_info = parse_wrapper_info(func)
    wrapper.__wrapper_info__ = wrapper_info
    wrapper.__router_info__ = parse_router_info(wrapper_info)

    return wrapper


type2name = {
    int: 'int'
}


class ServerTest:
    def __init__(self):
        self.x = 2

    # @app.route('/')
    @myself
    @parse_info
    def test(self, tid: int) -> dict:
        """
        就是这样desu
        :param tid: 就是那个TID啊懂不懂
        :method GET: 请求数据
        :return: 返回测试的数据啊
        """
        return {
            'x': self.x,
            'tid': tid
        }


if __name__ == '__main__':
    # parse_test(test)
    # tt = TestClass()
    # parse_test(tt.test_func)
    # parse_test(TestClass.test_func_static)
    # parse_test(lambda x: x * 2)
    st = ServerTest()
    # logger.info('st.test()', st.test())
    # parse_data = parse_test(st.test)['warpper_info']
    parse_data = st.test.__wrapper_info__.get_base()
    logger.info(parse_data)
    # app.route(f'/{parse_data["name"]}/<{type2name[parse_data["args"][1]["type"]]}:{parse_data["args"][1]["name"]}>')(
    #     st.test)
    # app.run("0.0.0.0", port=8192, debug=False)
