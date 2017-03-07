from pyventory import Asset


class All(Asset):
    run_tests = False
    use_redis = False
    redis_host = 'localhost'
    minify = False
    version = 'develop'
