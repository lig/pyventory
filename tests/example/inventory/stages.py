from inventory.env import Staging
from inventory.project import BackEnd, FrontEnd


class DevelopHost(Staging, BackEnd, FrontEnd):
    ansible_host = 'develop_hostname'
    version = 'develop'
    extra = {
        'debug': 1
    }


class StagingHost(Staging, BackEnd, FrontEnd):
    ansible_host = 'master_hostname'
    version = 'master'
    extra_branches = ['foo', 'bar']
    extra_objs = [
        {
            'prop1': 'value1',
            'prop2': 'value2',
        },
        {
            'prop3': 'value3',
            'prop4': 'value4',
        },
    ]
