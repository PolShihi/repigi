import circle
import square
import os

figs = ['circle', 'square']
funcs = ['perimeter', 'area']
sizes = {
	'perimeter-circle' : 1,
	'area-circle' : 1,
	'perimeter-square' : 1,
	'area-square' : 1,
}

def calc(fig, func, size):
	assert fig in figs
	assert func in funcs

	result = eval(f'{fig}.{func}(*{size})')
	print(f'{func} of {fig} is {result}')

if __name__ == "__main__":
	func = os.environ.get('FUNC')
	fig = os.environ.get('FIG')
	size = list([int(os.environ.get('SIZE'))])
    
	while fig not in figs:
		fig = input(f"Enter figure name, avaliable are {figs}:\n")
	
	while func not in funcs:
		func = input(f"Enter function name, avaliable are {funcs}:\n")
	
	while len(size) != sizes.get(f"{func}-{fig}", 1):
		size = list(map(int, input("Input figure sizes separated by space, 1 for circle and square\n").split(' ')))
	
	calc(fig, func, size)



