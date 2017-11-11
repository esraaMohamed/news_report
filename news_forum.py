#!/usr/bin/env python3
from flask import Flask

from newsdb import get_three_most_popular_articles, get_authors, get_errors

app = Flask(__name__)

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>News Report</title>
    <style>
      h1, form { text-align: center; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>News Report</h1>
    <!-- post content will go here -->
%s
  </body>
</html>
'''

POST = '''\
    <div class=post><em class=date>%s</em><br>%s</div>
'''


@app.route('/', methods=['GET'])
def three_popular_articles():
    articles = "".join(
        POST % text for text in get_three_most_popular_articles())
    authors = "".join(POST % text for text in get_authors())
    errors = "".join(POST % (date, text) for text, date in get_errors())
    results = articles + authors + errors
    html = HTML_WRAP % results
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


