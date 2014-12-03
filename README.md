### Fantasy Buff

## Guide to Running/Deploying

To run locally, you need to install all the dependencies, preferably in a virtualenv,
 
 pip install requirements.txt
 
you need to setup a Postgres server (configuring in league/settings.py), then run all the migrations,
 
  python manage.py migrate
  
then 

  python manage.py runserver
  
Should start up the development server. Unfortunately, any user or league loading will not function because the 
development server uses a built in cache, even though the loading takes place on a Redis cache. So if you want the full 
app locally, you also need to install Redis and Foreman and then just run

  python manage.py collectstatic
  foreman start
  
This should probably all be in a Vagrant file but it's not.

## Guide to Running Tests

There are two totally independent test suites, the Django tests which are run the standard django way
  
  python manage.py tests
  
and the Karma tests which are run the standard Karma way

  karma start

## Guide to the Files

league/ is the main Django configuration.

static/ is all the static files, including all the Javascript/Coffeescript for the project.

static/js/app is most of the front-end code written by me for the app, as opposed to static/js/lib which is where
I put third party code.

staticfiles/ is where we put files when we run collectstatic. This is automatically run on Heroku. Locally, we need
to run it ourselves if we're using Foreman. If we're just using the development server, the files get served straight
from static/ anyway.

teams/ is the only Django app where all the models and views go and is the heart of the application. Most of the
scraping logic is between teams/scraper.py and teams/html_scrapes.py. Ideally the parsing/extraction all happens
in html_scrapes, the loading into models happens in league_loader, and this is coordinate by scraper, 
but unfortunately it's not perfectly separated yet.

teams/metrics is where the post-processing on all the stats we bring in happens and we generate the report cards etc.

teams/SqlStore, teams/FileBrowser, and management/commands/scrape.py (web scraper) are the three main data access 
objects to the scrapes. There is basically a get() interface for any given page that is provided by any of those 
objects, and there is a put() inteface for the pages that the SqlStore and the FileBrowser have. These interfaces
are just informally enforced via test, but it's useful because it simplifies doing things like moving the production
database into my local file system (easier to open up a page in Chrome to inspect), or run a mock-scrape against the
file system rather than the live ESPN site.


### Lots more to write in this README , documentation is very overdue for this project.

 