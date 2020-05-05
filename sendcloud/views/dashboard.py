import logging
from django.views import generic
from sendcloud.core.user_info import UserInfoAPI

from sendcloud.minixs import TemplateListMixin, MailStatusMixin

logger = logging.getLogger("sendcloud")


class UserInfoMixin(object):
    def get_userinfo(self):
        r = UserInfoAPI().user_info()
        return r["info"]


class DashboardView(
    TemplateListMixin, MailStatusMixin, UserInfoMixin, generic.TemplateView
):
    template_name = "sendcloud/dashboard.html"

    def get_context_data(self, **kwargs):
        _context = super(DashboardView, self).get_context_data()
        _userinfo = self.get_userinfo()

        logger.info(self.get_invalid_stat())

        _context.update(_userinfo)
        _context.update(
            {
                "template_list": self.get_template_list(),
                "invalid_stat": self.get_invalid_stat(),
            }
        )
        return _context
