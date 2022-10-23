import re

valid = re.compile(r"^[a2-9tjqk]{5}$")
print(valid.match('23336').group(), valid.match("23336").groups())