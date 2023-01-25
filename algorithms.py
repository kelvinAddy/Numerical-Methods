# Written by Kelvin Addy

"""This module contains a class with methods that implements some numerical methods algorithms"""
import numpy as np


class Algorithms:
    # .............Root solving algorithms..........
    def bisection_algorithm(self, f, a, b, y=0, margin=.00_001):
        ''' Bracketed approach of Root-finding with bisection method
        Parameters
        ----------
        f: callable, continuous function
        a: float, lower bound to be searched
        b: float, upper bound to be searched
        y: float, target value
        margin: float, margin of error in absolute term
        Returns
        -------
        A float c, where f(c) is within the margin of y
        '''
        count = 0
        if (lower := f(a)) > (upper := f(b)):
            a, b = b, a
            lower, upper = upper, lower

        assert y >= lower, f"y is smaller than the lower bound. {y} < {lower}"
        assert y <= upper, f"y is larger than the upper bound. {y} > {upper}"

        while 1:
            count += 1
            c = (a + b) / 2
            if abs((y_c := f(c)) - y) < margin:
                # found!
                return c, count
            elif y < y_c:
                b, upper = c, y_c
            else:
                a, lower = c, y_c

    def regula_falsi_algorithm(self, f, a, b, y=0, margin=.00_001):
        ''' Bracketed approach of Root-finding with regula-falsi method
        Parameters
        ----------
        f: callable, continuous function
        a: float, lower bound to be searched
        b: float, upper bound to be searched
        y: float, target value
        margin: float, margin of error in absolute term
        Returns
        -------
        A float c, where f(c) is within the margin of y
        '''
        count = 0
        if (lower := f(a)) > (upper := f(b)):
            a, b = b, a
            lower, upper = upper, lower

        assert y >= (lower := f(a)), f"y is smaller than the lower bound. {y} < {lower}"
        assert y <= (upper := f(b)), f"y is larger than the upper bound. {y} > {upper}"

        while 1:
            count += 1
            c = ((a * (upper - y)) - (b * (lower - y))) / (upper - lower)
            if abs((y_c := f(c)) - y) < margin:
                # found!
                return c, count
            elif y < y_c:
                b, upper = c, y_c
            else:
                a, lower = c, y_c

    def illinois_algorithm(self, f, a, b, y=0, margin=.00_001):
        ''' Bracketed approach of Root-finding with illinois method
        Parameters
        ----------
        f: callable, continuous function
        a: float, lower bound to be searched
        b: float, upper bound to be searched
        y: float, target value
        margin: float, margin of error in absolute term
        Returns
        -------
        A float c, where f(c) is within the margin of y
        '''
        if (lower := f(a)) > (upper := f(b)):
            a, b = b, a
            lower, upper = upper, lower
        assert y >= (lower := f(a)), f"y is smaller than the lower bound. {y} < {lower}"
        assert y <= (upper := f(b)), f"y is larger than the upper bound. {y} > {upper}"

        stagnant = 0
        count = 0
        while 1:
            count += 1
            c = ((a * (upper - y)) - (b * (lower - y))) / (upper - lower)
            if abs((y_c := f(c)) - y) < margin:
                # found!
                return c, count
            elif y < y_c:
                b, upper = c, y_c
                if stagnant == -1:
                    # Lower bound is stagnant!
                    lower += (y - lower) / 2
                stagnant = -1
            else:
                a, lower = c, y_c
                if stagnant == 1:
                    # Upper bound is stagnant!
                    upper -= (upper - y) / 2
                stagnant = 1

    def secant_algorithm(self, f, x_0, x_1, y=0, margin=.00_001):
        ''' Iterative approach of Root-finding with secant method
        Parameters
        ----------
        f: callable, continuous function
        x_0: float, initial seed
        x_1: float, initial seed
        y: float, target value
        margin: float, margin of error in absolute term
        Returns
        -------
        A float x_2, where f(x_2) is within the margin of y
        '''

        count = 0

        if abs((y_0 := f(x_0) - y)) < margin:
            # found!
            return x_0, count
        if abs((y_1 := f(x_1) - y)) < margin:
            # found!
            return x_1, count

        while True:
            count += 1
            x_2 = x_1 - y_1 * (x_1 - x_0) / (y_1 - y_0)
            if abs((y_2 := f(x_2) - y)) < margin or count > 2e6:
                # found!
                return x_2, count
            x_0, x_1 = x_1, x_2
            y_0, y_1 = y_1, y_2
        return x_2, count

    def steffensen_algorithm(self, f, x, y=0, margin=.00_001):
        ''' Iterative approach of Root-finding with steffensen's method
        Parameters
        ----------
        f: callable, continuous function
        x: float, initial seed
        y: float, target value
        margin: float, margin of error in absolute term
        Returns
        -------
        A float x_2, where f(x_2) is within the margin of y
        '''

        count = 0
        if abs((y_x := f(x) - y)) < margin:
            # found!
            return x, count

        while True:
            count += 1
            g = (f(x + y_x) - y) / y_x - 1
            if g * x == 0:
                # Division by zero, search stops
                return x, count
            x -= (f(x) - y) / (g * x)
            if abs((y_x := f(x) - y)) < margin or count > 2e6:
                # found!
                return x, count
        return x, count

    def newton_raphson(self, f, df, x_2, tolerance):
        ''' Iterative approach of Root-finding with the newton-raphson method
            Parameters
            ----------
            f: callable, continuous function
            f: callable, derivative of f
            x_2: float, initial seed
            tolerance: float, margin of error in absolute term
            Returns
            -------
            A float x_2, where f(x_2) is within the margin of y
        '''
        count = 0
        while True:
            count += 1
            if abs(y_x := f(x_2)) < tolerance or count > 2e6:
                return x_2, count

            x_2 = x_2 - f(x_2) / df(x_2)

    # .............Numerical integration algorithms..........
    def simpsons_3rd_rule(self, f, a, b, n):
        """
        Approximates the definite integral of a function f(x) over the interval [a, b]
        using Simpson's 1/3 rule.

        Parameters:
        f (function): The function to be integrated.
        a (float): The lower bound of the interval of integration.
        b (float): The upper bound of the interval of integration.
        n (int): The number of subintervals to use in the approximation.

        Returns:
        float: The approximate value of the definite integral of f(x) over the interval [a, b].
        """
        # Compute the width of each subinterval
        h = (b - a) / n

        # Initialize the sum
        integral = 0

        # Iterate over the subintervals
        for i in range(n + 1):
            # Compute the value of x at the current point
            x = a + i * h

            # Check if the current point is a starting, ending, or middle point
            if i == 0 or i == n:
                # If it's a starting or ending point, use a weight of 1
                weight = 1
            elif i % 2 == 0:
                # If it's an even-numbered middle point, use a weight of 2
                weight = 2
            else:
                # If it's an odd-numbered middle point, use a weight of 4
                weight = 4

            # Add the contribution from the current point to the sum
            integral += weight * f(x)

        # Return the approximation of the integral using Simpson's 1/3 rule
        return integral * h / 3

    def simpsons_8th_rule(self, f, a, b, n):
        """
        Approximates the definite integral of a function f(x) over the interval [a, b]
        using Simpson's 3/8 rule.

        Parameters:
        f (function): The function to be integrated.
        a (float): The lower bound of the interval of integration.
        b (float): The upper bound of the interval of integration.
        n (int): The number of subintervals to use in the approximation.

        Returns:
        float: The approximate value of the definite integral of f(x) over the interval [a, b].
        """
        # Compute the width of each subinterval
        h = (b - a) / n

        # Initialize the sum
        integral = 0

        # Iterate over the subintervals
        for i in range(n + 1):
            # Compute the value of x at the current point
            x = a + i * h

            # Check if the current point is a starting, ending, or middle point
            if i == 0 or i == n:
                # If it's a starting or ending point, use a weight of 1
                weight = 1
            elif (i - 1) % 3 == 0:
                # If it's a point one step away from the starting or ending point, use a weight of 3
                weight = 3
            else:
                # If it's a middle point, use a weight of 3
                weight = 3

            # Add the contribution from the current point to the sum
            integral += weight * f(x)

        # Return the approximation of the integral using Simpson's 3/8 rule
        return integral * 3 * h / 8

    def trapazoidal_rule(self, f, a, b, n):
        """Approximate the definite integral of f from a to b using the
        composite trapezoidal rule, with n intervals.

        Parameters
        ----------
        f : function
            The function to be integrated.
        a : float
            The lower limit of the integration.
            The upper limit of the integration.
        n : int
            The number of intervals to use.

        Returns
        -------
        float
            The approximate integral of f from a to b.
        """
        h = (b - a) / n
        s = 0.5 * (f(a) + f(b))
        for i in range(1, n):
            s += f(a + i * h)
        return h * s

    def monte_carlo(self, f, a, b, n):
        """Approximate the definite integral of f from a to b using the
        Monte Carlo method, with n samples.

        Parameters
        ----------
        f : function
            The function to be integrated.
        a : float
            The lower limit of the integration.
        b : float
            The upper limit of the integration.
        n : int
            The number of samples to use.

        Returns
        -------
        float
            The approximate integral of f from a to b.
        """
        s = 0
        for i in range(n):
            x = np.random.uniform(a, b)
            s += f(x)
        return (b - a) * s / n

    # .............Numerical optimization algorithms..........
    def golden_section_search(self, f, a, b, tol=1e-5):
        count = 0
        # Constants for the golden ratio
        gr = (1 + 5 ** 0.5) / 2
        # Calculate the distances between the points
        c = b - (b - a) / gr
        d = a + (b - a) / gr

        while abs(c - d) > tol or count > 2e6:
            count += 1
            # Evaluate the function at the points c and d
            fc = f(c)
            fd = f(d)

            if fc < fd:
                # Set b to the value of d and recalculate c
                b = d
                d = c
                c = b - (b - a) / gr
            else:
                # Set a to the value of c and recalculate d
                a = c
                c = d
                d = a + (b - a) / gr

        # Return the midpoint between a and b as the final result
        return (b + a) / 2, count

    def parabolic_interpolation(self, f, x1, x2, x3, epsilon=1e-6):
        count = 0
        while True:
            count += 1
            # Calculate the parabolic fit through the three points
            f1 = f(x1)
            f2 = f(x2)
            f3 = f(x3)
            A = (f1 * (x2 - x3) + f2 * (x3 - x1) + f3 * (x1 - x2)) / (
                    x1 * x1 * (x2 - x3) + x2 * x2 * (x3 - x1) + x3 * x3 * (x1 - x2))
            B = (f1 * (x2 * x2 - x3 * x3) + f2 * (x3 * x3 - x1 * x1) + f3 * (x1 * x1 - x2 * x2)) / (
                    x1 * (x2 - x3) * (x2 - x3) + x2 * (x3 - x1) * (x3 - x1) + x3 * (x1 - x2) * (x1 - x2))
            C = (f1 * (x3 * x3 * x3 - x2 * x2 * x2) + f2 * (x1 * x1 * x1 - x3 * x3 * x3) + f3 * (
                    x2 * x2 * x2 - x1 * x1 * x1)) / (
                        x1 * x1 * (x2 - x3) + x2 * x2 * (x3 - x1) + x3 * x3 * (x1 - x2))

            # Calculate the minimum of the parabolic fit
            xmin = -B / (2 * A)

            # Check if we have found a satisfactory minimum
            if abs(xmin - x2) < epsilon or count > 2e6:
                return xmin, count

            # Update the bounds for the next iteration
            if f(xmin) < f2:
                x3 = x2
                x2 = xmin
            else:
                x1 = x2
                x2 = xmin

    def newtons_method(self, df, dff, x_2, tolerance):
        ''' Iterative approach of Root-finding with the newton's method
            Parameters
            ----------
            f: callable, continuous function
            df: callable, first derivative of f
            dff: callable, second derivative of f
            x_2: float, initial seed
            tolerance: float, margin of error in absolute term
            Returns
            -------
            A float x_2, where x_2 is the approximate minimum of f
        '''
        count = 0
        while True:
            count += 1
            if abs(y_x := df(x_2)) < tolerance or count > 2e6:
                return x_2, count

            x_2 = x_2 - df(x_2) / dff(x_2)


if __name__ == "__main__":
    f = lambda x: x ** 3 - 81
    df = lambda x: 3*x**2
    dff = lambda x: 6 * x
    x = [0, 1, 2, 3]
    y = [0, 60, 120, 180]
    algo = Algorithms()