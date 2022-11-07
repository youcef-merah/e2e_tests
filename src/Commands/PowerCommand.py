from src.Libraries.patterns.patterns import ICommand
from src.Libraries.PowerController.PowerController import IPowerController
from src.Libraries.PowerController.PowerCtrlErrors import ErrorNum

import time

class PowerRestart(ICommand):
  def __init__(self, power_ctrl: IPowerController):
    self.__power_ctrl = power_ctrl
    
  def execute(self) -> int:
    result = ErrorNum.ERROR_UNEXPECTED
    try:
      self.__power_ctrl.powerOff()
      time.sleep(1)
      self.__power_ctrl.powerOn()
      result = 0
    except PowerCtrlError as exc:
      print(f'errno={exc.value}; reason={exc.msg}')
      result = exc.value
    finally:
      return result