from libmproxy import filt
from libmproxy.version import IVERSION
if IVERSION[1] < 14:
  from libmproxy.protocol.http import HTTPResponse
  from netlib.odict import ODictCaseless
else:
  # I didn't actually test this, it's probably broken
  from libmproxy.models import HTTPResponse
  from netlib.http import Headers

def start(context, argv):
  if len(argv) == 3:
    context.content_type = "application/json"
    context.filename = argv[2]
  elif len(argv) == 4:
    context.content_type = argv[2]
    context.filename = argv[3]
  else:
    raise ValueError("Wrong format: filter [content-type] filename")

  context.filter = filt.parse(argv[1])

def request(context, flow):
  if flow.match(context.filter):
    if IVERSION[1] < 14:
      headers = ODictCaseless([["Content-Type", context.content_type]])
    else:
      headers = Headers(Content_Type=context.content_type)

    with open(context.filename) as f:
      flow.reply(HTTPResponse(
        [1,1], 200, "OK",
        headers,
        f.read()
        ))
