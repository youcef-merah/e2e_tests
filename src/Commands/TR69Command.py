from src.Libraries.patterns.patterns import ICommand
from src.Libraries.TR69Manager.TR69Manager import ITR69Manager
from src.Libraries.TR69Manager.TR69Errors import TR69MgrError, ErrorNum

import time

class TR69ReadParameters(ICommand):
  def __init__(self, tr69_mgr: ITR69Manager, param):
    self.__tr69_mgr = tr69_mgr
    self.__param = param

  def execute(self) -> int:
    result = ErrorNum.ERROR_UNEXPECTED
    try:
      result = self.__tr69_mgr.getParameterValue(self.__param)
    except TR69MgrError as exc:
      print(f'errno={exc.value}; reason={exc.msg}')
      result = exc.value
    finally:
      return result


class TR69WriteParameters(ICommand):
  def __init__(self, tr69_mgr: ITR69Manager, param, value):
    self.__tr69_mgr = tr69_mgr
    self.__param = param
    self.__value = value

  def execute(self) -> int:
    result = ErrorNum.ERROR_UNEXPECTED
    try:
      self.__tr69_mgr.setParameterValue(self.__param, self.__value)
      result = 0
    except TR69MgrError as exc:
      print(f'errno={exc.value}; reason={exc.msg}')
      result = exc.value
    finally:
      return result