import lxml.html
tree=lxml.html.parse("http://www.sueddeutsche.de/news/activevisits")
tree.xpath('//div[class="entrylist__entry"]')
tree.xpath('//div[@class="entrylist__entry"]')
for e in tree.xpath('//div[@class="entrylist__entry"]') : 
    print(e)
for e in tree.xpath('//div[@class="entrylist__entry"]') : 
    print(e.xpath('.//span[@class="entrylist__socialcount"]/text()'))
for e in tree.xpath('//div[@class="entrylist__entry"]') : 
    print(e.xpath('.//span[@class="entrylist__socialcount"]/text()'))
for e in tree.xpath('//div[@class="entrylist__entry"]') : 
    print(e.xpath('.//span[@class="entrylist__socialcount"]/text()'),
    e.xpath('.//em[@class="entrylist__title"]/text()')
    )
%history -h xpath-test.py
%history -f xpath-test.py
