import xml.etree.ElementTree as ET
import re
import urllib.request

def textgrid2txt(textgrid_id,txt_path):
	urllib.request.urlretrieve("https://textgridlab.org/1.0/aggregator/teicorpus/textgrid:"+textgrid_id, textgrid_id+'.xml')
	tree = ET.parse(textgrid_id+'.xml')
	root = tree.getroot()
	ns = '{http://www.tei-c.org/ns/1.0}'
	with open(txt_path,'w') as f:
		for text in root.iter(ns+'text'):
			f.write(ET.tostring(text, encoding='utf-8', method='text').decode('utf-8')+'\n')

	with open (txt_path, 'r' ) as f:
		content = f.read()
		content = re.sub(r'^\s+', '', content)
		content = re.sub(r'([^ ]) \n', r'\1 ', content)
		content = re.sub(r'\n ([^ ])', r' \1', content)
		content = re.sub(r'\n +', '\n', content)
		content = re.sub(r'\n{3,}', '\n\n', content)
	with open (txt_path, 'w' ) as f:
		f.write(content)

if __name__ == '__main__':
	textgrid_id = input('TextGrid ID (e.g. k5d3.0 for \"Die Kronenwächter\" by Achim von Arnim): ')
	txt_path = input("Path of output txt file (TextGrid ID.txt if empty): ")
	if txt_path.strip() == "":
		txt_path = textgrid_id+'.txt'
	textgrid2txt(textgrid_id,txt_path)