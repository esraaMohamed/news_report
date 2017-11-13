# !/usr/bin/env python3
#  "Database code" for the DB News.


import csv

import psycopg2

DBNAME = "news"


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except ConnectionError:
        print("Database not found, Please check the database name")


def get_three_most_popular_articles():
    """Return the 3 most popular articles"""
    db, cursor = connect(DBNAME)
    query = '''
    select title, count(*) as views
    from log join articles
    on log.path = concat('/article/', articles.slug)
    group by title
    order by views desc
    limit 3;
    '''
    cursor.execute(query)
    result = cursor.fetchall()

    with open('results.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='-')
        for row in result:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return result


def get_authors():
    db, cursor = connect(DBNAME)
    query = '''
    select authors.name, article.title, articleCount from 
    (select author, title, count(*) as articleCount from articles 
    join log on log.path = concat('/article/', articles.slug) 
    group by title, author order by articleCount desc) as article 
    join authors on article.author = authors.id 
    group by authors.name, article.title, articleCount limit 4;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    with open('results.csv', 'a') as f:
        writer = csv.writer(f, delimiter='-')
        for row in result:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return result


def get_errors():
    db, cursor = connect(DBNAME)
    query = '''SELECT 
    l1.time::timestamp::date, count(l2.id)::float / 
    count(l1.id)::float as error_percentage
    FROM 
    public.log as  l1 left join (select * from public.log where status 
    like '%404%') as l2 on l1.id = l2.id
    group by l1.time::timestamp::date
    having count(l2.id)::float / count(l1.id)::float >= 0.01;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    lst = []
    for r in result:
        date, percentage = r
        percentage *= 100
        date = date.strftime('%B, %d %Y')
        lst.append((date, str(float("%.2f" % percentage))))
    with open('results.csv', 'a') as f:
        writer = csv.writer(f, delimiter='-')
        for row in lst:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return lst
