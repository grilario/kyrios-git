import mimetypes
import posixpath
import re
from pathlib import Path

from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotModified
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from kyrios.settings import MEDIA_ROOT


def serve(request, filename, uuid=None, mediaPath=MEDIA_ROOT):
    file = uuid + '_' + filename if uuid else filename   
    path = posixpath.normpath(file).lstrip("/")
    path = Path(safe_join(mediaPath, path))

    if path.is_dir():
        raise Http404(_("Directory indexes are not allowed here."))

    if not path.exists():
        raise Http404(_("“%(path)s” does not exist") % {"path": path})

    statobj = path.stat()
    if not was_modified_since(
        request.META.get(
            "HTTP_IF_MODIFIED_SINCE"), statobj.st_mtime, statobj.st_size
    ):
        return HttpResponseNotModified()

    content_type, encoding = mimetypes.guess_type(str(path))
    content_type = content_type or "application/octet-stream"

    response = FileResponse(path.open("rb"), content_type=content_type)
    response.headers["Last-Modified"] = http_date(statobj.st_mtime)

    if encoding:
        response.headers["Content-Encoding"] = encoding
    response.headers["Content-Disposition"] = f'inline; filename="{filename}"'

    return response




DEFAULT_DIRECTORY_INDEX_TEMPLATE = """
{% load i18n %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <meta http-equiv="Content-Language" content="en-us">
    <meta name="robots" content="NONE,NOARCHIVE">
    <title>{% blocktranslate %}Index of {{ directory }}{% endblocktranslate %}</title>
  </head>
  <body>
    <h1>{% blocktranslate %}Index of {{ directory }}{% endblocktranslate %}</h1>
    <ul>
      {% if directory != "/" %}
      <li><a href="../">../</a></li>
      {% endif %}
      {% for f in file_list %}
      <li><a href="{{ f|urlencode }}">{{ f }}</a></li>
      {% endfor %}
    </ul>
  </body>
</html>
"""
template_translatable = gettext_lazy("Index of %(directory)s")


def directory_index(path, fullpath):
    try:
        t = loader.select_template(
            [
                "static/directory_index.html",
                "static/directory_index",
            ]
        )
    except TemplateDoesNotExist:
        t = Engine(libraries={"i18n": "django.templatetags.i18n"}).from_string(
            DEFAULT_DIRECTORY_INDEX_TEMPLATE
        )
        c = Context()
    else:
        c = {}
    files = []
    for f in fullpath.iterdir():
        if not f.name.startswith("."):
            url = str(f.relative_to(fullpath))
            if f.is_dir():
                url += "/"
            files.append(url)
    c.update(
        {
            "directory": path + "/",
            "file_list": files,
        }
    )
    return HttpResponse(t.render(c))


def was_modified_since(header=None, mtime=0, size=0):
    try:
        if header is None:
            raise ValueError
        matches = re.match(
            r"^([^;]+)(; length=([0-9]+))?$", header, re.IGNORECASE)
        header_mtime = parse_http_date(matches[1])
        header_len = matches[3]
        if header_len and int(header_len) != size:
            raise ValueError
        if int(mtime) > header_mtime:
            raise ValueError
    except (AttributeError, ValueError, OverflowError):
        return True
    return False
