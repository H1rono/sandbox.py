import argparse

import matplotlib.pyplot as plt
import numpy as np

# samples in https://matplotlib.org/stable/tutorials/pyplot.html


def sample0() -> None:
    plt.plot([1, 2, 3, 4])
    plt.ylabel("some numbers")
    plt.show()


def sample1() -> None:
    # red 'o'
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], "ro")
    # xmin, xmax, ymin, ymax
    plt.axis((0, 6, 0, 20))
    plt.show()


def sample2() -> None:
    # evenly sampled time at 200ms intervals
    t = np.arange(0.0, 5.0, 0.2)
    # red dashes, blue squares, green triangles
    plt.plot(t, t, "r--", t, t**2, "bs", t, np.sqrt(t), "g^")
    plt.show()


def sample3() -> None:
    data = {"a": np.arange(50), "c": np.random.randint(0, 50, 50), "d": np.random.randn(50)}
    data["b"] = data["a"] + 10 * np.random.randn(50)
    data["d"] = np.abs(data["d"]) * 100
    plt.scatter("a", "b", c="c", s="d", data=data)
    plt.xlabel("entry a")
    plt.ylabel("entry b")
    plt.show()


def sample4() -> None:
    names = ["group_a", "group_b", "group_c"]
    values = [1, 10, 100]

    plt.figure(figsize=(9, 3))

    plt.subplot(131)
    plt.bar(names, values)

    plt.subplot(132)
    plt.scatter(names, values)

    plt.subplot(133)
    plt.plot(names, values)

    plt.suptitle("Categorical Plotting")
    plt.show()


def sample5() -> None:
    x = np.arange(-np.pi, np.pi, 0.3)
    y = np.sin(x)

    (line,) = plt.plot(x, y, "-")
    # line.set_alpha(1.0)
    # line.set_animated(False)
    line.set_antialiased(False)
    # line.set_clip_box
    # line.set_clip_on
    line.set_color("#5CCFE6")
    line.set_linewidth(2.0)
    # ...

    plt.show()


def sample6() -> None:
    def f(t):  # type: ignore
        return np.exp(-t) * np.cos(2 * np.pi * t)

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)

    # create a figure
    _fig = plt.figure()

    # nrows, ncols, plot_number, where 1 <= plot_number <= nrows * ncols
    # this call is identical to plt.subplot(2, 1, 1)
    plt.subplot(211)
    plt.plot(t1, f(t1), "bo", t2, f(t2), "k")

    plt.subplot(212)
    plt.plot(t2, np.cos(2 * np.pi * t2), "r--")

    plt.show()


def sample7() -> None:
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(1000)

    # the histogram of the data
    n, bins, patches = plt.hist(x, 50, density=True, facecolor="b", alpha=0.75)

    plt.xlabel("Smarts")
    plt.ylabel("Probability")
    plt.title("Histogram of IQ")
    plt.text(60, 0.025, r"$\mu=100,\ \sigma=15$")
    plt.axis((40, 160, 0, 0.03))
    plt.grid(True)
    plt.show()


def sample8() -> None:
    _ax = plt.subplot()
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2 * np.pi * t)
    (_line,) = plt.plot(t, s, lw=2)

    # annotation comment, xy=annotated point, xytext=comment location, arrowprops=arrow properties
    plt.annotate("local max", xy=(2, 1), xytext=(3, 1.5), arrowprops={"facecolor": "black", "shrink": 0.05})

    plt.ylim(-2, 2)
    plt.show()


def run_sample() -> None:
    parser = argparse.ArgumentParser("plot-sample")
    parser.add_argument("index", type=int, default=0)
    args = parser.parse_args()
    index = args.index
    assert isinstance(index, int)
    match index:
        case 0:
            sample0()
        case 1:
            sample1()
        case 2:
            sample2()
        case 3:
            sample3()
        case 4:
            sample4()
        case 5:
            sample5()
        case 6:
            sample6()
        case 7:
            sample7()
        case 8:
            sample8()
        case _:
            print(f"index {index} is not supported")
