from __future__ import annotations
from abc import abstractmethod
from typing import List
from threading import *

from src.Services.ConnectionManager import ConnectionManager


class IServiceFactory(object):
  @abstractmethod
  def createService(self):
    raise NotImplementedError("MUST be implemented")


class ConnectionManagerFactory(IServiceFactory):
  __instances: List[ConnectionManager] = list()
  
  @classmethod
  def createService(self, host_ip, host_port):
    for instance in cls.__instances:
      if getattr(instance, '_ConnectionManager__host_ip') == host_ip and
        getattr(instance, '_ConnectionManager__host_port') == host_port:
        return instance
    instance = ConnectionManager(host_ip, host_port)
    Thread(target=instance.run, daemon=True).start()
    cls.__instances.append(instance)
    return instance
