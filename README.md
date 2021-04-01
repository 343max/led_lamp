I built a LED lamp as described [here](https://www.control-led.de/init/default/show_post/14/Python-RaspberryPi/Adressierung-von-LED-Strips-mit-dem-Raspberry-Pi-Zero)

This is my code, please modify it.

Installation:
```
sudo pip3 install -r requirements.txt
```

run it:
```
sudo python3 server.py
```

(sudo is neccessary as it won't be able to talk to the GPIO otherwise)

List of supported scenes:
```
curl http://lamp.local:8080/list
```

Select a scene:
```
curl --data "" http://lamp.local:8080/starry_night
```