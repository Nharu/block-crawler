import requests
import sys
import csv

# Select which coin to archive
print()
print('select coin')
print('1: ethereum')
s = int(input('select: '))

if s == 1:
	print()
	print('select category')
	print('1: blocks')
	print('2: transactions')
	s = int(input('select: '))

	if s == 1:
		r = requests.get('https://api.blockchair.com/ethereum/blocks').json()
		lid = r['data'][0]['id']

		start = int(input('start block: '))
		end = int(input('end block(current last block#{0}): '.format(lid)))

		# error handling
		if start < 0:
			print('error')
			sys.exit(1)

		elif end > lid:
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

	elif s == 2:
		print()
		print('select option')
		print('1: set range with tx#')
		print('2: set range with block#')
		s = int(input('select: '))

		if s == 1:
			r = requests.get('https://api.blockchair.com/ethereum/transactions').json()
			lid = r['data'][0]['id']

			start = int(input('start tx: '))
			end = int(input('end tx(current last tx#{0}): '.format(lid)))

			# error handling
			if start < 0:
				print('error')
				sys.exit(1)

			elif end > lid:
				print('error')
				sys.exit(1)

			elif start > end:
				print('error')
				sys.exit(1)

			# open csv
			name = input('set csv file name: ')
			with open('{0}.csv'.format(name), 'w') as f:
				w = csv.writer(f)

				for i in range(start, end + 1):
					print('collecting tx#{0}'.format(i))
					b = requests.get('https://api.blockchair.com/ethereum/transactions?q=id({0})'.format(i)).json()
					bd = b['data'][0]

					if i == start:
						w.writerow(bd.keys())

					w.writerow(bd.values())

		elif s == 2:
			r = requests.get('https://api.blockchair.com/ethereum/blocks').json()
			lid = r['data'][0]['id']

			start = int(input('start block: '))
			end = int(input('end block(current last block#{0}): '.format(lid)))

			# error handling
			if start < 0:
				print('error')
				sys.exit(1)

			elif end > lid:
				print('error')
				sys.exit(1)

			elif start > end:
				print('error')
				sys.exit(1)

			# open csv
			name = input('set csv file name: ')
			with open('{0}.csv'.format(name), 'w') as f:
				w = csv.writer(f)

				for i in range(start, end + 1):
					print('collecting block#{0}'.format(i))
					b = requests.get('https://api.blockchair.com/ethereum/transactions?q=block_id({0})'.format(i)).json()
					bd = b['data']

					if i == start:
						w.writerow(bd[0].keys())

					for tx in bd:
						w.writerow(tx.values())

						
