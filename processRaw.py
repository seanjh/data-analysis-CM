import time
import gzip
import simplejson

def parse(filename):
  f = gzip.open(filename, 'r')
  entry = {}
  for l in f:
    l = l.strip()
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:]
    entry[eName] = rest
  yield entry

def processGenderAge():
  res = {}
  ls = open("gender_age_raw.txt", 'r').readlines()
  for l in ls:
    user = {}
    fields = l.split()
    user["user/profileName"] = fields[0]
    if fields[1] != 'unknown':
      user["user/gender"] = fields[1]
    birthday = ' '.join(fields[2:])
    if birthday != 'unknown':
      try:
        unixBirthday = time.mktime(time.strptime(birthday.lower(), "%b %d, %Y"))
        today = time.mktime(time.localtime())
        ageInSeconds = today - unixBirthday
        user['user/birthdayRaw'] = birthday
        user['user/birthdayUnix'] = int(unixBirthday)
        user['user/ageInSeconds'] = int(ageInSeconds)
      except Exception as e:
        pass
    res[user['user/profileName']] = user
  return res

users = processGenderAge()

for e in parse("Beeradvocate.txt.gz"):
  try:
    e['review/appearance'] = float(e['review/appearance'])
    e['review/taste'] = float(e['review/taste'])
    e['review/overall'] = float(e['review/overall'])
    e['review/palate'] = float(e['review/palate'])
    e['review/aroma'] = float(e['review/aroma'])
    e['review/timeUnix'] = int(e['review/time'])
    e.pop('review/time', None)
    try:
      e['beer/ABV'] = float(e['beer/ABV'])
    except Exception as q:
      e.pop('beer/ABV', None)
    e['user/profileName'] = e['review/profileName']
    e.pop('review/profileName', None)
    if users.has_key(e['user/profileName']):
      e.update(users[e['user/profileName']])
    timeStruct = time.gmtime(e['review/timeUnix'])
    e['review/timeStruct'] = dict(zip(["year", "mon", "mday", "hour", "min", "sec", "wday", "yday", "isdst"], list(timeStruct)))
    print e
  except Exception as q:
    pass
