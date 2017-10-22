#!/usr/bin/env python3
#
# A reporting tool to analyse logs for a news website

import psycopg2
from datetime import datetime

DBNAME = "news"


# Function to return query from database
def get_query_results(query):
                db = psycopg2.connect(database=DBNAME)
                c = db.cursor()
                c.execute(query)
                result = c.fetchall()
                db.close()
                return result


# Returns three most viewed articles along with the view count
def get_popular_articles():
                query = ("select author_join_articles.title, "
                         "path_aggregate.views from path_aggregate, "
                         "author_join_articles where path_aggregate.path "
                         "like concat('%', author_join_articles.slug) "
                         "limit 3;")
                return get_query_results(query)


# Returns authors along with their respective views
def get_popular_authors():
                query = ("select author_join_articles.name, "
                         "sum(path_aggregate.views) as views from "
                         "path_aggregate, author_join_articles "
                         "where path_aggregate.path "
                         "like concat('%', author_join_articles.slug) "
                         "group by author_join_articles.name "
                         "order by views desc;")
                return get_query_results(query)


# Returns the dates where more than 1% of requests returned an error
def get_error_dates():
                query = ("select date, error_percentage from "
                         "error_percentage where error_percentage >=1;")
                return get_query_results(query)


def main():
                # print most popular articles
                print("\nMost popular articles: ")
                articles = get_popular_articles()
                # loop through each row in result
                for article, views in articles:
                                r = "'{}', - {} views".format(article, views)
                                print(r)

                # print most popular authors
                print("\nMost popular authors: ")
                authors = get_popular_authors()
                # loop through each row
                for author, views in authors:
                                r = "{} - {} views".format(author, views)
                                print(r)

                # print error prone days
                print("\nError prone days: ")
                error = get_error_dates()
                # loop through each row
                for date, error_percentage in error:
                                error = "{0:.2f}".format(error_percentage)
                                r = "{} - {} % errors".format(date, error)
                                print(r)


if __name__ == '__main__':
                main()
