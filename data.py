data = {0: {}, 1: {}, 2: {0: 0}, 3: {0: 0, 1: 5, 4: 2}, 4: {1: 2}}
edges_data = {}
for key in data:
	da = data[key]
	if not da:
		print 'null'
	else:
		for d in da:
			edges_data[key,d] = da[d]
print edges_data