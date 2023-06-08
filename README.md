# CoRal

Webapp for data collection

## Guide

Note that this is a quick guide to get you started and there might be a few errors. In that case or if any generel questions, feel free to create issues on this github repo and I will try to fix / help you.

Note, you should definetly use chrome or firefox!

### Requirements

* django which can be installed through pip or conda

### Getting started

* Run python manage.py migrate --run-syncdb (this will create the db)
* (optional) Run python manage.py createsuperuser (super user if you want to access the admin side / monitoring)
* Run python manage.py runserver (this will launch the wepapp on port <http://127.0.0.1:8000/>

### Audio files

The audio files are saved in .webm format. If i remember correctly, then they are saved as mono files with 44100kHz. So you may use e.g. ffmpeg to convert them to .wav files afterwards. I think `ffmpeg -y -i file.webm -acodec pcm_s16le -ac 1 -ar 16000 -f wav file.wav` will do the trick and if you are a linux/mac user, then you can do a bash forloop for the directory with the sound files to convert all the files at the same time.

### Database and extraction

The relation between the audiofile names and the transcriptions is stored in a simple sqllite database. After you're done recording, you need to extract the information from the database using sql scripts or by dumping the database to your preferred format using django (python manage.py dumpdata > db.json). Further preprocessing might be required depending on how you wish to use the data.

### Admin page

Go to <http://127.0.0.1:8000/admin> and login with your superuser to get an overview of what has been recorded.

### Modifying presented text in the webapp

To modify the presented text, edit the `CoRal_webapp/audio_files/transcriptions.txt` file. The text presented in the webapp is randomly sampled from that file.
