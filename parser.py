import re
import router
import numpy as np
from bs4 import BeautifulSoup
from operator import itemgetter


class Parser:
    """Get bestsellers data from Amazon departments and filter it."""
    PERCENTILE = 95

    def get_department_urls(self):
        """Get links of all first level departments."""
        soup = BeautifulSoup(router.do_get(
            "https://www.amazon.com/Best-Sellers/zgbs/").text, "html.parser")

        return [a.attrs["href"] for a in soup.find_all(
            "a",
            href=re.compile("https://www.amazon.com/Best-Sellers-"))]

    def get_department_bestsellers(self, url):
        """Parse name, rating, reviews and price from department url"""
        # print(url)
        dep_bestsellers = []
        b_soup = BeautifulSoup(router.do_get(url).text, "html.parser")
        # Find first bestseller data
        bestsellers = b_soup.find_all("div", class_="zg_itemImmersion")
        for b in bestsellers:
            name = b.find("a").text.strip()
            rating = float(b.find("a", href=re.compile(
                "/product-reviews")).text.split()[0])
            reviews = int(b.find("a", class_="a-size-small").text.
                          replace(",", ""))
            price = b.find("span", class_="p13n-sc-price").text[1:]

            if reviews > 300:
                b = {"name": name, "rating": rating, "reviews": reviews,
                     "price": float(price)}
                # Track the most reviewed
                if reviews > self.max_reviews:
                    self.top = b
                    self.max_reviews = reviews
                dep_bestsellers.append(b)

        return dep_bestsellers

    def get_percentile(self, list, p):
        a = np.array(list)
        return np.percentile(a, 80)

    def get_bestsellers(self, urls):
        """Create list from each department"""
        self.max_reviews = 0
        bestsellers = []
        for u in urls:
            try:
                b = self.get_department_bestsellers(u)
                bestsellers += b
            except Exception as e:
                print("Skipping {}".format(u))
                print(str(e))
        return bestsellers

    def filter_data(self, dict, key, value):
        return list(filter(lambda b: b['price'] < value, dict))

    def get_data(self):
        dep_urls = self.get_department_urls()
        bestsellers = self.get_bestsellers(dep_urls)

        # Remove duplicates
        bestsellers = [dict(t) for t in set([tuple(d.items())
                                             for d in bestsellers])]
        print("Found {} bestsellers".format(len(bestsellers)))

        sorted_b = sorted(bestsellers, key=itemgetter('price', 'reviews'))
        p = self.get_percentile([b['price']
                                 for b in sorted_b], self.PERCENTILE)
        print("Percentile value is: {}".format(p))

        # Filter by percentile
        filtered_b = self.filter_data(dict=sorted_b, key='price', value=p)
        print("Filtered to {} by {} percentile".format(
            len(filtered_b), self.PERCENTILE))

        return filtered_b
