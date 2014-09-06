from dj_static import Cling


class MezzrowCling(Cling):
    def get_base_url(self):
        return '/static/'
