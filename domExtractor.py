import sys
import subprocess


def extract_subdomains(input_domain, amass_output):
    subdomains = []
    for line in amass_output.split('\n'):
        if input_domain in line:
            parts = line.split()
            for part in parts:
                if part != input_domain and part.endswith(input_domain):
                        subdomains.append(part)
    return subdomains 

main_domain = sys.argv[1]
output_file_tmp = "amass_passive_"+main_domain+"_tmp.txt"
# amass enum -passive -d owasp.org


with open(output_file_tmp, "w") as output_file:
    try:
        subprocess.run(["amass", "enum", "-passive", "-d", sys.argv[1]], stdout=output_file, timeout=120)
    except subprocess.TimeoutExpired:
        print("Command timed out. Continuing with the script...")

with open(output_file_tmp, "r") as output_file:
    amass_output = output_file.read()

# Extract subdomains
result = extract_subdomains(main_domain, amass_output)

result_file_path = "amass_passive.txt"
# Write result to a new file
with open(result_file_path, "w") as result_file:
    for subdomain in result:
        result_file.write(subdomain + '\n')



# # Example usage:
# main_domain = sys.argv[1]
# amass_output = """
# example.com (FQDN) --> ns_record --> a.iana-servers.net (FQDN)
# example.com (FQDN) --> ns_record --> b.iana-servers.net (FQDN)
# example.com (FQDN) --> a_record --> 93.184.216.34 (IPAddress)
# example.com (FQDN) --> aaaa_record --> 2606:2800:220:1:248:1893:25c8:1946 (IPAddress)
# google.com (FQDN) --> ns_record --> ns3.google.com (FQDN)
# google.com (FQDN) --> ns_record --> ns4.google.com (FQDN)
# google.com (FQDN) --> ns_record --> ns1.google.com (FQDN)
# google.com (FQDN) --> ns_record --> ns2.google.com (FQDN)
# google.com (FQDN) --> mx_record --> smtp.google.com (FQDN)
# google.com (FQDN) --> node --> ns3.google.com (FQDN)
# google.com (FQDN) --> node --> ns4.google.com (FQDN)
# google.com (FQDN) --> node --> ns1.google.com (FQDN)
# google.com (FQDN) --> node --> ns2.google.com (FQDN)
# google.com (FQDN) --> node --> smtp.google.com (FQDN)
# google.com (FQDN) --> a_record --> 142.250.201.78 (IPAddress)
# google.com (FQDN) --> aaaa_record --> 2a00:1450:401b:80e::200e (IPAddress)
# www.example.com (FQDN) --> a_record --> 93.184.216.34 (IPAddress)
# www.example.com (FQDN) --> aaaa_record --> 2606:2800:220:1:248:1893:25c8:1946 (IPAddress)
# google.com (FQDN) --> node --> uberproxy.l.google.com (FQDN)
# google.com (FQDN) --> a_record --> 142.250.200.110 (IPAddress)
# google.com (FQDN) --> aaaa_record --> 2a00:1450:4003:80e::200e (IPAddress)
# google.com (FQDN) --> node --> rr1---sn-q4fl6nd6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr1.sn-q4fl6nd6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> google-proxy-74-125-213-99.google.com (FQDN)
# google.com (FQDN) --> node --> google-proxy-74-125-213-102.google.com (FQDN)
# google.com (FQDN) --> node --> rr4---sn-a5mlrnl6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4.sn-a5mlrnl6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr1---sn-q4fzene7.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr1.sn-q4fzene7.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr2---sn-a5mlrnll.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr2.sn-a5mlrnll.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr5---sn-q4fzene7.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr5.sn-q4fzene7.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4---sn-q4fl6n6r.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4.sn-q4fl6n6r.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4---sn-hp57kndz.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4.sn-hp57kndz.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4---sn-a5m7lnl6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rr4.sn-a5m7lnl6.c.drive.google.com (FQDN)
# google.com (FQDN) --> node --> rate-limited-proxy-66-249-87-193.google.com (FQDN)
# google.com (FQDN) --> node --> planocoreservices.rr3---sn-q4flrney.c.drive.google.com (FQDN)                                                                                      
# google.com (FQDN) --> node --> planocoreservices.rr3.sn-q4flrney.c.drive.google.com (FQDN)                                                                                        
# google.com (FQDN) --> node --> redirector.c.pack.google.com (FQDN)
# google.com (FQDN) --> node --> alt-144004.dns-staging.corp.google.com (FQDN)
# google.com (FQDN) --> node --> alt-131005.dos.corp.google.com (FQDN)
# rr1---sn-q4fl6nd6.c.drive.google.com (FQDN) --> cname_record --> rr1.sn-q4fl6nd6.c.drive.google.com (FQDN)                                                                        """

# result = extract_subdomains(main_domain, amass_output)
# print("Subdomains originating from", main_domain, ":", result)
