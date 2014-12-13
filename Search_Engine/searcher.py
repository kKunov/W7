from searcher_class import Spider


def search_more_than_one_site():
    file = open('sites.txt', 'r')
    sites = file.read().split('\n')
    file.close()

    for line in sites:
        print(line)
        site = Spider(line)
        site.scan_website()


def main():
    search_more_than_one_site()


if __name__ == '__main__':
    main()
