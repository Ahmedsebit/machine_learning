from bs4 import BeautifulSoup

html = ['<html><heading style=""font-size:20><i>This is the heading<br><br></i></heading>',
        '<body><b>This is the body</b><p id="paral">This is a paral <a href="www.google.com">Google</a></p>',
        '<p id="paral2">This is a paral 2</p></html>']

html = ''.join(html)

soup = BeautifulSoup(html, "html.parser")

# print (soup.prettify())

# print (soup.html.name)

# print (soup.body.name)

# print (soup.body.text)

# print (soup.body.contents)

# print (soup.body.parent.name)

# print (soup.b.nextSibling)

# print (soup.p.previousSibling)

b = soup.findAll('b')

# print(b[0].text)


paras = ' '.join([p.text for p in soup.findAll('p')])

# print(paras)

# print (soup.findAll(id='paral')[0].text)

# print(soup.findAll(['b','p']))

# print(soup.findAll({'b':True,'p':True}))

links = soup.find('a')

# print(links['href'])

# print (soup.find(text='Google').findNext('p').next)

print(soup.body('p'))