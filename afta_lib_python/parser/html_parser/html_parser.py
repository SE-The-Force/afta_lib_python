from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from collections import deque

class HtmlParser:
    def __init__(self, domain, depth=1):
        self.domain = domain
        self.depth = depth
        self.visited = set()
        self.robots_cache = {}

    def is_stored(self, header):
        return header in ["Content", "url"]

    def is_indexable(self, header):
        return header == "Content"

    def is_analyzed(self, header):
        return header == "Content"

    def is_crawlable(self, url):
        try:
            domain = urlparse(url).hostname
            if domain in self.domain and url not in self.visited:
                robots_url = urljoin(self.domain, '/robots.txt')
                
                if robots_url in self.robots_cache:
                    robots_content = self.robots_cache[robots_url]
                else:
                    response = requests.get(robots_url, headers={'User-Agent': 'Googlebot'})
                    robots_content = response.text
                    self.robots_cache[robots_url] = robots_content
                # print(url)
                # print(urlparse("https://www.hanaelias.org").path)
                # print(robots_content)
                disallow = f"Disallow: {urlparse(url).path}"
                is_allowed = disallow not in robots_content
                if disallow == "Disallow: ":
                    return True
                return is_allowed
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        return False

    async def crawl(self):
        stack = deque([(self.domain, 0)])
        results = []
        while stack:
            url, depth = stack.pop()
            print(f"Visiting: {url}, Depth: {depth}")
            if url not in self.visited:
                if self.is_crawlable(url):
                    try:
                        response = requests.get(url, headers={'User-Agent': 'Googlebot', 'Content-Type': 'text/html'})
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a')
                        content = soup.find('html').get_text()
                        results.append((content, url))
                        if depth + 1 < self.depth:
                            for link in links:
                                link_url = link.get('href')
                                if link_url:
                                    if not (link_url.startswith('http') or link_url.startswith('www')):
                                        link_url = urljoin(url, link_url)
                                    if urlparse(link_url).hostname == self.domain:
                                        stack.append((link_url, depth + 1))
                                        print(stack)
                    except Exception as e:
                        print(f"Error crawling {url}: {str(e)}")
                self.visited.add(url)
        return results
