def hyperelipsoid(x) -> float:
    """
    Calculate the hyperelipsoid function value for a given input vector x.
    
    The hyperelipsoid function is defined as:
        f(x) = sum(i * (x[i] ** 2)) for i in range(1, n+1)
    
    where n is the dimension of the input vector x.
    
    Args:
        x (list or np.ndarray): Input vector of shape (n,).
        
    Returns:
        float: The hyperelipsoid function value.
    """
    N = len(x)

    return sum(x[j] ** 2 
        for i in range(N) 
        for j in range(i))

#jak cos to przenioslem implementacje funckji do backend.models.fitness (mozesz przeniesc gdzies indziej)