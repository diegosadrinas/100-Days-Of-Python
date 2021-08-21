import json
from bs4 import BeautifulSoup
import click


# checks for duplicates and returns the count without them
def unique_elements_count(array):
    new_set = set(array)
    set_count = len(new_set)
    return set_count


# gets the text content of every selected element and removes the nulls (empty strings) to avoid miscounting
def get_content(array):
    new_array = [element.getText() for element in array if element.getText()]
    return new_array


# scraps the given element and returns a count without duplicates
def scrap_and_count_element(array):
    elements_list = get_content(array)
    unique_count = unique_elements_count(elements_list)
    return unique_count


# checks for empty string elements and turns them to none -null in json-
def replace_empty_for_none(array):
    for a_dict in array:
        for key, value in a_dict.items():
            if value == '':
                a_dict[key] = None
    return array


# takes an xml file and returns a json file with the given requirements
@click.command()
@click.option("--input", required=True)
@click.option("--output", required=True)
def xml_count_to_json(input: str, output: str):
    with open(input) as file:
        file_content = file.read()
        soup = BeautifulSoup(file_content, "lxml")

        hosts = soup.select("hosts")
        hosts_count = scrap_and_count_element(hosts)

        services = soup.select("host services service id")
        services_count = scrap_and_count_element(services)

        websites = soup.select("web_sites")
        websites_count = scrap_and_count_element(websites)

        web_vulns = soup.select("web_vulns")
        vulns_web_count = scrap_and_count_element(web_vulns)

        vulns_not_web = soup.select("host vuln-count")
        vulns_list = get_content(vulns_not_web)
        vulns_not_web_count = sum([int(i) for i in vulns_list])

        vulns = soup.select("host vulns vuln")
        vulns_dict = []

        for item in vulns:
            new_dict = {"ID": int(item.select_one("id").getText()),
                        "Host-id": int(item.select_one("host-id").getText()),
                        "name": item.select_one("name").getText(),
                        "info": item.select_one("info").getText(),
                        "refs": item.select_one("refs").getText(),
                        }
            vulns_dict.append(new_dict)

        lista_con_vulns = replace_empty_for_none(vulns_dict)

        final_dict = {
            "hosts_count": hosts_count,
            "services_count": services_count,
            "website_count": websites_count,
            "web_vulns_count": vulns_web_count,
            "vulns_count": vulns_not_web_count,
            "vulns": lista_con_vulns
        }

        json_text = json.dumps(final_dict)
        with open(output, "w") as json_file:
            json_file.write(json_text)
            return


if __name__ == "__main__":
    xml_count_to_json()