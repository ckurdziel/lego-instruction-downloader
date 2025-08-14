# Lego Instruction Downloader
I have a ton of lego sets and all the instruction booklets take up a lot of space. I wanted to download all of them into PDF form. 

Lego doesn't have an easy API for this so we need to use the Brickset API (v3) to accomplish this.


## How to use
1. Create a text file ```sets.txt``` with all of your set numbers in it.
2. Modify ```lego-instruction-downloader.py``` to include your API key from Brickset (if you don't have an account, you'll need to create one and create an API key).
3. Run ```python3 lego-instruction-downloader.py```
4. The script will hit the Brickset API and return a list of instruction PDFs. It  will limit these to US PDFs only (typically these have v39 in the description) and then download and sort these into folders for each set.
