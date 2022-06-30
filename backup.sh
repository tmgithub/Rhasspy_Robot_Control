#! /bin/bash
rsync -rav /root/.config/rhasspy/profiles/de/intents /root/.config/rhasspy/profiles/de/raven/ /root/.config/rhasspy/profiles/de/slots/ /root/.config/rhasspy/profiles/de/profile.json /usr/local/intent/rhasspy
git add -A
git commit -m "Sync"
git pull
git push
