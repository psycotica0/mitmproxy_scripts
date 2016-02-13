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
  if len(argv) != 3:
    raise ValueError("Must give a filter and a filename")
  context.filter = filt.parse(argv[1])
  context.filename = argv[2]

def request(context, flow):
  if flow.match(context.filter):
    if IVERSION[1] < 14:
      headers = ODictCaseless([["Content-Type","application/json"]])
    else:
      headers = Headers(Content_Type="application/json")

    with open(context.filename) as f:
      flow.reply(HTTPResponse(
        [1,1], 200, "OK",
        headers,
        f.read()
        ))
