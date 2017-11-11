# "Database code" for the DB News.
# !/usr/bin/env python3

import csv

import psycopg2

DBNAME = "news"


def get_three_most_popular_articles():
    """Return the 3 most popular articles"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = '''
    select title, count(*) from log join articles on path like '%' ||slug ||'%' 
    group by title limit 3;
    '''
    c.execute(query)
    result = c.fetchall()

    with open('results.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='-')
        for row in result:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return result


def get_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = '''
    select authors.name, articleCount from 
    (select author, title, count(*) as articleCount from articles 
    join log on path like '%' ||slug ||'%' group by title, 
     author order by articleCount desc) as article join authors
    on article.author = authors.id 
    group by authors.name, articleCount limit 4;
    '''
    c.execute(query)
    result = c.fetchall()
    with open('results.csv', 'a') as f:
        writer = csv.writer(f, delimiter='-')
        for row in result:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return result


def get_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = '''SELECT 
    l1.time::timestamp::date, count(l2.id)::float / 
    count(l1.id)::float as error_percentage
    FROM 
    public.log as  l1 left join (select * from public.log where status 
    like '%404%') as l2 on l1.id = l2.id
    group by l1.time::timestamp::date
    having count(l2.id)::float / count(l1.id)::float >= 0.01
    '''
    c.execute(query)
    result = c.fetchall()
    with open('results.csv', 'a') as f:
        writer = csv.writer(f, delimiter='-')
        for row in result:
            writer.writerow(row)
        writer.writerow("\n")
    db.close()
    return result
