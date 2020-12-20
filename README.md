# Foodiez (Food with Friends)

## Introduction

I've had an issue with deciding where to eat with my friends for a long time, and this web app should help with that.

With a simple Tinder-like interface, it allows users to add friends and recommend restaurants based on Yelp's dataset that is pulled in externally (since it's 9gb large). I created my own ranking algorithm externally and am working on printing it out neatly in a very simple GUI. I didn't want to bake the ranking system into the web application, and I'm currently developing an API to store the algorithm and the massive Yelp dataset externally on the web.

## Creating the web application

I am using Flask Login to log in and SQLAlchemy to plan and structure my database, tables are stored in login.db with test variables.

## Bugs and shortcomings

Currently, I still have trouble with adding and removing friends. I am still brainstorming ways to make the UI better, and I recently added Type.js to the front to add a more interesting graphic to it.