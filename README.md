# Learn-Coding Server

## Run local

```bash
# download and install deps
git clone ...
cd .../server
pip install pipenv
pipenv install --dev 

# start pipenv shell and run the script
pipenv shell
python run_local.py

# or use pipenv directly
pipenv run python run_local.py

# or shortcut:
pipenv run serve
```


## Deployment

### Services

learn-coding-db:
`cf cs aws_dynamodb table learn-coding-db -c`

```json
{
  "Attributes":[
    {"Name":"id", "Type":"S"},
    {"Name":"version", "Type":"S"}
   ],
  "KeySchema":[
    {"Name":"id", "Type":"HASH"},
    {"Name":"version", "Type":"RANGE"}
  ],
  "BillingMode": "PAY_PER_REQUEST"
}
```

### Push

```
cf push
```


## Architecture

### Endpoints
```
GET /
-> Team input page
```

```
GET /teams/<team>
-> Editor page
```


### Code highlighting

Tutorial text is injected using Flask-Markdown with CodeHilite.
To apply the style, we include a generated `highlights.css` file.

> Generated with `pygmentize -S default -f html -a .codehilite > static/css/highlights.css`

Links:
* https://python-markdown.github.io/extensions/  
* https://python-markdown.github.io/extensions/code_hilite/

# Backlog

* [x] Load code at start from server
* [ ] Check local storage for code
* [x] Save code on 'Save'-clicked
* [x] Feedback while saving
* [x] Feedback after saving
* [x] Run code
* [ ] Stop code
* [ ] Claim team name
    * [ ] Lock code
    * [ ] Unlock code (for private editing)
* [x] Catch `[CMD] + S` to save code
* [ ] Add control elements (button, switch)
* [ ] Versioned
    * [ ] Save code versioned
    * [ ] Load code with latest version
    * [ ] Save timestamp with version
    * [ ] Show versions and load them
* [ ] Simulator 
    * [x] Add led simulator
    * [x] Connect API with simulator
    * [x] Implement length
    
* [x] Deployable to CF

## Bugs
* [x] Alignment of editor and tutorial text box 



## Tutorial
1. Move the light using the arrow keys
1. For `if` conditionals we need a `pixels.get(<index>)`
2. For more fun we need a `getRandomColor()` method
3. We need `pixels.length()`