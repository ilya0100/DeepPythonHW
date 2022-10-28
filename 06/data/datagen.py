from argparse import ArgumentParser
from urllib.request import urlopen


def generate_urls(urls_count):
    urls = set()
    while len(urls) < urls_count:
        page = urlopen("https://en.wikipedia.org/wiki/Special:Random")
        urls.add(page.url)
    
    return urls


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help="Filename")
    parser.add_argument("-k", default=1, help="URLs count")

    args = parser.parse_args()

    with open(args.f, "w") as file:
        for url in generate_urls(int(args.k)):
            file.write(url + "\n")