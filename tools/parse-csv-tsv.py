import sys
import csv

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
with open(input_file_path, "r") as myfile:
    soup = csv.reader(myfile, delimiter=',')

    placemark_str_list = list()
    for row in soup:
        hospital_name = row[1]
        hospital_address = "台南市" + ''.join(row[2:5])
        hospital_phone = row[5]
        placemark_str = "%s\t%s\t%s" % (hospital_name, hospital_address, hospital_phone)
        placemark_str_list.append(placemark_str)

    output_str = '\n'.join(placemark_str_list)
    with open(output_file_path, 'w') as myfile:
        myfile.write(output_str)
