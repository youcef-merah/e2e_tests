from __future__ import annotations
from abc import abstractmethod
from src.Libraries.patterns.patterns import IObservable, IObserver
import time

class IService(IObservable):
  def __init__(self):
    super(IObservable, self).__init__()

  def attach(self, observer: IObserver):
    self._observers.append(observer)
    # The service is not necessary launched by the observer itself
    # Then give the current state at subscription
    observer.update(self)

  def detach(self, observer: IObserver):
    self._observers.remove(observer)

  def _notify(self):
    for obs in self._observers:
      obs.update(self)

  @abstractmethod
  def run(self):
    raise NotImplementedError("MUST be implemented")

  @abstractmethod
  def getState(self):
    raise NotImplementedError("MUST be implemented")

  @abstractmethod
  def setState(self):
    raise NotImplementedError("MUST be implemented")

class ServiceSubscriber(IObserver):
  def __init__(self, svc: IService, svc_state):
    self._svc= svc
    self._svc_state = svc_state
    self.__event_catched = 0

  def update(self, svc: IService):
    if svc.getState() == self._svc_state:
      self.__event_catched += 1

  def catchEvent(self, count):
    if count < 0:
      raise ValueError
    
    self._svc.attach(self)
    while self.__event_catched != count:
      time.sleep(1)
    self._svc.detach(self)