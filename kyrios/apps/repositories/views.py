from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from git.object import GitTree, GitBlob, GIT_BLOB_OBJECT, GIT_TREE_OBJECT
from git.repo import Repo
from utils.urlparser import partition_url


@require_http_methods(['GET'])
def view_repository(request, communityID, username, repository, rev='HEAD'):
    """
        View for showing repository objects inside the given revision (either trees or blobs).
    """

    path1 = '/community' + '/' + communityID + '/' + 'task' + '/' + repository + '/' + username
    path2 = '/' + username + '/' + repository + '.git'
    path = path2 + request.path_info.split(path1)[1]

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    objects = _parse_repo_url(path, requested_repo, rev)

    if objects is None:
        raise Http404()

    context = {
        'repo_name': repository,
        'repo_owner': username,
        'repo_lsmsg': requested_repo.get_latest_status,
        'objects': objects,
    }

    return render(request, 'repositories/detail.html', context)


def _parse_repo_url(request_path, repository, rev):
    """
        Parses url for viewing repository. Splits request url on '/' and checks parts
            to specify which revision and object should be shown.
        e.g.
            Input like "/username/repository.git/tree/master/some/folder/object.c" will return
                branch "master" and blob object "some/folder/object.c" to show.
    """

    request_sections = partition_url(request_path)
    num_sections = len(request_sections)

    if num_sections == 2:
        return repository.ls_tree(recursive=False, rev=rev)
    elif num_sections == 4 and request_sections[2] == GIT_TREE_OBJECT:
        return repository.ls_tree(recursive=False, rev=request_sections[3])
    elif num_sections > 4:
        if request_sections[2] == GIT_TREE_OBJECT:
            return GitTree(repo=repository, path='/'.join(request_sections[4:]), rev=rev).show()
        elif request_sections[2] == GIT_BLOB_OBJECT:
            return GitBlob(repo=repository, path='/'.join(request_sections[4:]), rev=rev)
    else:
        return None
