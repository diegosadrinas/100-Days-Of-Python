This is code test for a Jr Python Developer position. The task is to create a script that takes an xml as an input and returns a json file with a series of element counters and results.

The main goal is to iterate over the xml file and count the total number of "hosts", "services", "web-sites", "web vulnerabilities" and "non web vulnerabilities". Also, it needs to create a dictionary with all the vulnerabilities detected in the xml file and their elements. Finally, once the script has to collected all the required information, it creates a json file from the list described above.

The implemented solution uses BeautifulSoup module in order to scrap the xml elements and make lists from needed selectors. Once the lists are created, a function eliminates the duplicates and returns the final count of each element. Finally, a list of dictionaries is created. I used the json built-in module in order to convert the dictionary into a json file.

The script uses the click library so it can parse the arguments once the user tries to run from the console. In order to make it work, the function takes two parameters: --input xmlfile --output jsonfile.

