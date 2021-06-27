# Raspberry Pi Temp Monitor with Adafruit IO

This is an example Python script for creating a temperature and
humidity monitor with a Raspberry Pi, an Adafruit DHT22 sensor,
and the Adafruit IO service for data ingestion and reporting. 

SMS alerts can be easily set up with a $20 preloaded Twilio account
and a free Zapier account, but that is beyond the scope of this 
document.

## What you'll need

- Raspberry Pi (I used a RPi 3 Model B)
- Raspbian OS with Python 3
- AM2302/DHT22 sensor
- Probably some breadboard wires

## Hardware config

Install latest Raspbian to a SD card.

Find pinout for your Raspberry Pi. Attach + wire to 3.3v, - wire to GND, 
and the data wire to GPIO4 (or any other GPIO pin, you'll just need to
modify the script).

## Adafruit IO config

Create a free Adafruit IO account. Create four feeds: `temp`, `humidity`,
`apifailures`, `sensorfailures`. Feel free to create a dashboard around these
feeds to your liking. Also feel free to create Triggers if you desire,
again that is outside the scope of this document.

Take note of your username, and copy your API key from the My Key page.

## Script installation

Run the following commands to install the prerequisite libraries:
```
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT
sudo pip3 install adafruit-io
```

Clone this repo to `/home/pi/dev/tempsensor` (aka `~/dev/tempsensor`). 
Feel free to clone to a different path, you'll just need to update the 
`tempsensor.service` file respectively.

Modify the Python script if you've deviated from the instructions
above.

Run the following commands:
```
sudo cp ~/dev/tempsensor/tempsensor.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/tempsensor.service
chmod +x ~/dev/tempsensor/tempsensor.py
sudo systemctl daemon-reload
sudo systemctl enable tempsensor.service
```

Set the environment variables by running `sudo systemctl edit tempsensor`
and typing the following contents into the editor:
```
[Service]
Environment="ADAFRUIT_IO_KEY=aaaaa"
Environment="ADAFRUIT_IO_USERNAME=bbbbb"
```

Replace `aaaaa` with your IO key, and `bbbbb` with your IO username.

If the previous command launched nano to edit the file, press Ctrl+O then 
Enter to save the file, then Ctrl+X to exit. If it launched vim, then you 
probably already know how to exit vim.

Run the following command to start the service:
```
sudo systemctl start tempsensor.service
```

To check the logs and ensure it's working, run:
```
sudo journalctl -f -u tempsensor.service
```

A few seconds after starting, you should see temperature and humidity data
with no errors. This service is now set to run at startup.

If you see "Sensor reading failed!" you might have a bad connection to your
sensor, a bad sensor, or it plugged into the wrong pin.

If you see "Failed sending data!" you might have a bad internet connection,
incorrectly set API key/username, or some other issue with your IO account.
