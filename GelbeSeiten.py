import urllib, sys, csv, time
from bs4 import BeautifulSoup

names = []
postal_addresses = []
phone_numbers = []


def get_information(soup):
    result_items = soup.findAll("div", {"class": "result-item"})
    for item in result_items:
        # names
        name = item.find("span", itemprop="name")
        names.append(name.next)

        # addresses
        address = item.find("p", {"class": "address"})
        postal_addresses.append(address.next)

        # phone numbers
        x = item.find("a", {"data-category": "Telefonnummer_result", "class": "dropdown-item"})
        if x:
            split = str(x.next).split(" ", 1)
            phone_numbers.append(split[1])
        else:
            phone_numbers.append("")


url = "https://www.herold.at/gelbe-seiten"
city = ""
url_end = "/was_"
searchparam = ""

for x in sys.argv:
    if sys.argv.index(x) == 0:
        continue
    if sys.argv.index(x) == 1:
        city = "/" + x
        url += city
        url += url_end
        continue
    url += x
    searchparam += x
    if sys.argv.index(x) == len(sys.argv) - 1:
        continue
    url += "-"
    searchparam += "_"

standard_url = url

index = 2

while True:
    breakall = False
    f = urllib.urlopen(url)
    myfile = f.read()
    soup = BeautifulSoup(myfile, 'html.parser')
    # if soup.findAll("div", id="noresult") is None:
    #     break
    bla = soup.findAll("h1")
    if bla is not None:
        for x in bla:
            if x.next.startswith("Hoppla!"):
                breakall = True
                break
        if (breakall):
            break
    print("scanning site no. " + str(index - 1))
    get_information(soup)
    url = standard_url + "/?page=" + str(index)
    index = index + 1

filename = "gelbe_seiten_" + searchparam + "_" + time.strftime("%Y-%m-%d_%HH-%MM-%SS") + ".csv"
print(filename)

with open(filename, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Name", "Address", "Phone number"])

    for i in range(0, len(names) - 1):
        spamwriter.writerow([unicode(names[i]).encode("utf-8"), unicode(postal_addresses[i]).encode("utf-8"),
                             unicode(phone_numbers[i]).encode("utf-8")])
