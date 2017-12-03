from pyvars.env_groups import Production
from pyvars.project_groups import BackEnd, FrontEnd


class ProdBackEnd(Production, BackEnd):
    redis_host = 'prod_redis_hostname'
    ansible_hostname = 'app{num:03}.prod.dom'


class ProdFrontEnd(Production, FrontEnd):
    ansible_hostname = 'www{num:03}.prod.dom'
