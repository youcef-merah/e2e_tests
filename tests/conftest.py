import pytest
import pandas

from typing import Dict, Tuple

from src.Services.ServiceFactory import *
from src.Libraries.PowerController.PowerController import *
from src.Libraries.TR69Manager.TR69Manager import *

def pytest_addoption(parser):
   parser.addoption("--out", action="store")

@pytest.fixture
def out(request):
   return request.config.getoption("--out")

@pytest.fixture()
def power_ctrl(out):
  #return RelayArduinoController(out_port=out) # cast to int if necessary
  return NetioTelnetController(out_port=out)

@pytest.fixture()
def tr69_mgr():
  return GeniAcsHttp(serial_number='YAAC22060187', oui='38A659', model='MERCV3X', host_ip='192.168.27.15', host_port='7557')

@pytest.fixture()
def cm_lan():
  cm = ConnectionManagerFactory().createService(host_ip='192.168.0.1', host_port=80)
  return cm

@pytest.fixture()
def cm_wan_acs():
  cm = ConnectionManagerFactory().createService(host_ip='192.168.27.15', host_port=7557)
  return cm

def pytest_csv_written(csv_path):
    csv_dir= os.path.dirname(csv_path)
    csv_detailed_path = f'{csv_dir}/report-detailed.csv'
    
    df = pandas.read_csv(csv_path)
    df_passed = df[df['status'] == 'passed']
    df_failed = df[df['status'] == 'failed']

    steps = df.nunique()['function']
    total_tests = df.shape[0] / steps
    total_fails = df_failed.shape[0]

    df_main_results = pandas.DataFrame({ '# Tests': [total_tests],  '# Fails': [int(total_fails)], '% Fails':[(total_fails/float(total_tests))*100] })
    df_failed_results = df.groupby('function')['status'].apply(lambda x: ((x=='failed').sum()/float(total_fails))*100).reset_index(name='count %')
    df_passed_results = df_passed.groupby('function')['duration'].aggregate(['min', 'max', 'mean']).reset_index()
    df_passed_results = df_passed_results.astype({"min":'int', "max":'int', "mean":"int"}) 

    df_list = [df_main_results, df_failed_results, df_passed_results]

    open(csv_detailed_path,'w').close()

    with open(csv_detailed_path,'a') as f:
        for df in df_list:
            df.to_csv(f, sep=';', index=False)
            f.write("\n")

# Sometimes you may have a testing situation which consists of a series of test steps.
# If one step fails it makes no sense to execute further steps as they are all
# expected to fail anyway and their tracebacks add no insight.
# Here is a simple conftest.py file which introduces an incremental marker which is to be used on classes:
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )

def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))
