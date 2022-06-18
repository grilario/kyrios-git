from django.urls import re_path

from .views import get_info_refs, service_rpc, \
                                view_repository, repository_settings, repository_area51,    \
                                repository_branches, repository_commits, repository_graphs


urlpatterns = [
    re_path(r'(?P<repository>[-\w]+).git/info/refs', get_info_refs, name='get_info_refs'),
    re_path(r'(?P<repository>[-\w]+).git/git-upload-pack$', service_rpc, name='service_rpc'),
    re_path(r'(?P<repository>[-\w]+).git/git-receive-pack$', service_rpc, name='service_rpc'),
    re_path(r'(?P<repository>[-\w]+).git/settings$', repository_settings, name='repository_settings'),
    re_path(r'(?P<repository>[-\w]+).git/area51$', repository_area51, name='repository_area51'),
    re_path(r'(?P<repository>[-\w]+).git/branches$', repository_branches, name='repository_branches'),
    re_path(r'(?P<repository>[-\w]+).git/commits$', repository_commits, name='repository_commits'),
    re_path(r'(?P<repository>[-\w]+).git/graphs$', repository_graphs, name='repository_graphs'),
    re_path(r'(?P<repository>[-\w]+).git/tree/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    re_path(r'(?P<repository>[-\w]+).git/blob/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    re_path(r'(?P<repository>[-\w]+).git$', view_repository, name='view_repository'),
]