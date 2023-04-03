import csv

# define the input file name
input_file = 'IOB.csv'

# define the output file name
output_file = 'output.csv'

# define the keys to extract
keys = ['date_recorded','sea_water_temperature_c', 'salinity', 'ph', 'dissolved_oxygen']

# open the input and output file
with open(input_file, 'r') as csv_file, open(output_file, 'w', newline='') as output:
    # read the csv file
    reader = csv.reader(csv_file)
    # write the output file
    writer = csv.writer(output)
    # write the header row
    writer.writerow(keys)
    # loop through each row

    i = 0
    for row in reader:
        
        if(i == 0):
            
            i+=1
            continue

        # if(1==i):
        #     print(row)
        #     i+=1

            
            
        # extract the values for the keys
        values = []
        
        
        
        try:
            date = row[0].split("+")[0]

            sea = row[1].split(":")[1]
            sea = float(sea[:len(sea)-1].replace('\'',
                        '').replace("\"", "").strip())

            salinity = row[2].split(":")[1]
            salinity = float(
                salinity[:len(salinity)-1].replace('\'', '').replace("\"", "").strip())

            
            
            ph = row[3].split(":")[1]
            ph= ph.replace("\"","").replace("}","").replace("'","")
            ph = float(ph)

            oxy = row[4].split(":")[1]
            oxy= oxy.replace("\"","").replace("}","").replace("'","").replace("]","")
            
            values = [date,sea, salinity, ph, oxy]
            
            writer.writerow(values)
        except:
            print("Incorrectly formatted row")
