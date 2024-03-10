from ortools.sat.python import cp_model

def solve(N,M,K,a,b,c,d,e,f,s,g,t):
    model = cp_model.CpModel()
    #create variables
    x = {}
    for i in range(N):
        for j in range(K):
            x[i,j] = model.NewIntVar(0,1,f"x[{i},{j}]")
    y = {}
    for i in range(M):
        for j in range(K):
            y[i,j] = model.NewIntVar(0,1,f"y[{i},{j}]")
    # Create binary variables z to represent the product of x[i,k] and y[j,k]
    z = {}
    for i in range(N):
        for j in range(M):
            for k in range(K):
                z[i,j,k] = model.NewIntVar(0, 1, f"z[{i},{j},{k}]")
                model.AddMultiplicationEquality(z[i,j,k], [x[i,k], y[j,k]])
    # Create binary variables w to represent the product of x[i,k] and x[j,k]
    w = {}
    for i in range(N):
        for j in range(N):
            for k in range(K):
                w[i,j,k] = model.NewIntVar(0, 1, f"w[{i},{j},{k}]")
                model.AddMultiplicationEquality(w[i,j,k], [x[i,k], x[j,k]])
                    
                    
    #create constraints
    # 1 hội đồng chỉ chấp nhận từ a đến b đề tài
    for k in range(K):
        model.add_linear_constraint( linear_expr=cp_model.LinearExpr.sum([x[i,k] for i in range(N)]) , lb=a, ub=b)
    # 1 hội đồng có từ c đến d giáo viên
    for k in range(K):
        model.add_linear_constraint(linear_expr=cp_model.LinearExpr.sum([y[i,k] for i in range(M)]) , lb=c, ub=d)
    # 1 đề tài được nhiều nhất 1 hội đồng
    for i in range(N):
        model.add(cp_model.LinearExpr.Sum([x[i,j] for j in range(K)]) == 1)
    
    # 1 giáo viên vào nhiều nhất 1 hội đồng
    for i in range(M):
        model.add(cp_model.LinearExpr.Sum([y[i,j] for j in range(K)]) == 1)
    # giáo viên không ngồi hội đồng có sinh viên mình hướng dẫn
    for i in range(N):
        for k in range(K):
            model.add(x[i,k] + y[t[i],k] <= 1)
    # độ tương đồng đồ án trong 1 hội đồng >= e
    for k in range(K):
        for i in range(N):
            for j in range(N):
                if i != j:
                    model.add((2 - x[i,k] - x[j,k])*e + s[i][j] >= e)
    # độ tường đồng đồ án , giáo viên trong hội đồng phải >= f
    for k in range(K):
        for i in range(N):
            for j in range(M):
                model.add((2 - x[i,k] - y[j,k])*f + g[i][j] >= f)
               
    #create objective
    
    model.maximize(obj = cp_model.LinearExpr.sum(
        [cp_model.LinearExpr.sum([w[i,j,k]*s[i][j] for i in range(N) for j in range(N)]) 
         + cp_model.LinearExpr.sum([z[i,j,k]*g[i][j] for i in range(N) for j in range(M)])
         for k in range(K)]))  
    
    #create solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print(N)
        for i in range(N):
            for j in range(K):
                if solver.Value(x[i,j]) == 1:
                    print(j+1, end=" ")
                    break
        print()
        print(M)
        
        for i in range(M):
            for j in range(K):
                if solver.Value(y[i,j]) == 1:
                    print(j+1, end=" ")
        solver.Solve(model)
        
        #print('\n',solver.objective_value)
# if __name__ == '__main__':
#     ip = [int(x) for x in input().split()]
#     N,M,K = ip[0], ip[1], ip[2]
#     ip = [int(x) for x in input().split()]
#     a,b,c,d,e,f = ip[0], ip[1], ip[2], ip[3], ip[4], ip[5]  

#     #read matrix s 
#     s = []
#     for i in range(N):
#         ip = [int(x) for x in input().split()]
#         s.append(ip)
#     #read matrix g
#     g = []
#     for i in range(N):
#         ip = [int(x) for x in input().split()]
#         g.append(ip)
#     solve(N,M,K,a,b,c,d,e,f,s,g)
def calculate_objective(N,M,K,s,g,t,student,teacher):
    objective_value = 0
    for k in range(K):
        for i in range(N):
            for j in range(i + 1, N):
                if student[i] == k and student[j] == k:
                    objective_value += s[i][j]
        for i in range(N):
            for j in range(M):
                if student[i] == k and teacher[j] == k :
                    objective_value += g[i][j]
    return objective_value
if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        ip = [int(x) for x in file.readline().split()]
        N,M,K = ip[0], ip[1], ip[2]
        ip = [int(x) for x in file.readline().split()]
        a,b,c,d,e,f = ip[0], ip[1], ip[2], ip[3], ip[4], ip[5]  

        #read matrix s 
        s = []
        for i in range(N):
            ip = [int(x) for x in file.readline().split()]
            s.append(ip)
        #read matrix g
        g = []
        for i in range(N):
            ip = [int(x) for x in file.readline().split()]
            g.append(ip)
        # read list t
        t = [int(x)-1 for x in file.readline().split()]
        file.readline()
        student = [int(x) - 1 for x in file.readline().split()]
        file.readline()
        teacher = [int(x) - 1 for x in file.readline().split()]
        print(student, teacher)
        print(calculate_objective(N,M,K,s,g,t,student,teacher))
        # solve(N,M,K,a,b,c,d,e,f,s,g,t)
        
        print(N,M,K,a,b,c,d,e,f,s,g,t,student,teacher)

    