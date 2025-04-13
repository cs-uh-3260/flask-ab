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

Go to `frontend/frontend.py` and comment Line 13 and uncomment Lines 15 - 25. 

Shut down your containers using `docker compose down` and run them again using `docker compose up --build -d`. Now, repeat the above steps of running your applicant, clearing the cookies, and refreshing a couple of times: you should see a different variant in some of these times where some of these variants would end up with the "-- NEW VARIANT" message.

### Step 2: Log the experiment results

Ok, great but how do I know which variant performed better? We need a way to track the experiment results.

## Your Task

Add another page for deleting a student. This page will communicate with the backend.

Try to think about what you need systematically:

1. You need the html page that will contain the form for deleting a student (hint: we need to enter the email of the student we will delete). This will go into the templates/ folder

2. You need to specify what will happen when that forms gets submitted. This is the code that will go into the js/student.js script. It should be something similar to adding a student (i.e., you need to call the write backend endpoint)

3. You need to add a frontend url for this page. This will be another function and route in your frontend.py file

4. Finally, add a link for this page on the index.html page

Thus, in summary, you will need to edit/add the following files

- create a new `delete_student.html` page in frontend/templates
- add new javascript code for handling the submission of the delete student form in `frontend/static/js/students.js`
- add the new frontend endpoint/url for delete student in `frontend/frontend.py`
- add needed link in `index.html`