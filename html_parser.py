import re
import urlparse
from bs4 import BeautifulSoup

#re for regex support
class Parser(object):
	"""docstring for Parser"""
	def _get_new_url(self, page_url, soup):
		new_urls = set()
		links = soup.find_all('a', href = re.compile(r"/item/(.*)"))
		for link in links:
			new_url = link['href']
			new_full_url = urlparse.urljoin(page_url, new_url)
			new_urls.add(new_full_url)
		return new_urls

	def _get_new_data(self, page_url, soup):
		res_data = {}
		res_data['url'] = page_url
		title_node = soup.find('dd', class_ = "lemmaWgt-lemmaTitle-title").find("h1")
		if title_node is None:
			res_data['title'] = "(Null)"
		else:
			res_data['title'] = title_node.get_text()
		summary_node = soup.find('div', class_ = "lemma-summary")
		if summary_node is None:
			res_data['summary'] = "(Null)"
		else:
			res_data['summary'] = summary_node.get_text()
		return res_data

	def parse(self, page_url, html_content):
		if page_url is None or html_content is None:
			return
		soup = BeautifulSoup(html_content, 'html.parser', from_encoding = 'utf-8')
		new_url = self._get_new_url(page_url, soup)
		new_data = self._get_new_data(page_url, soup)
		return new_url, new_data

		