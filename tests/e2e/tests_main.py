import pytest, time
#from tests.BaseTestCase import *
from src.Services.ConnectionManager import ConnectionOpened
from src.Commands.PowerCommand import PowerRestart
from src.Commands.TR69Command import TR69ReadParameters

from src.Services.Service import IService, ServiceSubscriber

from src.Libraries.TR69Manager.TR69Manager import ITR69Manager
from src.Libraries.PowerController.PowerController import IPowerController

@pytest.mark.incremental
class TestRestartPower(object):
  @pytest.mark.timeout(timeout=5,method="signal")
  def test_env_power(self, power_ctrl: IPowerController):
    result = PowerRestart(power_ctrl).execute()
    assert result == 0

@pytest.mark.incremental
class TestConnectivityLan(TestRestartPower):
  @pytest.mark.timeout(timeout=180, method="signal")
  def test_svc_connectivity_lan(self, cm_lan: IService):
    subscriber = ServiceSubscriber(cm_lan, ConnectionOpened()) 
    subscriber.catchEvent(1)
    assert True

@pytest.mark.incremental
class TestConnectivityWan(TestConnectivityLan):
  @pytest.mark.timeout(timeout=60,method="signal")
  def test_svc_connectivity_wan(self, cm_wan_acs: IService):
    subscriber = ServiceSubscriber(cm_wan_acs, ConnectionOpened()) 
    subscriber.catchEvent(1)
    assert True

@pytest.mark.incremental
class TestDeviceAccessFromAcs(TestConnectivityWan):
  def test_cmd_read_sn(self, tr69_mgr: ITR69Manager) -> int:
    param='Device.GatewayInfo.SerialNumber'
    time.sleep(30)
    result = TR69ReadParameters(tr69_mgr, param).execute()
    assert result == tr69_mgr.serial_number
