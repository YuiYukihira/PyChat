# PyChat
A TCP chat using python

This program allows people to chat over a LAN connection, currently, WAN support might be possible through port forwarding the server, but has not been tested.

The server can be run without any modification, however, the client requires its code to be opened and the ip of the server to be supplied manually

yes, it is full of bugs at the moment as we used tkinter for the client, which has a limiting factor of requiring workarounds to allow for scrollbars to be used on labels, so we are thinking of either having the program cull the chatlog to fit it in place, or attempt to recreate the gui in a gui creating software

25/9/15:
We have edited the code so that the client just removes the earlier lines so the messages do not force the user to extend the chat so they can see them, if we do have the abilty to add a scrollar we will likely add it.
