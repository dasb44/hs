import requests, json, argparse

# parameterize the model year if you want
honda_invent = "https://automobiles.honda.com/platform/api/v3/inventoryAndDealers?productDivisionCode=A&modelYear=2021&modelGroup=civic-type-r&zipCode={zipcode}&maxDealers=20"

class dealer:
    def __init__(self, number, name, address, city, state, zipcode):
        self.number = number
        self.name = name
        self.address = address
        self.city=city
        self.state=state
        self.zipcode = zipcode


class typer:
    def __init__(self, dealernumber, color, dle, onsite):
        self.dealernumber = dealernumber
        self.color = color
        self.dle = dle
        self.onsite = onsite
    
    def __str__(self):
        return "Dealer: %s || %s || %s || %s" % (self.dle.name, self.color, self.dle.zipcode, self.onsite)

dealer_dic = {}
typer_list = []

# right now we just input a file with zip codes
# TODO: programmatically get all zip codes since they are static
def read_zipcode(filename):
    with open(filename) as f:
        zip_c = f.read().splitlines()
    return zip_c
    
def load_and_parse(zipcode):
    honda_url = honda_invent.format(zipcode=zipcode)
    resp = requests.get(honda_url)
    result = resp.json()
    result.pop('filters', None)

    for dle in result['dealers']:
        d = dealer(dle['DealerNumber'], dle['Name'], dle['Address'], dle['City'], dle['State'], dle['ZipCode'][0:5])
        dealer_dic[dle['DealerNumber']] = d

    for invt in result['inventory']:
        t = typer(invt['DealerNumber'],invt['ExteriorColor'], dealer_dic[invt['DealerNumber']], invt['NumberOnSite'])
        typer_list.append(t)
    
    # now sort the list based on zip code
    typer_list.sort(key=lambda x : abs(94536 - int(x.dle.zipcode)))


def main():
    parser = argparse.ArgumentParser(description='Honda inventory search.')
    parser.add_argument('-f', '--file', required=True, type=str, help='file which contains the zip codes')
    args = parser.parse_args()
    zipcodes = read_zipcode(args.file)
    for z in zipcodes:
        load_and_parse(z)
    
    for t in typer_list:
        print(t)
        

main()