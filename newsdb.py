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
    except (Exception, psycopg2.DatabaseError):
        print("Database not found, Please check the database name")


def get_three_most_popular_articles():
    """Return the 3 most popular articles"""
    db, cursor = connect(DBNAME)
    query = '''
    SELECT title, views
    FROM articles
    INNER JOIN
        (SELECT path, count(path) AS views
         FROM log
         GROUP BY log.path) AS log
    ON log.path = '/article/' || articles.slug
    ORDER BY views DESC
    LIMIT 3;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    csv.register_dialect('myDialect', delimiter='-')
    my_file = open('results.csv', 'w')
    with my_file:
        writer = csv.writer(my_file, dialect='myDialect')
        writer.writerows(result)
        writer.writerows("\n")
    db.close()
    return result


def get_authors():
    db, cursor = connect(DBNAME)
    query = '''
    select authors.name, sum(articleCount) as views from
    (select author, title, count(*) as articleCount from articles
    join log on log.path = concat('/article/', articles.slug)
    group by title, author order by articleCount desc) as article
    join authors on article.author = authors.id
    group by authors.name
    order by views desc limit 4;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    csv.register_dialect('myDialect', delimiter='-')
    my_file = open('results.csv', 'a')
    with my_file:
        writer = csv.writer(my_file, dialect='myDialect')
        writer.writerows(result)
        writer.writerows("\n")
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
    csv.register_dialect('myDialect', delimiter='-')
    my_file = open('results.csv', 'a')
    with my_file:
        writer = csv.writer(my_file, dialect='myDialect')
        writer.writerows(lst)
        writer.writerows("\n")
    db.close()
    return lst
