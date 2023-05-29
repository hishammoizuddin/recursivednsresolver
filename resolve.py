"""
resolve.py: a recursive resolver built using dnspython
"""

import argparse

import dns.message
import dns.name
import dns.query
import dns.rdata
import dns.rdataclass
import dns.rdatatype

FORMATS = (("CNAME", "{alias} is an alias for {name}"),
           ("A", "{name} has address {address}"),
           ("AAAA", "{name} has IPv6 address {address}"),
           ("MX", "{name} mail is handled by {preference} {exchange}"))

# current as of 21 Oct 2022
ROOT_SERVERS = ("198.41.0.4",
                "199.9.14.201",
                "192.33.4.12",
                "199.7.91.13",
                "192.203.230.10",
                "192.5.5.241",
                "192.112.36.4",
                "198.97.190.53",
                "192.36.148.17",
                "192.58.128.30",
                "193.0.14.129",
                "199.7.83.42",
                "202.12.27.33")


def collect_results(name: str) -> dict:
    """
    This function parses final answers into the proper data structure that
    print_results requires. The main work is done within the `lookup` function.
    """
    full_response = {}
    target_name = dns.name.from_text(name)
    # lookup CNAME
    response = lookup(target_name, dns.rdatatype.CNAME)
    cnames = []
    for answers in response.answer:
        for answer in answers:
            cnames.append({"name": answer, "alias": name})
    # lookup A
    response = lookup(target_name, dns.rdatatype.A)
    arecords = []
    for answers in response.answer:
        a_name = answers.name
        for answer in answers:
            if answer.rdtype == 1:  # A record
                arecords.append({"name": a_name, "address": str(answer)})
    # lookup AAAA
    response = lookup(target_name, dns.rdatatype.AAAA)
    aaaarecords = []
    for answers in response.answer:
        aaaa_name = answers.name
        for answer in answers:
            if answer.rdtype == 28:  # AAAA record
                aaaarecords.append({"name": aaaa_name, "address": str(answer)})
    # lookup MX
    response = lookup(target_name, dns.rdatatype.MX)
    mxrecords = []
    for answers in response.answer:
        mx_name = answers.name
        for answer in answers:
            if answer.rdtype == 15:  # MX record
                mxrecords.append({"name": mx_name,
                                  "preference": answer.preference,
                                  "exchange": str(answer.exchange)})

    full_response["CNAME"] = cnames
    full_response["A"] = arecords
    full_response["AAAA"] = aaaarecords
    full_response["MX"] = mxrecords

    return full_response


def lookup(target_name: dns.name.Name,
           qtype: dns.rdata.Rdata) -> dns.message.Message:
    """
    This function uses a recursive resolver to find the relevant answer to the
    query.
    """
    servers_to_query = list(ROOT_SERVERS)  # storing in a list to traverse

    # querying until answer found or all servers checked
    while servers_to_query:
        server = servers_to_query.pop(0)

        for s in [server]:
            outbound_query = dns.message.make_query(target_name, qtype)
            response = dns.query.udp(outbound_query, s, 3)

        if response is None:
            continue

        if response.answer:
            # Checking for CNAME if answer found
            cname_response = None
            for a in response.answer:
                for answer in a:
                    if answer.rdtype == dns.rdatatype.CNAME:
                        cname_target = answer.target
                        # recursive call to lookup() with CNAME
                        cname_response = lookup(cname_target, qtype)

            if cname_response:
                # combining old response and cname_response for output
                response.answer.extend(cname_response.answer)

            return response

        next_servers = []  # additional servers from response
        if response.additional:
            for record in response.additional:
                if record[0].rdtype == dns.rdatatype.A:
                    next_servers.append(str(record[0]))

        if not next_servers:
            # check in response.authority if no next_servers found
            for authority in response.authority:
                if authority[0].rdtype != dns.rdatatype.SOA:
                    next_target_name = str(authority[0])
                    # recursive call to lookup() with next_target_name
                    next_response = lookup(
                        dns.name.from_text(next_target_name), dns.rdatatype.A)
                    if next_response:
                        for answer in next_response.answer:
                            if answer.rdtype == dns.rdatatype.A:
                                servers_to_query.append(str(answer[0]))
        else:
            # assign to be queried if additional servers found
            servers_to_query = next_servers

    return response


def print_results(results: dict) -> None:
    """
    take the results of a `lookup` and print them to the screen like the host
    program would.
    """

    for rtype, fmt_str in FORMATS:
        for result in results.get(rtype, []):
            print(fmt_str.format(**result))


def main():
    """
    if run from the command line, take args and call
    printresults(lookup(hostname))
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("name", nargs="+",
                                 help="DNS name(s) to look up")
    argument_parser.add_argument("-v", "--verbose",
                                 help="increase output verbosity",
                                 action="store_true")
    program_args = argument_parser.parse_args()
    for a_domain_name in program_args.name:
        print_results(collect_results(a_domain_name))


if __name__ == "__main__":
    main()
