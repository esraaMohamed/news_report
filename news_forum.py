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
      h1, h2{ text-align: center; }
      div.post { 
        border: 1px solid #999;
        padding: 10px 10px;
        margin: 10px 20%%; 
        }
    </style>
  </head>
  <body>
    <h1>News Report</h1>
    %s
  </body>
</html>
'''

# HTML template for articles data
ARTICLES = '''\
    <div class=post><h3>Article Title</h3>%s<br><h3>Views</h3>%s</div>
'''
# HTML template for authors data
AUTHORS = '''\
    <div class=post><h3>Author name</h3>%s<br><h3>Views</h3>%s</div>
'''
# HTML template for error data
ERRORS = '''\
    <div class=post><h3>Day</h3>%s<br><h3>Error percentage</h3>%s</div>
'''


@app.route('/', methods=['GET'])
def main():
    """
    Main page of the report.
    :return:
    """
    articles = "".join(ARTICLES % (name, views) for name, views in
                       get_three_most_popular_articles())
    authors = "".join(AUTHORS % (name, count) for name, count in
                      get_authors())
    errors = "".join(ERRORS % (date, num) for date, num in get_errors())
    result = "<h2> 3 Most famous articles</h2>'{0}', " \
             "<br><h2> Famous authors</h2>'{1}', " \
             "<br><h2> Error rate was more than 1 percent on:</h2>'{2}'".\
        format(articles, authors, errors)
    html = HTML_WRAP % result
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
