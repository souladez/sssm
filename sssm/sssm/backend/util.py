from functools import wraps

def validate_stock(*param):
    def stock_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """ func wrapper """
            
            if len(args) == 0:
                raise ValueError("SSSM - {}: [ERROR] No parameters provided.".format(param[0]))
                
            if not isinstance(args[1], str):
                raise ValueError("SSSM - {}: [ERROR] Invalid Symbol {} specified.".format(param[0], args[1]))
            
            if not args[0].store['stocks'].get(args[1]):
                raise ValueError("SSSM - {}: [ERROR] Stock doesn't exist in database.".format(param[0])) 
            
            if len(args) > 2 and type(args[2]) != float:
                raise ValueError("SSSM - {}: [ERROR] Invalid Price {} specified.".format(param[0], args[2]))
                
            return func(*args, **kwargs)
        return wrapper
    return stock_decorator