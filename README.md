# Overview

This branch shows how you can implement A/B testing using decorators.


## How to run the application

Run 

`docker compose up --build -d`

Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) on your browser, and make sure that you can add a student successfully (just to make sure that you can run the system).

Note how the UI you see for the landing page simply has "Student Management System" as the header (this is what we have been seeing all along in our demos). 

[Clear cookies from your browser](https://me-en.kaspersky.com/resource-center/preemptive-safety/how-to-clear-cache-and-cookies) (You can clear only the past hour), refresh the page and try again. You should still see the same message.


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

## Checking the results

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
