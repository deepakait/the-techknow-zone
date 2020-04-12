from flask import Flask, render_template, request
import pymysql

# Open database connection
db = pymysql.connect("localhost", "root", "root", "the_tech_know_zone")

# prepare a cursor object using cursor() method

cursor = db.cursor()


# @app.route("/contact", methods=['GET', 'POST'])




