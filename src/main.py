import re
import time

import requests

# REFERENCE DOC = https://documentation.solusvm.com/display/DOCS/Functions
# Function .............. : Get virtual server information. Setting any flag to true will return the result.
# Action ................ : info
# Method ................ : GET or POST
# Flags ................. : ipaddr (Returns a list of ip addresses)
#                           hdd    (Returns the hard disk usage in Bytes)
#                           mem    (Returns the memory usage in Bytes)
#                           bw     (Returns the bandwidth usage in Bytes)
#
# Returned values ....... : <ipaddr>123.123.123.123,122.122.122.122,111.111.111.111</ipaddr>
#                           <hdd>total,used,free,percent_used</hdd>
#                           <mem>total,used,free,percent_used</mem>
#                           <bw>total,used,free,percent_used</bw>


settings = open("../settings.txt", "r")
# if you want to continuously run in the terminal, change False in settings.txt to True
loop = True if settings.readline().strip('\n') == "True" else False
# amount of time to sleep if looping, in minutes. change in settings.txt
minutes = int(settings.readline().strip('\n'))
settings.close()

token = open("../tokens.txt", "r")

post_flags = {
    "key": token.readline().strip('\n'),
    "hash": token.readline().strip('\n'),
    "action": "info",
    "bw": "true",
    "hdd": "true",
    # false for now, only outputs 0's in Racknerd's case
    "mem": "false"
}
token.close()
types = ["hdd", "bw", "mem"]

oTypes = ["hostname", "ipaddress"]

url = "https://nerdvm.racknerd.com/api/client/command.php"

# breaks up tags
oPat = re.compile(r'(<(?P<type>\w*?)>.*?</\w*?>)')
# breaks up data inside a tag
iPat = re.compile(r'<.*?>(?P<total>\d*?),(?P<used>\d*?),(?P<free>\d*?),(?P<per>\d*?)</.*?>')
# breaks up simple data inside identification tags
# assumes that you only have a single hostname and ip address,
sPat = re.compile(r'<.*?>(?P<string>.*?)</.*?>')

while True:
    response = requests.request("POST", url, data=post_flags)
    resp = {}

    for i in oPat.finditer(response.text):
        if i.groups()[1] in types:
            s = iPat.match(i.group()).groupdict()
            lKey = list(s.keys())
            for k in lKey:
                if k == "per":
                    # apparently solusvm api on racknerd returns 0.0 for mem and for hdd used, dont know who to blame on
                    # this one or if its a limitation of the racknerd's config
                    if s['used'] != 0.0 or s['total'] != 0.0:
                        # lint warns about conversion error, percentage is the last param according to solusvm doc
                        # assume inputs are floats since conversions are already done in line 72.
                        s[k] = (s['used'] / s['total']) * 100.0
                else:
                    # default response is a str in bytes, stupid conversion to float and convert the float to GB/TB
                    f = float(s[k]) * 1E-09
                    if f >= 1000.0:
                        j = f * 1E-3
                        s[k + '_mag'] = 'TB'
                        s[k + "_display"] = j
                    else:
                        s[k + '_mag'] = 'GB'
                        s[k + "_display"] = f
                    s[k] = f
            resp[i.groups()[1]] = s
        elif i.groups()[1] in oTypes:
            o = sPat.match(i.group()).groups()[0]
            resp[i.groups()[1]] = o

    print(f"{'-' * 61}\n"
          f"\t\t\tVPS status at {time.ctime()}\n"
          f"{'-' * 61}\n"
          f"Hostname: {resp['hostname']:<35}IP:{resp['ipaddress']:}\n")
    for pType in types:
        if post_flags[pType] == "true":
            print(f"{pType:<4}:", end="\t")
            for k in ['total', 'used', 'free']:
                print(f"{k:>3}: {'%.2f' % resp[pType][k + '_display']:>5}{resp[pType][k + '_mag']}", end="\t")
            print(f"{'%.2f' % resp[pType]['per']}%")
    print(f"{'-' * 61}")

    if not loop:
        break

    time.sleep(minutes * 60)
