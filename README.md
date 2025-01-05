# Build Your Own Flask API

## In this example python script I start by building the basic framework below for our Flask Application.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return  "Home"

if __name__ == "__main__":
    app.run(debug=True)
```

## By running this code, you will see similar debug info in your terminal:

```
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 740-075-329
```

## The decorator above the home() function indicates that this function occurs when navigating to root in your web browser.

![Screenshot from 2025-01-05 06-20-46](https://github.com/user-attachments/assets/8f0f65a0-d281-46fe-a54b-770d874e8987)

## Using the same path in Postman shows simply the text string that we returned.

![Screenshot from 2025-01-05 06-17-18](https://github.com/user-attachments/assets/bcc35a30-05b2-4a63-bc4f-1be9724bf75a)

# I created an additional function called get_movie() with the following decorator.

```python
@app.route("/get-movie/<movie_title>")
def get_movie(movie_title):

    url = f"https://yts.mx/browse-movies/{movie_title}/all/all/0/latest/0/all"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    responses = get_page_links(soup)
    print(type(responses))
    status_code = 200
    # check to make sure something was returned
    if responses == {}:
        status_code = 204

    return responses, status_code
```

## '<movie_title>' indicates a user defined string.

## Here is the response in Postman.

![Screenshot from 2025-01-05 06-52-12](https://github.com/user-attachments/assets/132a0583-b82c-4474-bda8-ef7cb3ad16e2)
