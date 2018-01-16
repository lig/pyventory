from inventory.env import Staging
from inventory.project import BackEnd, FrontEnd


class DevelopHost(Staging, BackEnd, FrontEnd):
    ansible_host = 'develop_hostname'
    version = 'develop'


class StagingHost(Staging, BackEnd, FrontEnd):
    ansible_host = 'master_hostname'
    version = 'master'
