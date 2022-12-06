data = """"""

# First solution
print(sum((1 if (x0 <= x1 and y0 >= y1) or (x1 <= x0 and y1 >= y0) else 0 for x0, y0, x1, y1 in (([*map(int, (*j[0].split("-"), *j[1].split("-")))] for j in (i.split(",") for i in data.split("\n")))))))

# Second solution
print(sum(1 if any(map(lambda z: z[0] <= z[1] <= z[2], ((x0, x1, y0), (x0, y1, y0), (x1, x0, y1), (x1, y0, y1)))) else 0 for x0, y0, x1, y1 in (([*map(int, (*j[0].split("-"), *j[1].split("-")))] for j in (i.split(",") for i in data.split("\n"))))))
