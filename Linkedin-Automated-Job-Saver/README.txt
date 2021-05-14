This mini-project consists in an automated job application bot for Linkedin. The key here is, first of all, determine a the preferred filters for the kind of applications you want to appear as options. After defining those filters, just copy the url and the bot will be ready to start applying.

Remember to set your private info as "env" variables using the module of your choice. I personally like de python-decouple module for this, mainly because (as far as I know) it is the simplest and cleanest way to do it.

It seems that Linkedin is not that exigent in terms of detecting these kind of practices, which means that this script can be used on daily bases from an online IDE that admits scheduled executions (i.e. pythonanywhere)