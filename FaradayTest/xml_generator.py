from datetime import datetime
from lxml import etree
from typing import List
import click
import random


now_date = datetime.now()
protos = ["UDP", "TCP"]
states = ["open", "close"]


@click.command(help="Generate demo report")
@click.option("--filename", required=True, prompt=True)
@click.option("--hosts", required=True, prompt=True, type=click.IntRange(min=1))
@click.option("--services", required=True, prompt=True, type=click.IntRange(min=1))
@click.option("--vulns", required=True, prompt=True, type=click.IntRange(min=1))
def generate_xml_format(filename: str, hosts: int, services: int, vulns: int):
    root = etree.Element("MetasploitV4")
    create_tree = generate_xml(root, hosts, services, vulns)
    with open(filename, "wb") as file:
        file.write(create_tree)


def rand_id_tag() -> str:
    return str(random.choice(range(100, 1000)))


def rand_port() -> str:
    return str(random.choice(range(1, 65535)))


def date_formatted() -> str:
    return str(now_date.replace(second=0, microsecond=0))


def rand_proto() -> str:
    return random.choice(protos)


def rand_state() -> str:
    return random.choice(states)


def generate_xml(root: str, hosts: int, services: int, vulns: int) -> bytes:

    created_hosts: List[str] = []
    total_vulns = 0
    total_services = 0


    for _ in range(hosts):
        hosts_tag = etree.SubElement(root, "hosts")
        host_tag = etree.SubElement(hosts_tag, "host")
        host_id_tag = etree.SubElement(host_tag, "id")
        host_id_tag.text = rand_id_tag()

        host_created_at_tag = etree.SubElement(host_tag, "created_at")

        host_created_at_tag.text = date_formatted()

        host_address_tag = etree.SubElement(host_tag, "address")
        host_address_tag.text = ".".join(
            map(str, (random.randint(0, 255) for _ in range(4)))
        )
        if host_address_tag.text not in created_hosts:
            created_hosts.append(host_address_tag.text)

        host_mac_tag = etree.SubElement(host_tag, "mac")
        host_mac_tag.text = "%02x:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        host_name_tag = etree.SubElement(host_tag, "name")
        host_name_tag.text = ""

        os = ["Windows", "Mac", "Linux"]
        host_os_name_tag = etree.SubElement(host_tag, "os-name")
        host_os_name_tag.text = random.choice(os)

        host_updated_at_tag = etree.SubElement(host_tag, "updated-at")
        host_updated_at_tag.text = date_formatted()

        host_comments_tag = etree.SubElement(host_tag, "comments")
        host_comments_tag.text = ""

        host_vuln_count_tag = etree.SubElement(host_tag, "vuln-count")
        

        host_service_count_tag = etree.SubElement(host_tag, "service-count")

        etree.SubElement(host_tag, "comm")
        etree.SubElement(host_tag, "state")
        etree.SubElement(host_tag, "os-flavor")
        etree.SubElement(host_tag, "os-sp")
        etree.SubElement(host_tag, "os-lang")
        etree.SubElement(host_tag, "purpose")

        services_tag = etree.SubElement(host_tag, "services")

        vulns_tag = etree.SubElement(host_tag, "vulns")
        vuln_count = 0
        service_count = 0
        for _ in range(random.randint(1,services)):
            service_tag = etree.SubElement(services_tag, "service")

            service_id_tag = etree.SubElement(service_tag, "id")
            service_id_tag.text = rand_id_tag()

            service_created_at_tag = etree.SubElement(
                service_tag, "created_at"
            )
            service_created_at_tag.text = date_formatted()

            service_host_id_tag = etree.SubElement(service_tag, "host-id")
            service_host_id_tag.text = host_id_tag.text

            service_port_tag = etree.SubElement(service_tag, "port")
            service_port_tag.text = rand_port()

            service_proto_tag = etree.SubElement(service_tag, "proto")
            service_proto_tag.text = rand_proto()

            service_state_tag = etree.SubElement(service_tag, "state")
            service_state_tag.text = rand_state()

            service_name_tag = etree.SubElement(service_tag, "name")
            service_name_tag.text = "http"

            service_updated_at_tag = etree.SubElement(
                service_tag, "updated-at"
            )
            service_updated_at_tag.text = date_formatted()

            service_info_tag = etree.SubElement(service_tag, "info")
            service_info_tag.text = ""
            service_count += 1

            for _ in range(random.randint(1,vulns)):
                vuln_tag = etree.SubElement(vulns_tag, "vuln")

                vuln_id_tag = etree.SubElement(vuln_tag, "id")
                vuln_id_tag.text = rand_id_tag()

                vuln_host_id_tag = etree.SubElement(vuln_tag, "host-id")
                vuln_host_id_tag.text = host_id_tag.text
                vuln_service_id_tag = etree.SubElement(vuln_tag, "service-id")
                vuln_service_id_tag.text = service_id_tag.text
                vuln_web_site_id_tag = etree.SubElement(
                    vuln_tag, "web-site-id"
                )
                vuln_web_site_id_tag.text = service_id_tag.text

                vuln_name_tag = etree.SubElement(vuln_tag, "name")
                vuln_name_tag.text = f"vuln {rand_id_tag()}"

                vuln_info_tag = etree.SubElement(vuln_tag, "info")
                vuln_info_tag.text = f"description n: {rand_id_tag()}"
                etree.SubElement(vuln_tag, "refs")
                vuln_count += 1

        for _ in range(random.randint(1,vulns)):
            vuln_tag = etree.SubElement(vulns_tag, "vuln")

            vuln_id_tag = etree.SubElement(vuln_tag, "id")
            vuln_id_tag.text = rand_id_tag()

            vuln_host_id_tag = etree.SubElement(vuln_tag, "host-id")
            vuln_host_id_tag.text = host_id_tag.text
            
            vuln_name_tag = etree.SubElement(vuln_tag, "name")
            vuln_name_tag.text = f"vuln {rand_id_tag()}"

            vuln_info_tag = etree.SubElement(vuln_tag, "info")
            vuln_info_tag.text = f"description n: {rand_id_tag()}"
            etree.SubElement(vuln_tag, "refs")
            vuln_count+=1
        host_vuln_count_tag.text = str(vuln_count)
        host_service_count_tag.text = str(service_count)
        total_vulns += vuln_count
        total_services += service_count


    root_services_tag = etree.SubElement(root, "services")

    root_service_tag = etree.SubElement(root_services_tag, "service")

    root_id_tag = etree.SubElement(root_service_tag, "id")
    root_id_tag.text = rand_id_tag()

    root_created_at_tag = etree.SubElement(root_service_tag, "created-at")
    root_created_at_tag.text = date_formatted()

    root_host_id_tag = etree.SubElement(root_service_tag, "host-id")
    root_host_id_tag.text = rand_id_tag()

    root_port_tag = etree.SubElement(root_service_tag, "port")
    root_port_tag.text = rand_port()

    root_proto_tag = etree.SubElement(root_service_tag, "proto")
    root_proto_tag.text = rand_proto()

    root_state_tag = etree.SubElement(root_service_tag, "state")
    root_state_tag.text = rand_state()

    root_name_tag = etree.SubElement(root_service_tag, "name")
    root_name_tag.text = "http"

    root_updated_at_tag = etree.SubElement(root_service_tag, "updated-at")
    root_updated_at_tag.text = date_formatted()

    root_info_tag = etree.SubElement(root_service_tag, "info")
    root_info_tag.text = ""

    etree.SubElement(root, "web_sites")
    etree.SubElement(root, "web_vulns")

    create_tree = etree.tostring(root, pretty_print=True)
    print(f"Total vulns: {total_vulns}")



if __name__ == "__main__":
    generate_xml_format()
