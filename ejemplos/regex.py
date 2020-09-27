import re

text = 'me llamo jose y tu'

m = re.search('(.+?)(llamo)(.+?)', text)
if m:
    for x in m.groups():
        print(x)

    for x in m.groupdict():
        print(x)

#m = re.match("\W*llamo[^:]*:\D*(\d+)", t)
m = re.match(".*llamo(.*)y tu.*", text)
print(m.group(1))
# found: 1234


s = 'gfgfdAAA1234ZZZuijjk'
start = s.find('AAA') + 3
end = s.find('ZZZ', start)
print(s[start:end])


print(re.findall(r'\d{1,5}','gfgfdAAA1234ZZZuijjk'))