from urllib.parse import urlencode


def google_maps_link(attraction, destination):
    query = attraction + ", " + destination
    return "https://www.google.com/maps/search/?" + urlencode({"api": 1, "query": query})
