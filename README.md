# race-competitor-lookup
Some trail races use RunSignup to handle registrations and display the entrants list. The majority of trail ultras use UltraSignup for the same purpose. 
This is a Python script that will scrape the entrants list for a race that uses RunSignup then look up each participant on UltraSignup to get their 
UltraSignup rankings and number of races. Output a csv with all the data for obsessing over/further analysis in a spreadsheet. Just indulging the most competitive parts of my soul...

`beautifulsoup4` for scraping RunSignup, then relied on this very helpful stack overflow post (https://stackoverflow.com/questions/51755889/how-to-scrape-text-between-data-bind/51756041#51756041)
to figure out which URLs to use to access the JSON UltraSignup is using to display participant results (it's a "heavily dynamic" site). Lots of data cleanup on both ends, handling for different ways of combining multi-part names into first name/last name fields and some inexplicable variations in how UltraSignup formats its participant page URLs.

`participants.csv` is a sample output for the 2023 Miwok 100k.
