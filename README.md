First foray in to python here, so I'm not sure how much setup is required on your local environment. The project uses the [Flask framework](http://flask.pocoo.org/); you may need to consult the install docs there if you run in to trouble. SQLite 3.x is required.

Assuming you have virtualenv installed, you should be able to run the code with the following. These commands assume you've cloned this repo and are working in that directory.

`. env/bin/activate`
`python uber.py`

At this point, pop open a browser of your choice and check out http://localhost:5000. Note that there is a Quicktime video in this repo that shows how the app _should_ behave in case these instructions aren't sufficient to get the code running locally.

Known issues: Main python script could benefit from a healthy dose of DRY-ing; HTML/CSS interface is pretty barebones; no validation for inputs; have not tested/implemented fallbacks when JS disabled; hitting 'edit' on an item inserts form multiple times, etc.