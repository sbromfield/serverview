import sys
import json
import feedparser
import re
import datetime

def check(title):
  regex = re.compile("(\d+)")
  r= regex.findall(title)
  t = datetime.date.today()-datetime.timedelta(1)
  classday = int(t.strftime("%d"))

  if r:
    day = int(r[0])

    if day == classday:
      return True
    else:
        return False

  else:
      return false

if __name__ == "__main__":
  if(len(sys.argv) == 2):
    print "Opening " + sys.argv[1]
  else:
    print "error"
    sys.exit(0) 

  try:
    f = open(sys.argv[1])
    data = json.load(f)

    for k in data:
      d = feedparser.parse(k[1].replace(" ", "%20"))
      index = len(d.entries) - 1 
      test = check(d.entries[index].title)
      if test == False :
        print "problem with class " + k[0]
      else:
        print k[0] + " recorded just fine."
  except:
    print "error"
    sys.exit(0)
