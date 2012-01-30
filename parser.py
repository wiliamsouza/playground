import urllib2
import re

from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen('http://www.paodeacucar.com.br/secoes/C46_C51/bebida/cerveja?sort=&rows=61')
soup = BeautifulSoup(page)

for product in  soup.findAll(id=re.compile('^line_')):
    product_link = product.find('a', attrs={'class': 'prdNome'})
    product_name = product_link['title']
    product_small_image = product_link.find('img', attrs={'class': 'prdImagem'})['src']
    product_big_image = product_small_image.replace('_t1', '_a1')
    product_price = product.find('span', attrs={'class': 'prdPreco prdPrices'}).strong.contents

    print product_name
    print product_price
    print '-' * 80
