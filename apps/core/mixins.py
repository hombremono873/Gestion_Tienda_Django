from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

"""
    Exige sesión iniciada y que el rol del usuario esté en roles_permitidos.
    Sin sesión redirige al login; con un rol no permitido responde 403.
"""
class RolRequeridoMixins(LoginRequiredMixin, UserPassesTestMixin):
    roles_permitidos = []

    def test_func(self):
       return self.request.user.rol in self.roles_permitidos
