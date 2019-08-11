import test
import os
import json
import time

previous = []


with open('test_file.txt', 'a') as f:

	previous = []
	while(True):

		x = test.commence_search([""],"", '')
		ids = []
		for item in x:
			ids.append(item['id'])

		for item in x:
			if (item['id'] in previous):
				break
			else:
				l = item
		
				id_ = l['id']
				try:
					l['certNum'] = test.get_cert_number(test.get_image(id_))
					if (len(l['certNum']) != 1):
						continue
				except:
					continue

				json.dump(l, f)
				f.write(os.linesep)

		previous = ids
		

		time.sleep(300)

