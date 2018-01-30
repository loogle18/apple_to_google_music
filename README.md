## apple_to_google_music
**apple_to_google_music** is a library converter that allows you easily convert your
exported Apple Music songs list to Google Music.
It parses passed list of songs and add them to your Google Music library.

It also creates file with ignored tracks that were not found on Google Music library.
So You can check them out.

# Install common requirements
`pip3 install -r requirements.txt`

# Credentials configuration
Before using script be sure you have generated [app password](https://support.google.com/mail/answer/185833?hl=en) in your google account.

# Usage
`python3 apple_to_google_music.py -e ${EMAIL} -p ${APP_PASSWORD} -f ${PATH_TO_TXT_SONGS_LIST}`

Example:

`python3 apple_to_google_music.py -e "some.name@gmail.com" -p "dniandisand1a" -f "apple-music.txt"`
