# Home-AssistantConfig
## Indice
* [Installation Home Assistant](#Installation-Home-Assistant)
* [Addons base](#Addons-base)
* [HACS](#HACS)
* [RTL-SDR](#RTL-SDR)
* [MCP3008](#MCP3008)
* [API for host service](#API-for-host-service)
* [Ripristino](#Ripristino)


## Installation Home Assistant

### Docker
Installiamo i componenti di network
```bash
sudo apt-get install apt-transport-https ca-certificates curl avahi-daemon dbus -y
sudo apt-get install jq apparmor-utils socat software-properties-common -y
sudo apt-get install network-manager -y
```
Riavviamo
```bash
sudo reboot
```
Installiamo il docker deamon
```bash
curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo apt-key add -
echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install docker-ce -y
```

A questo punto dobbiamo perfezionare la configurazione. 
Modificheremo quindi il file “/boot/cmdline.txt“:
```bash
sudo nano /boot/cmdline.txt
```

Aggiungiamo la riga
```bash
cgroup_enable=memory cgroup_memory=1
```
Per impedire che ad ogni riavvio il mac adress dell'interfaccia wifi cambi, creiamo un nuovo file in
```bash
/etc/NetworkManager/conf.d/100-disable-wifi-mac-randomization.conf
```
Con contenuto
```bash
[connection]
wifi.mac-address-randomization=1
[device]
wifi.scan-rand-mac-address=no
```
Riavviamo
```bash
sudo reboot
```

Spegnamo se vogliamo l'uscita HDMI
```bash
sudo tvservice --off
```

### Hassio
Installiamo ora l'agente hassio che si occuperà di predisporre il sistema per il primo avvio
```bash
sudo -i
curl -sL https://raw.githubusercontent.com/home-assistant/hassio-installer/master/hassio_install.sh | bash -s -- -m raspberrypi3
```

## Addons base
### RedNode
```yaml
credential_secret: aaabbbbbcccddddeeeeffff
dark_mode: false
http_node:
  username: ''
  password: ''
http_static:
  username: ''
  password: ''
ssl: true
certfile: fullchain.pem
keyfile: privkey.pem
require_ssl: true
system_packages:
  - make
  - musl
  - g++
npm_packages:
  - node-red-contrib-home-assistant-websocket
  - node-red-contrib-moment
init_commands: []
```

### Samba Share
```yaml
workgroup: ''
username: aaaaa
password: bbbbb
interface: wlan0
allow_hosts:
  - 192.168.1.0/16
veto_files:
  - ._*
  - .DS_Store
  - Thumbs.db
  - icon?
  - .Trashes
compatibility_mode: false
```

### DuckDNS
```yaml
lets_encrypt:
  accept_terms: true
  certfile: fullchain.pem
  keyfile: privkey.pem
token: aaaa-bbbb-cccc-dddd
domains:
  - mrnight-home.duckdns.org
seconds: 300
```

### Mosquitto broker
```yaml
logins:
  - username: aaaa
    password: bbbb
anonymous: false
customize:
  active: false
  folder: mosquitto
certfile: fullchain.pem
keyfile: privkey.pem
require_certificate: false
```

### deCONZ
```yaml
device: >-
  /dev/serial/by-id/usb-dresden_elektronik_ingenieurtechnik_GmbH_ConBee_II_DE2147218-if00
vnc_password: aaaa
```

Backup DB
```bash
cd /usr/share/hassio/addons/data
sudo tar --exclude='core_deconz/otau/*' -zcvf complete_deconz.tar.gz core_deconz/
sudo chown pi:pi complete_deconz.tar.gz
sudo mv complete_deconz.tar.gz /home/pi
```

## HACS
Questo repository contiene una serie di moduli sviluppati dalla comunity ma non ancora ufficiali.
Per poterla attivare occorre andare in Impostazioni” > “Integrazioni” e premere su “+“. Cercare “HACS”.
Per attivare il modulo servirà un "GitHub Personal Access Token".

### Rednode extension
Per poter utilizzare il blocco ENTITY servirà attivare un'altro modulo: node-red-contrib-home-assistant-websocket.
Questo modulo può essere scaricato da HACS direttamente.

## RTL-SDR
### Modulo base
```bash
cd ~
sudo apt-get install git git-core cmake libusb-1.0-0-dev build-essential
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr/ && mkdir build && cd build/
cmake ../ -DINSTALL_UDEV_RULES=ON
sudo make
sudo make install
sudo ldconfig
cd ~
sudo cp ./rtl-sdr/rtl-sdr.rules /etc/udev/rules.d/
sudo reboot
# create file no-rtl.conf
sudo nano /etc/modprobe.d/no-rtl.conf
# add these three lines
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
sudo reboot
lsusb
rtl_test -t
```
### Modulo 433MHz
```bash
sudo apt-get install libtool libusb-1.0.0-dev librtlsdr-dev rtl-sdr doxygen
git clone https://github.com/merbanan/rtl_433.git
cd rtl_433/ && mkdir build &&
cd build && cmake ../ &&
make
sudo make install
Test installation:
rtl_433
```
### Modulo 1090Mhz
```bash
git clone git://github.com/MalcolmRobb/dump1090.git
cd dump1090
make
./dump1090 --interactive --net
```
Se il make vi restituisce un errore in compilazione verificare questo fix
https://github.com/joergsteinkamp/dump1090/commit/d219d463ef4b8793e1e41790853ee3dbf30e033c

### Installare mosquitto (sender)
```bash
sudo apt-get install mosquitto-clients
```

### Attivazione servizi
TO DO
creare file sh
creare file service 


## MCP3008
### Attiviamo interfaccia Hardware SPI
```bash
sudo raspi-config
```

### Connessione tra Raspberry e MCP3008

* MCP3008 VDD     to Raspberry Pi 3.3V
* MCP3008 VREF    to Raspberry Pi 3.3V
* MCP3008 AGND    to Raspberry Pi GND
* MCP3008 DGND    to Raspberry Pi GND
* MCP3008 CLK     to Raspberry Pi SCLK
* MCP3008 DOUT    to Raspberry Pi MISO
* MCP3008 DIN     to Raspberry Pi MOSI
* MCP3008 CS/SHDN to Raspberry Pi CE0

### Configurazione
```bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python setup.py install
```

## API for host service
### Installiamo Apache e il modulo cgi
```bash
sudo apt-get install apache2
sudo a2enmod cgi
```

Creiamo i file .cgi nelle folder 
```bash
/usr/lib/cgi-bin/
```
Ricordiamoci di dargi i privilegi di esecuzione
```bash
chmod +x .cgi
```

### Sicurezza
In /etc/apache2/ports.conf cambiamo la porta da 80 a 8083


Puliamo ogni file dalla cartella /var/www

Limitiamo le chiamate alle API dal solo localhost modificando il file
```bash
/etc/apache2/conf-enabled/serve-cgi-bin.conf
```
inserendo lo statment
```bash
Require local
```
abilitamo in visudo la possibilità di chiamare solo i servizi scelti
```bash
www-data ALL=(ALL) NOPASSWD: /bin/systemctl * sniffer-433.service, /bin/systemctl * sniffer-1090.service, /bin/systemctl * loop_analog.service, /bin/systemctl poweroff
```


## Ripristino
Il ripristino può essere effettuato in pochi passaggi:

1) Installare hassio

2) Copiare .storage in /usr/share/hassio/homeassistant.

    Questo file contiene tutti i settaggi di sicurezza, nonchè le password e i token.

    Non viene normalmente salvata su git e quindi serve crearne una copia manuale

3) Clonare repo nella folder /usr/share/hassio/homeassistant
```bash
sudo git initsudo git remote add origin https://github.com/lorerave85/Home-AssistantConfig.git
git fetch --all
git reset --hard origin/master
sudo git pull origin master
```

4) Copiare file secrets.yaml nella folder /usr/share/hassio/homeassistant

    Non viene normalmente salvata su git e quindi serve crearne una copia manuale.

    Copiare eventuali altri file (es: google tooken)

5) Disattivare per il momento i settaggi in https all'interno del file configuration.yaml fino a quando non si installa l'addons per duckdns

6) tutti i moduli custom e HACS sarà già disponibile in quanto contenuto nel repo git

### cgi
Rimuovere local dall'header del file

### service 
Rimuovere local dall'header del file
