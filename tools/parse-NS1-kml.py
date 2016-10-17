import sys

from bs4 import BeautifulSoup

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
with open(input_file_path, "r") as myfile:
    xml_str = myfile.read()

soup = BeautifulSoup(xml_str, "lxml")

placemarks = soup.find_all('placemark')
placemark_str_list = list()
for placemark in placemarks:
    hospital_name = placemark.find('name').text
    hospital_address = placemark.find('data', {"name": "地址"}).find('value').text
    hospital_phone = placemark.find('data', {"name": "電話"}).find('value').text
    placemark_str = "%s\t%s\t%s" % (hospital_name, hospital_address, hospital_phone)
    placemark_str_list.append(placemark_str)

output_str = '\n'.join(placemark_str_list)
with open(output_file_path, 'w') as myfile:
    myfile.write(output_str)
