from pyventory import Inventory


class All(Inventory):
    run_tests = False
    use_redis = False
    redis_host = 'localhost'
    minify = False
    version = 'develop'
