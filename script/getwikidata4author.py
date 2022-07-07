import pandas as pd
import json
import re
import os
import urllib.request

def addwikidata2authorlist(authorlist_path,authordata_folder):
	df = pd.read_csv(authorlist_path,sep='\t')
	for index, row in df.iterrows():
		#urllib.request.urlretrieve("https://www.wikidata.org/wiki/Special:EntityData/"+row['wdid']+'.json', authordata_folder+os.sep+row['wdid']+'.json')
		with open(authordata_folder+os.sep+row['wdid']+'.json') as f:
			item = json.load(f)
		name = item['entities'][row['wdid']]['labels']['de']['value']
		gender = item['entities'][row['wdid']]['claims']['P21'][0]['mainsnak']['datavalue']['value']['id']
		if gender == "Q6581097":
			gender = "male"
		elif gender == "Q6581072":
			gender = "female"
		df.loc[index, 'name'] = name
		df.loc[index, 'gender'] = gender
		df.loc[index, 'birth'] = item['entities'][row['wdid']]['claims']['P569'][0]['mainsnak']['datavalue']['value']['time'][1:11]
		df.loc[index, 'death'] = item['entities'][row['wdid']]['claims']['P570'][0]['mainsnak']['datavalue']['value']['time'][1:11]
	df.sort_values(by=['birth']).to_csv(authorlist_path,sep='\t',index=False)

if __name__ == '__main__':
	authorlist_path = input('Path of author list (tsv): ')
	authordata_folder = input("Where to save authordata (json from wikidata): ")
	addwikidata2authorlist(authorlist_path,authordata_folder)