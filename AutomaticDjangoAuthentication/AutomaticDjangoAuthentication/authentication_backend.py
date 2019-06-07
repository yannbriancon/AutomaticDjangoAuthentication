from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from ldap3 import Server, Connection, ALL


class AuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = request.GET.get('username')
        password = request.GET.get('password')
        if AuthenticationBackend._search_user(username, password) is None:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def _search_user(username, password):
        try:
            server = Server('ldap.forumsys.com', get_info=ALL)
            connection = Connection(server,
                                    'uid={username},dc=example,dc=com'.format(
                                        username=username),
                                    password, auto_bind=True)

            connection.search('dc=example,dc=com', '({attr}={login})'.format(
                attr='uid', login=username), attributes=['cn'])

            if len(connection.response) == 0:
                return None

            return connection.response[0]
        except:
            return None