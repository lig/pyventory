from pyvars import All


class Staging(All):
    run_tests = True


class Production(All):
    use_redis = True
    minify = True
    version = 'master'
