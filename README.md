# Overview

This repo provides two simple ways to implement AB testing. Note that this repo does not have authentication and thus we don't have user identities to attach a variant to or to track. In your project, you have user identities and accordingly, you can save the assigned variant to a user (or in a separate experiment collection) such that you can analyze metrics at a user level later after your experiment.


## How to run

Run 

`docker compose up --build -d`

Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) on your browser, and make sure that you can add a student successfull (just to make sure that you can run the system).

Note how the UI you see for the landing page simply has "Student Management System" as the header (this is what we have been seeing all along). 

[Clear cookies from your browser](https://me-en.kaspersky.com/resource-center/preemptive-safety/how-to-clear-cache-and-cookies) (You can clear only the past hour), refresh the page and try again. You should still see the same message.

## A simple way to implement a variant -- frontend feature example

### Step 1: Serve different variants

Now assume that your design team said that this landing page is confusing and that users navigate away from it and don't end up using your system. They suggest a new design for this landing page, which is the new variant you now want to test in production.

For the purposes of this exercise, we will just assume that this new design includes a "-- NEW VARIANT" in the title.

Now, let's see the simplest way we can implement this variant. We can assume that we will randomly assign users to the original variant (called `index_a.html`) or to the new variant (called `index_b.html`). Note that I have already created these variants. Originally, we would have only had one page called `index.html`.

Go to `frontend/frontend.py` and comment Line 13 and uncomment Lines 15 - 25. These lines make use of the current session to add information to the session cookie about the current variant to serve. We assign this variant randomly. How you assign the variant depends on your experiment setup.

Shut down your containers using `docker compose down` and run them again using `docker compose up --build -d`. Now, repeat the above steps of running your applicant, clearing the cookies, and refreshing a couple of times: you should see a different variant in some of these times where some of these variants would end up with the "-- NEW VARIANT" message.

### Step 2: Log the experiment results

Ok, great we now have two variants, but how do I know which variant performed better? We need a way to track the experiment results.

For the purposes of our small experiment, we will assume we care about how many times users clicked on the "List students" link in the two variants. 

So we will follow a set of steps:

1. We will add a collection and related db functionality for recording experiment results in the DB. Notice the new file `server/db/ab_test.py` that I added? This has a function that records results of an event in the database. So this will be our way of saving an entry in the DB every time a user clicks on the List Students link. This entry will also tell us which variant the user was seeing at that time. Notice how the entry in the DB has the session id? The session id is automatically generated (based on a SECRET_KEY value in your environment) for each new session. It helps us track if these clicks are coming in from the same browsing session or different ones. Since we don't have any user management or authentication right now, we will assume each session is a different user.

2. Ok, now we need to actually call this function every time the user clicks on the link. We will keep our ab logging server side and assume that hitting the server get students endpoints means that the user clicked on the link.

# Browsing data with mongosh

Go to a new terminal

```
mongosh
show databases # make sure you can see abdemo there
use abdemo 
show collections # this will display all collections
db.students.find() # will display all students
db.db.ab_test_logs.find() # will display all abtesting results
```