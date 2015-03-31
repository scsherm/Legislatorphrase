import requests
import csv
import yaml

phrase = input("Got a phrase?") #User input for phrase
query_params = { 'apikey': 'f6ab5f2e4f69444b9f2c0a44d9a5223d',
		   		 'phrase': phrase,
                         'sort': 'count desc'
                         } #Query parameters for capitol words

endpoint = 'http://capitolwords.org/api/phrases/legislator.json' #API endpoint
response = requests.get(endpoint, params=query_params).json()
response = response['results'] #Remove the results index

with open("legislators.yaml", "r") as file: #Open legislators.yaml file as file
    legislators = yaml.load(file) #Load file with yaml func into legislators
    
    phrase = phrase + ".csv" #Add .csv to input phrase to write file
    with open(phrase, "w") as csvfile: #Open file to write
        writer = csv.writer(csvfile)
        writer.writerow(['count', 'legislator', 'state', 'party', 'gender'])

        for n in response:
            for i in range(len(legislators)):
                if legislators[i]['id']['bioguide'] == n['legislator']: #Match bioguide id
                    count = n['count'] #Count for phrase
                    legislator = legislators[i]['name']['official_full'] #Name for bioguide id
                    noterms = len(legislators[i]['terms']) - 1 #Get latest term
                    state = legislators[i]['terms'][noterms]['state']
                    party = legislators[i]['terms'][noterms]['party']
                    gender = legislators[i]['bio']['gender']
                    writer.writerow([count, legislator, state, party, gender])
