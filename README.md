# collaging-machine
creates a collage out of jpegs in a specified folder 

It's not currently working as intended, but it generally prints an irregular collage of up to all the images in the folder (which needs to be exclusively filled with jpegs) - the path to which, you need to paste into 'ad' - which is the first thing you should see when you open it!

note that it doesn't resize - the ultimate aim is for the output to be potentially worthy of consideration for printing, so files might be big and take a while to load..

also note that get_pix() searches for ".DS_Store" and ignores this file. That the folder "coll" unavoidably contains such a file was discovered by trial and error, so I have no idea if others will encounter other such problematic files. So the equality should be replaced with a set to which other filenames can be added...

collage95.py is the one that's being updated, rather than collage96.py
