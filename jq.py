from libmproxy import filt
from subprocess import Popen, PIPE

def start(context, argv):
  if len(argv) != 3:
    raise ValueError("Must give a filter and a jq expression")
  context.filter = filt.parse(argv[1])
  context.expression = argv[2]

def response(context, flow):
  if flow.match(context.filter):
    p = Popen(['jq', context.expression], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    flow.response.content = p.communicate(input=flow.response.content)[0]
