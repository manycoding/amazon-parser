import re
import router
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from operator import itemgetter


def get_department_urls():
    """Get links of all first level departments."""
    soup = BeautifulSoup(router.do_get(
        "https://www.amazon.com/Best-Sellers/zgbs/").text, "html.parser")

    return [a.attrs["href"] for a in soup.find_all(
        "a",
        href=re.compile("https://www.amazon.com/Best-Sellers-"))]


def get_bestsellers_data(url):
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

        if rating > 3.5 and reviews > 300:
            dep_bestsellers.append({"name": name, "rating": rating,
                                   "reviews": reviews, "price": float(price)})

    return dep_bestsellers


def get_percentile(list, p):
    a = np.array(list)
    return np.percentile(a, 80)


def get_bestsellers(urls):
    """Create list from each department"""
    bestsellers = []
    for u in urls:
        try:
            b = get_bestsellers_data(u)
            bestsellers += b
        except Exception as e:
            print("Skipping {}".format(u))
            print(str(e))
    return bestsellers


def filter_data(dict, key, value):
    return list(filter(lambda b: b['price'] < value, dict))


def main():
    dep_urls = get_department_urls()
    bestsellers = get_bestsellers(dep_urls)
    # print(bestsellers)
    sorted_b = sorted(bestsellers, key=itemgetter('price', 'reviews'))
    p = get_percentile([b['price'] for b in sorted_b], 95)
    print("Percentile is: {}".format(p))

    # Filter by percentile
    reduced_b = filter_data(dict=sorted_b, key='price', value=p)

    x_values = [b['price'] for b in reduced_b]
    x_values = np.array(x_values)
    y_values = [b['reviews'] for b in reduced_b]

    # Set the size of the plotting window.
    plt.figure(dpi=128, figsize=(10, 6))

    plt.scatter(x_values, y_values, edgecolor='none', s=3)
    plt.show()


if __name__ == "__main__":
    main()
