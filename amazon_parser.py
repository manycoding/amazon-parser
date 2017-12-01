import re
import router
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


def get_bestseller_data(url):
    """Parse name, rating, reviews and price from department url"""
    # print(url)
    b_soup = BeautifulSoup(router.do_get(url).text, "html.parser")
    # Find first bestseller data
    bestseller = b_soup.find("div", class_="zg_itemImmersion")
    name = bestseller.find("a").text.strip()
    rating = float(bestseller.find("a", href=re.compile(
        "/product-reviews")).text.split()[0])
    reviews = int(bestseller.find("a", class_="a-size-small").text.
                  replace(",", ""))
    price = bestseller.find("span", class_="p13n-sc-price").text[1:]
    if rating < 4.0 or reviews < 300:
        print(rating)
        print(reviews)
        return None
    return {"name": name, "rating": rating, "reviews": reviews,
            "price": float(price)}


def get_bestsellers(urls):
    """Create list from each department"""
    bestsellers = []
    for u in urls:
        try:
            bestsellers.append(get_bestseller_data(u))
        except Exception as e:
            print("Skipping {}".format(u))
            print(str(e))
    return bestsellers


def main():
    dep_urls = get_department_urls()
    bestsellers = get_bestsellers(dep_urls)
    sorted_b = sorted(bestsellers, key=itemgetter('price', 'reviews'))
    print(bestsellers)
    x_values = [b['price'] for b in sorted_b]
    y_values = [b['reviews'] for b in sorted_b]
    plt.scatter(x_values, y_values, c=len(x_values), cmap=plt.cm.Blues,
                edgecolor='none', s=2)
    plt.show()
    # print(get_bestseller_data("https://www.amazon.com/Best-Sellers-MP3-Downloads/zgbs/dmusic"))


if __name__ == "__main__":
    main()
