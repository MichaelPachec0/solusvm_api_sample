# Racknerd VPS API sample (SolusVM backend) README

[![License: MIT](https://img.shields.io/badge/License-MIT-important.svg)](https://opensource.org/licenses/MIT)

## Description

This was created because I was not able to find any information on how to access the api that was afforded by the SolusVM software. I am posting in the hope that anyone that needs it can find an easy way to access the api (without having to use php). In order to use this script you need to already have a key and hash, both of these will be generated once you enable API access in the SolusVM
control panel (under the API tab). The client api is rudimentary but allows for actions like reboot/boot/shutdown and to retrieve status information like how much disk/bandwidth/memory is being used. This sample focuses on status information, the other functions are much easier to code once the code flow is understood.

### Racknerd specific configuration

The SolusVM documentation (furthermore referred as documentation, [link here](https://documentation.solusvm.com/display/DOCS/Functions)) specifies that you need to point this to a <MASTER IP> (on port 5656). Racknerd support gave me an IP (withheld in case it changes and/or they do not wish to have it be public) to point to but curl complains about the certificate mismatch (i.e. the cert used does
not have a reference for the IP). I eventually understood that you can just point it to the url (in the case of racknerd: https://nerdvm.racknerd.com), and it works perfectly. No port is needed to be specified (the documentation refers to connect on port 5656) so depending on your VPS provider this might change.

#### Script specific limitations

As specified earlier, multiple data points can be retrieved from the api. One of the options (ram) does not currently provide meaningful data (it responds with 0.0's). Another data point (disk space) does not output disk used correctly (always 0.0's at least from what was observed). I do not know if its a configuration problem on Racknerd's end or a bug in the SolusVM software, or a limitation in
the way its implemented, but it is disabled by default in the script. Its pretty clear how it is disabled and if your VPS provider provides meaningful memory information it should be easy to enable in the script.

## Usage

Clone the repository and create a text file named tokens.txt, and insert your key and the sha1 hash provided from the control panel in that order and followed by a newline.

```text
ABCED-EFGHI-JKLMO
0a4d55a8d778e5022fab701977c5d840bbc486d0
```

There is also a settings.txt file that can be used to run as a loop, and furthermore to change the sleep timeout (in minutes)

## License

This project uses the MIT License. More info about this license can be found at https://opensource.org/licenses/MIT