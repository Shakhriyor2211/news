from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class UserIsStaff(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
