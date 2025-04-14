# Overview

This repo provides two simple ways to implement AB testing. Note that this repo does not have authentication and thus we don't have user identities to attach a variant to or to track. In your project, you have user identities and accordingly, you can save the assigned variant to a user (or in a separate experiment collection) such that you can analyze metrics at a user level later after your experiment.


## How to run the application

Run 

`docker compose up --build -d`

Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) on your browser, and make sure that you can add a student successfully (just to make sure that you can run the system).

Note how the UI you see for the landing page simply has "Student Management System" as the header (this is what we have been seeing all along in our demos). 

[Clear cookies from your browser](https://me-en.kaspersky.com/resource-center/preemptive-safety/how-to-clear-cache-and-cookies) (You can clear only the past hour), refresh the page and try again. You should still see the same message.

## A simple way to implement a variant -- frontend feature example

### Step 1: Serve different variants

Now assume that your design team said that this landing page is confusing and that users navigate away from it and don't end up using your system. They suggest a new design for this landing page, which is the new variant you now want to test in production.

For the purposes of this exercise, we will just assume that this new design includes a "-- NEW VARIANT" in the title.

Now, let's see the simplest way we can implement this variant. We can assume that we will randomly assign users to the original variant (called `index_a.html`) or to the new variant (called `index_b.html`). Note that I have already created these variants. Originally, we would have only had one page called `index.html`.

Go to `frontend/frontend.py` and comment Line 17 and uncomment Lines 19 - 29 (You will find a comment telling you what to do). These lines add information to the response cookie about the current variant to serve. We assign this variant randomly. How you assign the variant depends on your experiment setup.
We can use information later from this cookie to know which variant to serve.  

Rebuild your containers use `docker compose up --build -d`. Now, repeat the above steps of running your application, clearing the cookies, and refreshing a couple of times: you should see a different variant in some of these times where some of these variants would end up with the "-- NEW VARIANT" message. If you can't see it, try decreasing the expiry time of the cookie to 20seconds and refresh every 20 seconds. You should see different variants being served.

### Step 2: Log the experiment results

Ok, great we now have two variants, but how do we know which variant performed better? We need a way to track the experiment results.

For the purposes of our small experiment, we will assume we care about how many times users clicked on the "List students" link in the two variants (in other words, how many times the backend list students endpoint was called). 

So we will follow a set of steps:

1. We will add a new `ab_test_logs` collection in our db and the related db functionality for recording experiment results in a new file `server/db/ab_test.py`. This file is already created for you; just read it to understand it. It has a function `log_ab_test_event()` that records results of an event in the database in a collection called `ab_test_logs`; this will be our way of saving an entry in the DB every time a user clicks on the List Students link. This entry will also tell us which variant the user was seeing at that time. 

2. Notice how the entry in the DB has a session id? Flask can automatically manage sessions based on a SECRET_KEY setup in the environment (you can find it in .env). Uncomment line 15 in `server/app.py` to set up the key flask needs to manage sessions.

3. Ok, but where is this session ID generated? Whenever, the end point we care about (fetching students gets hit), we want to either retrieve the current session key or generate a new one if the session has expired. Uncomment line 44 in `server/api/student.py` which sets this session ID. Uncomment lines 23-26 to define the function `get_session_id` that we use. Note that the session id helps us track if these clicks are coming in from the same browsing session or different ones. Since we don't have any user management or authentication right now, we will assume each unique session is a different user.

4. Ok cool, but where do we actually call `log_ab_test_event` that we created in step 2.1? In the same API endpoint implementation of retrieving the student list in `server/api/student.py`, we will retrieve the assigned variant from the cookies included in the request (recall that we set the cookies in the front end) and then call `log_ab_test_event` we created to save the ab experiment results. Uncomment lines 45-46.

Rebuild the containers `docker compose up --build -d`. Now, repeat the above steps of running your application, clearing the cookies, and refreshing a couple of times: similar to before, you should see a different variant in some of these times where some of these variants would end up with the "-- NEW VARIANT" message. In each of these variants, make sure to click on "List Students". You can even go back to the previous page and click on "List Students" again.

### Step 3

We will use mongosh to view our experiment results. In a proper experiment (similar to what you will do in deliverable 5), you would write a script to analyze these results and generate visualizations etc.

Go to a new terminal

```
mongosh
show databases # make sure you can see abdemo there
use abdemo 
show collections # this will display all collections
db.students.find() # will display all students
db.ab_test_logs.find() # will display all abtesting results
```

Let's get some insights on the average number of clicks for users from each variant:

```
db.ab_test_logs.aggregate([
  { $match: { event_type: "list_students_viewed" } },

  // Count clicks per session for each variant
  {
    $group: {
      _id: { variant: "$variant", session_id: "$session_id" },
      clicks_per_user: { $sum: 1 }
    }
  },

  // Average the clicks for each variant
  {
    $group: {
      _id: "$_id.variant",
      avg_clicks_per_user: { $avg: "$clicks_per_user" }
    }
  }
])

```

You should get something similar to this:

```
[  
    { _id: 'a', avg_clicks_per_user: 1 },
    { _id: 'b', avg_clicks_per_user: 1.5 }
]
```

### Upload your results to Brightspace

Run the experiment as above, making sure to generate enough data. Run the queries in mongosh and take a screenshot of your results showing average clicks per user between the variants.


## Using decorators to streamline your AB testing

You can define custom decorators to help you manage your A/B testing. This allows you to leverage common code to create many A/B experiments without having to modify the code too much every time.

You can read [https://realpython.com/primer-on-python-decorators/](https://realpython.com/primer-on-python-decorators/) to understand decorators more.

### Benefits of the decorator-based approach

The implementation in this branch uses decorators both on frontend (`@ab_test_frontend`) and backend (`@ab_test_monitor`) to handle A/B testing. In terms of functionality, it is equivalent to the original implementation with which you started the in-class demo. The differences are related to how the code is organized and how the different parts fit together:

1. **Modularity**: The A/B testing logic is encapsulated in **decorator** functions, keeping it separate from the core application logic. This makes the codebase cleaner and more maintainable.

2. **Separation of Concerns**: Related to modularity. The main functionality (like handling requests) remains untouched by A/B testing logic. The decorators handle variant assignment, cookie management, and recording experiment data without cluttering route handlers.

3. **Reusability**: The same decorators can be applied to any route in which you wish to introduce A/B testing.

4. **Scalability**: Related to **reusability**. Adding new experiments or variants is straightforward - apply the appropriate decorator to the relevant function and pass the experiment parameters.

5. **Easy to understand**: The code clearly indicates which functions are part of A/B tests through the decorator syntax, making it easier for developers to understand what's happening. That is, you don't have to go through the code logic to understand if something is a vital part of the application logic or if it is handling the A/B testing logic.

For example, in the frontend, the `@ab_test_frontend("landing_page", ["a", "b", "c"])` decorator automatically handles:
- Checking if the user has been assigned a variant
- Assigning a random variant if needed
- Passing the variant to the route handler
- Setting the appropriate cookie

Similarly, on the backend, the `@ab_test_monitor("landing_page")` decorator:
- Retrieves the session ID
- Gets the variant from cookies 
- Logs the relevant events

You can add A/B testing to your application with minimal changes to the original code.

### How do decorators work?

Think of a decorator as a wrapper or an envelope that surrounds a function. Just like an envelope can contain a letter but also add its own properties (like addresses or stamps), a decorator "wraps" around a function and can add behavior before and/or after the function runs.

For example, when the `@ab_test_frontend` decorator is applied to a route:

1. When someone visits that route, the decorator code runs first (like picking up the envelope)
2. The decorator can perform actions before the route handler runs (like reading instructions on the envelope)
3. Then the original route function is called (reading the actual letter)
4. After the route function completes, the decorator can perform more actions (like sealing the envelope again)
5. The decorator returns the response (sending the envelope)

This way, we can "inject" new behavior (here, it's A/B testing) around our existing code without changing it much. Thus, it is more modular and easier to maintain - very important aspects in software engineering!
