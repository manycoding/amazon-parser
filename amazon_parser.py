import argparse
import matplotlib.pyplot as plt
from parser import Parser
from mpl_toolkits.mplot3d import Axes3D


def draw_2d(x_values, y_values):
    plt.figure(dpi=128, figsize=(10, 6))
    ax = plt.gca()
    ax.set_xlabel('$')
    ax.set_ylabel('Reviews')

    ax.scatter(x_values, y_values, edgecolor='none', s=3)
    plt.show()


def draw_3d(x_values, y_values, z_values):
    plt.figure(dpi=128, figsize=(10, 6))
    ax = plt.gca(projection='3d')

    ax.set_title('3D Scatter Plot')
    ax.set_xlabel('$')
    ax.set_ylabel('Reviews')
    ax.set_zlabel('Rating')

    ax.scatter(x_values, y_values, z_values, c='r', marker='o')

    plt.show()


def main(type):
    p = Parser()
    b_data = p.get_data()

    x_values = [b['price'] for b in b_data]
    y_values = [b['reviews'] for b in b_data]
    z_values = [b['rating'] for b in b_data]

    # Print the name of top item
    print(
        "The most reviewed is\n {name} {reviews} {rating} {price}".
        format(**p.top))

    if type == '2d':
        draw_2d(x_values, y_values)
    else:
        draw_3d(x_values, y_values, z_values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph", choices=["2d", "3d"], default="2d", help="Graph type")
    args = parser.parse_args()
    main(args.graph)
