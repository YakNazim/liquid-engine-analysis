# Simplex search

# Erin Schmidt

# for non-linear programming problems ala Nelder and Mead (1965)
# **Note** use Python3 for this script
import math as m
import numpy as np

def simplex_search(f, x_start, max_iter = 100, epsilon = 1E-6, gamma = 5, beta = 0.5):
    """
    parameters of the function:
    f is the function to be optimized, return a scalar, and operate over a numpy array with the same dimensions of x_start
    x_start (numpy array): initial position
    epsilon is the termination criteria
    gamma is the contraction coefficient
    beta is the expansion coefficient
    """
    
    # Init Arrays
    N = len(x_start) # Amount of Design Variables
    fnew = []        # Empty Function Matrix
    xnew = []        # Empty Re-write for Design Variables
    x = []           # Empty x Matrix
    
    # Generate vertices of initial simplex
    a = .75          # Step Size Alpha
    x0 = (x_start)   # x0 Value for x Matrix
    x1 = [x0 + [((N + 1)**0.5 + N - 1.)/(N + 1.)*a, 0.]]
    x2 = [x0 + [0., ((N + 1)**0.5 - 1.)/(N + 1.)*a]]
    x3 = [x0 - [0., ((N + 1)**0.5 - 1.)/(N + 1.)*a]]
    x4 = [x0 - [0., ((N + 1)**0.5 - 1.)/(N + 1.)*a]]
    x5 = [x0 - [0., ((N + 1)**0.5 - 1.)/(N + 1.)*a]]
    x = np.vstack((x1, x2, x3, x4, x5))
    print(x)

    # Simplex iteration
    while True:
        # Find best, worst and 2nd worst points --> new center point
        f_run = np.array([f(x[0]), f(x[1]), f(x[2])]).tolist() # Func. values at vertices
        #print(f_run)
        xw = x[f_run.index(sorted(f_run)[-1])] # Worst point
        xb = x[f_run.index(sorted(f_run)[0])]  # Best point
        xs = x[f_run.index(sorted(f_run)[-2])] # 2nd worst point
        xc = (xb + xs)/N                       # Center point  
        xr = 2*xc - xw                         # Reflection point
        
        # Check cases
        if f(xr) < f(xb):                      # Expansion
            xnew = (1 + gamma)*xc - gamma*xr
            # print('a', f(xr), f(xb))         # For debugging
        elif f(xr) > f(xw):                    # Contraction 1
            xnew = (1 - beta)*xc + beta*xw
            # print('b', f(xr), f(xw))
        elif f(xs) < f(xr) and f(xr) < f(xw):  # Contraction 2
            xnew = (1 + beta)*xc - beta*xw
            # print('c', f(xs), f(xr), f(xw))
        else:
            xnew = xr
        
        # Replace Vertices
        x[f_run.index(sorted(f_run)[-1])] = xnew
        # x[1] = xb
        # x[2] = xs
        fnew.append(f(xnew))
        # print('Current optimum = ', fnew[-1])
        
        # Break if any termination critera is satisfied
        if len(fnew) == max_iter or term_check(xb, xc, xs, xnew, N) <= epsilon:
            return f(x[f_run.index(sorted(f_run)[0])]), x[f_run.index(sorted(f_run)[0])], len(fnew)
        
def term_check(xb, xc, xs, xnew, N): # The termination critera
    return m.sqrt(((f(xb) - f(xc))**2 + (f(xnew) - f(xc))**2 + (f(xs) - f(xc))**2)/(N + 1))

# Testing
def f(x): # The pseudo-objective Function
    rp = 100
    x[0] = L
    x[1] = mdot
    x[2] = dia
    x[3] = p_e
    (L, dia, alt, v, a, t, F, D, Ma, rho, p_a, T_a, TWR, ex, Ve, A_t, dV1, m, S_crit, q, m_prop) = trajectory(L, mdot, dia, p_e) #change inputs to indices of x (e.g. design variables)
    obj_func = m[0] + rp*(max(0, (L+2)/(dia*0.0254) - 15)**2 + max(0, -TWR + 2)**2 + max(0, -S_crit + 0.35)**2 + max(0, -alt +100000)**2 + max(0, max(a)/9.81 - 15)**2)
    return obj_func

# Print results
(f, x, iter) = simplex_search(f, np.array([1.5, 0.453592 * 0.9 * 4, 8, 50]))
# print('\n')
print('f = ', f)
print('x = ', x)
print('iterations = ', iter)