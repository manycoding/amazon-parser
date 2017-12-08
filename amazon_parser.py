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

        if reviews > 300:
            b = {"name": name, "rating": rating, "reviews": reviews,
                 "price": float(price)}
            dep_bestsellers.append(b)

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
    print("Found {} bestsellers".format(len(bestsellers)))

    # Remove duplicates
    bestsellers = [dict(t) for t in set([tuple(d.items())
                                         for d in bestsellers])]
    print("Removed duplcates\n {}".format(len(bestsellers)))

    sorted_b = sorted(bestsellers, key=itemgetter('price', 'reviews'))
    p = get_percentile([b['price'] for b in sorted_b], 95)
    print("Percentile value is: {}".format(p))

    # Filter by percentile
    filtered_b = filter_data(dict=sorted_b, key='price', value=p)
    print("Filtered to {}".format(len(filtered_b)))

    x_values = [b['price'] for b in filtered_b]
    y_values = [b['reviews'] for b in filtered_b]

    # Print the name of top item
    top_name = [b['name'] for b in filtered_b if b['reviews'] == max(y_values)]
    print("The most reviewed is {}".format(top_name))

    # Set the size of the plotting window.
    plt.figure(dpi=128, figsize=(10, 6))

    plt.scatter(x_values, y_values, edgecolor='none', s=3)
    plt.show()


if __name__ == "__main__":
    main()
