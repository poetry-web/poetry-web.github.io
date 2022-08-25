import os
from collections import defaultdict

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:5])

path = "../poems-source/"

with open("poem_template.html", 'r') as f:
	base = f.read()

years = defaultdict(set)

for filename in os.listdir(path):
  with open(os.path.join(path, filename), 'r') as f:
      data = [l for l in f.read().split("\n") if l]
      title, date, info, lines = data[0], data[1], data[2], data[3:]
      year = date[-4:]

      the_poem = "<p>"
      will_indent, do_indent = False, False
      for line in lines:

      	if will_indent:
      		do_indent = True
      		will_indent = False

      	if "\\verselinebreak" in line:
      		will_indent = True
      		the_line = line.replace("\\verselinebreak", "")
      		after = "<br>\n"
      	elif "\\breakstanza" in line:
      		will_indent = True
      		the_line = line.replace("\\breakstanza", "")
      		after =  "</p>\n<p>"
      	elif "\\\\!" in line:
      		the_line = line.replace("\\\\!", "")
      		after =  "</p>\n<p>"
      	elif "\\\\" in line:
      		the_line = line.replace("\\\\", "")
      		after = "<br>\n"
      	else:
      		raise Exception()

      	if do_indent:
      		the_poem += "\t<span class=\"tab\">" + the_line + "</span>" + after
      		do_indent = False
      	else:
      		the_poem += the_line + after

      while True:
      	tmp = the_poem.split("\n")
      	if tmp[-1] == "<p>" or tmp[-1] == "":
      		the_poem = "\n".join(tmp[:-1])
      	else:
      		break

      poem = str(base)
      poem = poem.replace("{{TITLE}}", title)
      poem = poem.replace("{{POEM}}", the_poem)
      poem = poem.replace("{{INFO}}", info + ", " + date if info != "NONE" else date)

      camel_title = to_camel_case(title) + ".html"
      years[year].add((date, title, camel_title, poem))

      with open("../poems/" + camel_title, 'w') as file:
      	file.write(poem)


result = "<!-- Automatically generated -->"

for year, year_set in sorted(years.items()):
	result += f"<h3>{year}</h3>\n\t<ul>\n"
	for _, title, camel_title, poem in sorted(year_set, key = lambda x: x[0].split(".")[::-1]):
		result += "\t\t<li> <a href=\"./poems/" + camel_title + "\">" + title + "</a>\n"
	result += "\t</ul>\n"

result += "<!-- END -->"

with open("index_template.html", "r") as file:
	data = file.read()

data = data.replace("{{poems}}", result)

with open("../index.html", "w") as file:
	file.write(data)