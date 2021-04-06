You can fetch corrections scale with this script

Make sure you have this 2 env values before launching
```
API42_CLIENT='...'
API42_SECRET='...'
```

To have these credentials, you must create an application here https://profile.intra.42.fr/oauth/applications/new
And you can add them in your ~ / .zshrc file via export command (`export API42_CLIENT="CLIENT_TOKEN"`)

Standalone
You can start this script directly on your computer, to do that you must have `requests` & `inquirer` pip3 packages
Installation is done via this command
```
pip3 install -r requirements.txt
```

Launching via
```
python3 scale.py

OR

./scale.py
```

Docker
You simply need to launch a docker command
```
docker run -it --rm -e "API42_CLIENT=$API42_CLIENT" -e "API42_SECRET=$API42_SECRET" hexanyn/42-scale
```
