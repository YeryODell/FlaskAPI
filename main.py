from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_page_links(chunky_soup):
    # pull list of all hrefs belonging to movie titles
    title_links = chunky_soup.findAll('a', {'class': "browse-movie-title"})
    # movie dictionary
    all_results = {}
    listing = 0
    # add listings to dictionary
    for row in title_links:
        listing += 1
        movie = {}
        rows = str(row)
        if rows.find("</span>") == -1:
            title = get_substring(rows, '">', '</a>')
            link = get_substring(rows, 'href="', '">')
            movie.update({
                listing: {
                    "title": title,
                    "link": link,
                }})
        else:
            title = get_substring(rows, '</span> ', '</a>')
            link = get_substring(rows, 'href="', '">')
            movie.update({
                listing: {
                    "title": title,
                    "link": link,
                }})

        movie_link = movie[listing]["link"]
        req = requests.get(url=movie_link)
        nasty_soup = BeautifulSoup(req.text, 'html.parser')
        year = nasty_soup.find('h2').getText()
        movie[listing]["year"] = year
        ratings = nasty_soup.find_all('span', {'itemprop': "ratingValue"})
        rating = get_substring(str(ratings[0]), '">', '</span>')
        movie[listing]["rating"] = rating
        html_summary = nasty_soup.find('div', id = "synopsis").find("p")
        summary = get_substring(str(html_summary), '<p> ', ' </p>')
        movie[listing]["summary"] = summary
        all_results.update(movie)

    # return dictionary of links and titles
    return all_results

# html removal for unique strings
def get_substring(pasta_string, unique_start, unique_end):
    start_index = pasta_string.index(unique_start)
    start_index += len(unique_start)
    end_index = pasta_string.find(unique_end)
    subs = pasta_string[start_index:end_index]
    return subs


@app.route("/")
def home():
    return  "Home"

@app.route("/get-movie/<movie_title>")
def get_movie(movie_title):

    url = f"https://yts.mx/browse-movies/{movie_title}/all/all/0/latest/0/all"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    responses = get_page_links(soup)
    print(type(responses))
    status_code = 200
    # check to make sure a dictionar was returned
    if responses == {}:
        status_code = 204

    return responses, status_code

if __name__ == "__main__":
    app.run(debug=True)