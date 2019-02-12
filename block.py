import requests
import sys
import csv

# Select which coin to archive
print('select coin')
print('1: ethereum')
s0 = int(input('select: '))

if s0 == 1:
	print('select category')
	print('1: blocks')
	s1 = int(input('select: '))

	if s1 == 1:
		r = requests.get('https://api.blockchair.com/ethereum/blocks').json()
		id = r['data'][0]['id']

		start = int(input('start block: '))
		end = int(input('end block(current last block#{0}): '.format(id)))

		# error handling
		if start < 0:
			print('error')
			sys.exit(1)

		elif end > id:
			print('error')
			sys.exit(1)

		elif start > end:
			print('error')
			sys.exit(1)

		# open csv
		name = input('set csv file name: ')
		with open('{0}.csv'.format(name), 'w') as f:
			w = csv.writer(f)

			for i in range(start,end+1):
				print('collecting block#{0}'.format(i))
				b = requests.get('https://api.blockchair.com/ethereum/blocks?q=id({0})'.format(i)).json()
				bd = b['data'][0]

				if i == start:
					w.writerow(bd.keys())

				w.writerow(bd.values())




