a = [' p ', '123', '456']
start = [(i,j) for i, row in enumerate(a) for j, col in enumerate(row) if col == 'p'][0]
