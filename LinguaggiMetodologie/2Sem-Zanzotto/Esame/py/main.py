def applicaFunz(listaFunc, coppieNum):
	out = []
	templist = []
	i = 0
	for f in listaFunc:
		templist = []
		for coppia in coppieNum:
			res = f(coppia[0], coppia[1])
			templist.append(res)
		out.append(templist)

	return out


print(applicaFunz([lambda x, y: x + y, lambda x, y: x * y, lambda x, y: x - y], [(1, 2), (2, 3), (3, 4)]))
