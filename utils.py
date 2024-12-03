def get_urls_from_file(filename):
    with open(filename, 'r') as file:
        links = [line.rstrip() for line in file]
    return links