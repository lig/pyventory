from pyventory import InventoryItem


class All(InventoryItem):
    run_tests = False
    use_redis = False
    redis_host = 'localhost'
    minify = False
    version = 'develop'
