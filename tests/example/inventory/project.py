from inventory import All


class BackEnd(All):
    use_redis = True


class FrontEnd(All):
    pass
