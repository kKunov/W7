from searcher_class import Spider


def main():
    website = input("Site:")
    site = Spider(website)
    site.scan_website()


if __name__ == '__main__':
    main()
