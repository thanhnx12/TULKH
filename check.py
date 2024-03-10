def calculate_objective_value(N, M, K, s, g, t, solution):
    objective_value = 0

    for k in range(K):
        # Tính tổng độ tương đồng giữa các đồ án trong cùng một hội đồng
        for i in range(N):
            for j in range(i + 1, N):
                if solution[i] == k and solution[j] == k:
                    objective_value += s[i][j]

        # Tính tổng độ tương đồng giữa đồ án và giáo viên trong cùng một hội đồng
        for i in range(N):
            for j in range(M):
                if solution[i] == k and t[i] != j and solution[N + j] == k:
                    objective_value += g[i][j]

    return objective_value

# Đọc input từ file input.txt
with open('input.txt', 'r') as file:
    ip = [int(x) for x in file.readline().split()]
    N, M, K = ip[0], ip[1], ip[2]
    ip = [int(x) for x in file.readline().split()]
    a, b, c, d, e, f = ip[0], ip[1], ip[2], ip[3], ip[4], ip[5]

    # Đọc ma trận s
    s = []
    for i in range(N):
        ip = [int(x) for x in file.readline().split()]
        s.append(ip)
    # Đọc ma trận g
    g = []
    for i in range(N):
        ip = [int(x) for x in file.readline().split()]
        g.append(ip)
    # Đọc danh sách t
    t = [int(x) - 1 for x in file.readline().split()]
    # Gọi hàm solve
    solution = solve(N, M, K, a, b, c, d, e, f, s, g, t)

# Tính giá trị hàm mục tiêu
objective_value = calculate_objective_value(N, M, K, s, g, t, solution)

# In giá trị hàm mục tiêu
print("Objective Value from Output:", objective_value)