import matplotlib.pyplot as plt
from parser import Parser


def main():
    p = Parser()
    b_data = p.get_data()

    x_values = [b['price'] for b in b_data]
    y_values = [b['reviews'] for b in b_data]

    # Print the name of top item
    print(
        "The most reviewed is\n {name} {reviews} {rating} {price}".
        format(**p.top))

    # Set the size of the plotting window.
    plt.figure(dpi=128, figsize=(10, 6))

    plt.scatter(x_values, y_values, edgecolor='none', s=3)
    plt.show()


if __name__ == "__main__":
    main()
