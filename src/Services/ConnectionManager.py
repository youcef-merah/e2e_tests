from __future__ import annotations
from abc import abstractmethod
import os, time

import src.Services.Service as IService
from src.Libraries.patterns.patterns import Singleton
from src.Services.Service import IService

class ConnectionManager(IService):

  def __init__(self, host_ip='192.168.0.1', host_port=80):
    super(IService, self).__init__()
    self.__state: ConnectionState = ConnectionClosed()
    self.__host_ip = host_ip
    self.__host_port = host_port

  @property
  def host_ip(self):
    return self.__host_ip

  @property
  def host_port(self):
    return self.__host_port

  def getState(self):
    return self.__state

  def setState(self, state):
    self.__state = state
    self._notify()

  def establishConnection(self):
    self.getState().establishConnection(self)

  def inspectConnection(self):
    self.getState().inspectConnection(self)

  def run(self):
    while True:
      time.sleep(1)
      if self.getState() == ConnectionClosed():
        self.establishConnection()
      else:
        self.inspectConnection()

class ConnectionState():
  @abstractmethod
  def establishConnection(self, cm: ConnectionManager):
    raise NotImplementedError("MUST be implemented")

  @abstractmethod
  def inspectConnection(self, cm: ConnectionManager):
    raise NotImplementedError("MUST be implemented")

class ConnectionOpened(ConnectionState, Singleton):

  def __init__(self):
    super(Singleton, self).__init__()

  def __str__(self):
    return 'connection established'

  def inspectConnection(self, cm: ConnectionManager):
    command = ['ping -c 1', cm.host_ip]
    if  os.system(f'ping -c 1 {cm.host_ip} > /dev/null ') != 0:
      cm.setState(ConnectionClosed())


class ConnectionClosed(ConnectionState, Singleton):

  def __init__(self):
    super(ConnectionState, self).__init__()
    super(Singleton, self).__init__()

  def __str__(self):
    return 'connecion timed out'
  
  def establishConnection(self, cm: ConnectionManager):
    if os.system(f'ping -c 1 {cm.host_ip} > /dev/null ') == 0:
      cm.setState(ConnectionOpened())
