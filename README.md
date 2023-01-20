# Quore Daily Check-ins
Software to manage daily developer check-ins at Quore


# Installation

Python3/Node.js required. Clone the repository

	git clone https://github.com/connorgannaway/HuddleBot
	cd HuddleBot

## Backend

From project root, create and activate a virtual environment.

    python -m venv venv
    ./venv/Scripts/activate

Install packages

    pip install -r requirements

Copy `.env` file (contains secret key) to /backend.

Create database

    cd backend
    backend/> python manage.py migrate

Run backend server

    backend/> python manage.py runserver

### Note for deployment:

**[backend/backend/settings.py]**: *CORS_ALLOWED_ORIGINS will need the frontend webserver address added. ALLOWED_HOSTS will need the backend url path added. DEBUG needs to be set to false. DATABASES will need to be changed for non-sqlite3 applications.* [MORE INFO](https://docs.djangoproject.com/en/4.0/howto/deployment/)

To run:

    backend/> gunicorn backend.wsgi

## Frontend

From project root, cd into the frontend folder and install modules

    cd frontend
    npm install

Run dev server

    npm run dev

Build frontend

    npm run build

## Endpoints

### Frontend

    person/
    daily/

**person/** is a form to add a new user to the database. 

**daily/** is the form for daily check-ins, requiring a query parameter `uuid`

### Backend

    api/person/ - POST
    api/person/<int:pk>/ - GET
    api/check-in/uuid/ - GET/POST 
    api/check-in/<str:uuid>/ - GET/PATCH
    
    api/token/ - GET
    api/assignment/ - POST
    api/statuschange/ - POST
    
**api/person/** is the endpoint to add a new person to the database.

**api/person/*int:pk*/** will return person info for specified primary key

**api/check-in/uuid/** deals with check-in uuids.
 A GET request with query param `date` will return a list of related `user` and `check_in_uuid` objects for that date.

 A POST request with post data `create: True` will create check-in entries for all active users for the current date, and return the equivalent of the GET request. All fields are left null except `uuid`, `user`, and `date`. 

*(Note: `date` contains the day the entry is for, and `submitted_at` is when the user actually submitted their form.) Fields are TZ-aware and in UTC. This can be changed in backend/backend/settings.py*

**api/check-in/*str:uuid*/** interacts directly with the check-in entry matching the uuid in the url. A GET request will return the db entry, and a PATCH request will update the entry. `submitted_at` is autofilled on PATCH.

**api/token/** with query param `service` will return the current *slack* or *jira* API token.

**api/assignment/** is the destination for the Jira assignment change webhook. It requires a Jira issue in the standard *Jira Issue Format*.

**api/statuschange/** is the destination for the Jira status change webhook. It requires a Jira issue in the standard *Jira Issue Format*, as well as  `old_status` and `new_status` query parameters. Acceptable statuses are: `to_do`, `in_progress`, `testing`, and `done`.


## Altering DB entries

All DB entries can be modified in the Django Admin site at the `admin/` endpoint of the backend server. To access, you will need an admin account.

    python manage.py createsuperuser

## Setting up Jira Webhooks

1. From your Jira site, go to: Settings > System > Global Automation.
2. Create a new rule titled "Assignments" with *"Issue assigned"* as the trigger and *"Send web request"* as the action.
3. Set the web request URL to the **api/assignment/** endpoint, and the body to *"Issue Data (Jira Format)"*. Save.
4. Create another rule for the To Do to In Progress transition with *"Issue transitioned"* as the trigger. Set "From status" to *"To Do"* and the "To status" to *"In Progress"*.
5. Set the action to *"Send web request"*.
6. Set the web request URL to the **api/statuschange/** endpoint, and the body to *"Issue Data (Jira Format)"*.
7. Set `old_status` and `new_status` query params (url) to *"to_do"* and *"in_progress"*. Save.
8. Repeat 4-7 for the remaining issue transitions. *Note: all "in progress" and "testing" kanban categories should be grouped into one "in_progress" and "testing" status. e.g. there should not be a rule firing for an issue transitioning from one testing category to another.*

To make development easier, you can easily create a tunnel for the backend server and set the web request urls to the other end of that tunnel using [ngrok](https://ngrok.com/download).

    ngrok http --host-header=rewrite <backendport>

## OAuth Authentication & Bot Creation

### Slack

Create a slack app on [api.slack.com](https://api.slack.com) with `channels:join`, `chat:write`, `im:write`, `users:read` as bot scopes. Then, use the "Install App" page to install your slack app to your workspace. Copy your Bot User OAuth Token (starts with xoxb-) and enter it to the api_token database table (/admin).

### Jira

1. From [developer.atlassian.com](https://developer.atlassian.com), enter the developer console from the settings dropdown.
2. Create an app using OAuth2
3. Go to permissions and configure Jira API
4. Add classic scopes `read:jira-work`, `read:jira-user` as scopes
5. Go to authorization and configue OAuth2
6. Set the callback url to any url. This is only used to grab url params when redirected.
7. Copy the generated url and paste into a new tab
8. Change `state=${value}` to `state={a random string}`
9. Add `%20offline_access` after the last scope, but before other parameters
10. Hit enter and follow the prompts. When redirected, copy the Auth Code attached to the redirected url.

**Exchange the authorization code for access token:**

    curl --request POST \
      --url 'https://auth.atlassian.com/oauth/token' \
      --header 'Content-Type: application/json' \
      --data '{"grant_type": "authorization_code","client_id": "YOUR_CLIENT_ID","client_secret": "YOUR_CLIENT_SECRET","code": "YOUR_AUTHORIZATION_CODE","redirect_uri": "https://YOUR_APP_CALLBACK_URL"}'

- Save the access_token and refresh_token response in the api_token database table (/admin)
- In `/backend`, add `JIRA_CLIENT` and `JIRA_SECRET` (found in Jira App Settings) to the `.env` file. You will not be able to regenerate access tokens without this.

**Get the `cloudid` for your site**

Using your current access token (only valid for 1hr), make the following request

    curl --request GET \
      --url https://api.atlassian.com/oauth/token/accessible-resources \
      --header 'Authorization: Bearer ACCESS_TOKEN' \
      --header 'Accept: application/json'

Copy the appropriate `id` response. Save this as `VITE_CLOUD_ID` in a new `.env` file located in `/frontend`.

