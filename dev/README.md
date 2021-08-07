## Geckordp Development

<br />

Glad to see you here. Typically, examples are easy to understand and to get an idea how to proceed with your own project.
For example let's say you would like to implement an actor from [here](https://github.com/mozilla/gecko-dev/tree/master/devtools/shared/specs).

Usually the methods and the related events in the source file are most of the time enough to implement an actor class.

However, since there's no documentation you have no idea what it's exactly doing or where the actor ID is derived from.
In order to bridge this knowledge-gap without fully understanding the geckodriver source code, I suggest capturing the required packets for your needs (in my opinion it's more straightforward and simpler).

Note: The shown commands may vary on different operating systems.

---

Prerequisites:

- preconfigured profile
- 2 independent Firefox instances
- Wireshark


---

1\. Clone & install project:
```
cd <your-repositories-path>
git clone https://github.com/reapler/geckordp
cd geckordp
python -m pip uninstall geckordp
python -m pip install -e $PWD
cd dev
```

---

2\. Create preconfigured profile:
```
python profile.py --new geckordp
```

---

3\. Start & configure Wireshark:

1. select loopback interface
2. add one of the filter below
 
```
# filter by port
tcp.port == 6000

# with actual json payload
tcp.port == 6000 && tcp.payload

# with payload and comments
tcp.port == 6000 && tcp.payload || frame.comment
```

---

4\. Start first Firefox instance:
```
firefox -new-instance -no-remote -new-window http://example.com/ -p geckordp --start-debugger-server 6000
```

---

5\. Start second Firefox instance:

1. ```firefox -new-instance -no-remote -new-window about:debugging#/setup```
2. select section "Network Location"
3. add **localhost:6000**
4. connect to first instance

<br></br>

After you have followed these steps, Wireshark should have captured a few packets between the two instances.
Now you can proceed as you wish and use the DevTools as you wanted.

A few comments here and there on the packets before you do an action should make it easier to analyze it later.

At the end of your recording session, you can export your packets and convert your '.pcapng' file to a more readable format with:
```
python converter.py -i my-captured-packets.pcapng
```
A new file 'my-captured-packets.log' is created in the same directory.

To preview a converted pcap dump, see [connect-navigate.log](https://github.com/reapler/geckordp/blob/master/dev/connect-navigate.log)

You can always ask the Mozilla developers on their [matrix](https://chat.mozilla.org)-[channels](https://wiki.mozilla.org/Matrix#Software_Development) or here in the [issue](https://github.com/reapler/geckordp/issues) section for help.