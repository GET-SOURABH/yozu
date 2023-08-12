from django.shortcuts import render, HttpResponse

import math
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import random
import linecache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .modules.calculations import *




# Create your views here.
def index(request):
    return HttpResponse("this is home-page")

def cal(request):
    return HttpResponse("here you go")


@csrf_exempt
def evaluate_math(request):
    pi = 3.14
    if request.method == 'POST':

        # taking user input
        user_input = request.POST.get("question", "")
        user_input = str(user_input).lower()

        try:
            solution = (eval(user_input))   # example: 2 + 3 * 4 (any expression) (trigonometry functions not working)
            solution = str(solution)

            # plot
            plt.figure(figsize=(8, 1))
            plt.axhline(y=0, color='black', linewidth=2)
            plt.scatter(int(solution), 0, color='red', s=100, label=f'Number: {int(solution)}')
            plt.xlabel('Number Line')
            plt.yticks([])
            plt.legend()
            plt.savefig("output.jpg")

            #output
            return JsonResponse({"answer": solution}) # 14

        except:
            try:                        # example: (5 * x + 4 = 14)   if the question is an equation
                symbol_dict = {}
                for i in user_input:
                    if i.isalpha():
                        symbol_dict[i] = sp.Symbol(i)
                symbol_list = list(symbol_dict.values())
                variable = symbol_list[0]

                lhs, rhs = user_input.split("=")
                lhs_expr = sp.sympify(lhs)
                rhs_expr = sp.sympify(rhs)
                equation1 = sp.Add(lhs_expr, -rhs_expr)
                solution = sp.solve(equation1, variable)

                # plot
                lhs, rhs = user_input.split("=")
                lhs_expr = sp.sympify(lhs)
                rhs_expr = sp.sympify(rhs)
                equation1 = sp.Add(lhs_expr, -rhs_expr)

                def equation(x):
                    return eval(str(equation1))

                x_values = np.linspace(-10, 10, 100)
                y_values = equation(x_values)

                plt.plot(x_values, y_values, label=user_input)
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title(f'Equation Plot: {user_input}')
                plt.legend()
                plt.grid(True)
                plt.savefig("output.jpg")

                #output
                return JsonResponse({"answer": str(solution[0])}) # 2



            except:
                try:                                #example: (x**2 + 2*x -15) if the question is quadratic equation
                    expr = user_input
                    for i in expr:
                        if i.isalpha():
                            variable = sp.Symbol(i)
                    roots = sp.solve(expr, variable)

                    x = sp.Symbol('x')
                    equation = sp.sympify(expr)
                    coefficients_dict = sp.collect(equation, x, evaluate=False)

                    # Fetch the coefficients
                    a = coefficients_dict[x ** 2]
                    b = coefficients_dict[x]
                    c = coefficients_dict[1]

                    print_str = ''
                    print_str += "STEP1: To calculate discriminant: b^2 - 4ac"
                    discriminant = b ** 2 - 4 * a * c
                    print_str += (f"discriminant: {discriminant}\n")

                    # Step 2: Check if the discriminant is positive, negative, or zero
                    if discriminant > 0:
                        print_str += ("STEP2: Since the discriminant is positive, there are two distinct real roots.\n")
                    elif discriminant < 0:
                        print_str += ("STEP2: since the discriminant is negative,there are no real roots")
                    elif discriminant == 0:
                        print_str += ("STEP2: since the discriminant is equal to zero, there is one repeated real root.\n")

                    print_str += ("STEP3: Root1: (-b + sqrt(discriminant)) / (2*a)   and   Root2: (-b - sqrt(discriminant)) / (2*a)")

                    if roots != []:
                        print_str += "roots are:"
                        roots_str = list(map(str, roots))

                        #output
                        return JsonResponse({"answer": roots_str})

                    else:
                        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                        root1 = str(root1)
                        root2 = str(root2)
                        both_roots = root1 + root2

                        #plot
                        equation1 = user_input
                        x = sp.Symbol('x')
                        polynomial = sp.Poly(equation1, x)
                        coefficients = polynomial.all_coeffs()
                        a, b, c = coefficients
                        x = np.linspace(-10, 10, 100)
                        y = a * x ** 2 + b * x + c
                        plt.plot(x, y)
                        plt.xlabel('x-axis')
                        plt.ylabel('y-axis')
                        plt.title('Given Quadratic Equation')
                        plt.grid(True)
                        plt.savefig("output.jpg")

                        #output
                        return JsonResponse({"answer": both_roots}) # "answer": ["-5","3"]

                except:
                    pass
                    # try:          # if any problem occurs then these will manage
                    #     import os
                    #     import openai as openai
                    #     openai.api_key = '----'
                    #
                    #     input_question = user_input
                    #     completion = openai.ChatCompletion.create(
                    #         model="gpt-3.5-turbo",
                    #         messages=[
                    #             {"role": "user", "content": input_question},
                    #             {"role": "system","content": "you accept mathematics questions and give step-wise solution for the asked question."}
                    #         ]
                    #     )
                    #
                    #     symbol = completion.choices[0].message.content
                    #
                    #     #output
                    #     return JsonResponse({"answer": str(symbol)})
                    # except:
                    #     pass




@csrf_exempt
def category(request):

    if request.method == 'POST':

        #input
        user_input = request.POST.get("question", "")   # example:(x**2 + 2*x -15)  any question
        user_input = str(user_input).lower()

        l = user_input.split(" ")
        category_list = []

        # equation type
        alpha_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if 'x**3' in l or 'y**3' in l or 'x^3' in l or 'y^3' in l:
            category_list.append("Cubic Equation")
        elif 'x**2' in l or 'y**2' in l or 'x^2' in l or 'y^2' in l:
            category_list.append("Quadratic Equation")
        else:
            for i in alpha_letters:
                if i in l:
                    category_list.append("Polynomial Equation")

        # Number System
        number_system_key = ['number', 'numeral', '+', '-', '/', '*', 'numeration', 'place_value', 'compare',
                             "Natural_Numbers",
                             "natural", "whole", "integers", "rational", "irrational", "place", "face", "expanded",
                             "roman", "number", "estimation", "fractions", "decimal", "equivalent", "simplification",
                             "addition", 'add', "subtraction", "multiplication", "division", "operations",
                             "terminating",
                             "non-terminating", "remainder", "line", "conversion", "exponents", "power", "square",
                             "cube", "real",
                             "laws", "rationalizing", "euclid's", "hcf", "lcm", 'pow', "euclidean", "fundamental"]

        for i in number_system_key:
            if i in l:
                category_list.append("number system")
            else:
                pass

        # Algebra
        algebra_key = ['algebra', 'expression', 'equation', "=", "algebraic", "expression", "equation", "variable",
                       "constant", "coefficient", "linear", "quadratic", "**", "polynomial", "factor", "identity", 'root',
                       "simultaneous", "inequality", "algebra", "formula", "exponent", 'log', "binomial", "trinomial",
                       "equation", "simplification", "graph", "system"]

        for i in algebra_key:
            if i in l:
                category_list.append("algebra")
            else:
                pass

        # Mensuration
        mensuration_key = ['geometry', 'shape', 'area', 'perimeter', 'volume', "area", "perimeter", "rectangle",
                           "square", "triangle", "hypotenuse", "circle", "parallelogram", "rhombus", "trapezium",
                           "quadrilateral", "polygon",
                           "volume", "cylinder", "cone", "sphere", "cube", "cuboid", "pyramid", "hemisphere", "surface",
                           "base",
                           "height", "radius", "diameter", "perpendicular", "diagonal", "isometric", "net", "height",
                           "lateral", "surface", "right", "angled", "equilateral", "isosceles", "scalene", "obtuse",
                           "acute", "right-angled", "similar", "congruent", "prism", "composite",
                           "regular", "irregular", "symmetry", "axis", "point", "centroid", "circumcenter", "incenter",
                           "orthocenter", "area", "perimeter"]

        for i in mensuration_key:
            if i in l:
                category_list.append("mensuration")
            else:
                pass

        # Statistics and Probability

        stat_prob_key = ['data', 'graph', 'chart', 'mean', 'median', 'mode', 'probability', 'chance', 'likely',
                         'unlikely',
                         "data", "mean", "median", "mode", "range", "frequency", "bar", "chart", "pie", "graph",
                         "probability",
                         "experiment", "outcomes", "sample", "event", "likely", "unlikely", "fair", "biased", "tree",
                         "diagram", "combinations", "permutations", "random", "variable", "independent",
                         "dependent", "expected", "ratio", "odds", "experimental", "theoretical", "trials", "success",
                         "failure", "mutually", "exclusive", "complementary", "union", "intersection",
                         "outcome", "probability", "distribution", "range", "mode", "mean", "median", "variance",
                         "standard",
                         "deviation", "percentile", "correlation", "regression", "sample", "population", "confidence",
                         "interval", "hypothesis", "test"]

        for i in stat_prob_key:
            if i in l:
                category_list.append("statistics and probability")
            else:
                pass

        # Trigonometry
        trigonometry_key = ['trigonometry', "sin", "cos", "tan", "cot", "sec", "cosec", 'angle', 'triangle', 'sine',
                            'cosine', 'tangent',
                            "angle", "degree", "radian", "triangle", "right", "acute", "obtuse", "opposite",
                            "adjacent", "sine", "cosine", "tangent", "cotangent", "secant",
                            "cosecant", "pythagorean", "trigonometric", "identity", "solving", "equations",
                            "trigonometric", "ratios", "trigonometric", "functions", "angle", "measurements",
                            "angle", "sum", "difference", "multiple", "division", "values", "unit", "circle", "solving",
                            "problems"]

        for i in trigonometry_key:
            if i in l:
                category_list.append('trigonometry')
            else:
                pass

        category_list = set(category_list)
        print_str = "the following question involves: "

        # output
        return JsonResponse({"statement": print_str ,"answer": str(category_list)})   # "the following question involves: ",  "{'Quadratic Equation', 'number system'}"


def real_life_examples(request):

    if request.method == 'POST':

        # input
        user_input = request.POST.get("question", "")   #example: (x + 12 = 20) any question
        user_input = str(user_input).lower()

        import random
        import linecache
        l = user_input.split(" ")
        category_list = []

        # equation type
        alpha_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if 'x**3' in l or 'y**3' in l or 'x^3' in l or 'y^3' in l:
            category_list.append("Cubic Equation")
        elif 'x**2' in l or 'y**2' in l or 'x^2' in l or 'y^2' in l:
            category_list.append("Quadratic Equation")
        else:
            for i in alpha_letters:
                if i in l:
                    category_list.append("Polynomial Equation")

        # Number System
        number_system_key = ['number', 'numeral', '+', '-', '/', '*', 'numeration', 'place_value', 'compare',
                             "Natural_Numbers",
                             "natural", "whole", "integers", "rational", "irrational", "place", "face", "expanded",
                             "roman", "number", "estimation", "fractions", "decimal", "equivalent", "simplification",
                             "addition", 'add', "subtraction", "multiplication", "division", "operations",
                             "terminating",
                             "non-terminating", "remainder", "line", "conversion", "exponents", "power", "square",
                             "cube", "real",
                             "laws", "rationalizing", "euclid's", "hcf", "lcm", 'pow', "euclidean", "fundamental"]

        for i in number_system_key:
            if i in l:
                category_list.append("number system")
            else:
                pass

        # Algebra
        algebra_key = ['algebra', 'expression', 'equation', "=", "algebraic", "expression", "equation", "variable",
                       "constant", "coefficient", "linear", "quadratic", "**", "polynomial", "factor", "identity", 'root',
                       "simultaneous", "inequality", "algebra", "formula", "exponent", 'log', "binomial", "trinomial",
                       "equation", "simplification", "graph", "system"]

        for i in algebra_key:
            if i in l:
                category_list.append("algebra")
            else:
                pass

        # Mensuration
        mensuration_key = ['geometry', 'shape', 'area', 'perimeter', 'volume', "area", "perimeter", "rectangle",
                           "square", "triangle", "hypotenuse", "circle", "parallelogram", "rhombus", "trapezium",
                           "quadrilateral", "polygon",
                           "volume", "cylinder", "cone", "sphere", "cube", "cuboid", "pyramid", "hemisphere", "surface",
                           "base",
                           "height", "radius", "diameter", "perpendicular", "diagonal", "isometric", "net", "height",
                           "lateral", "surface", "right", "angled", "equilateral", "isosceles", "scalene", "obtuse",
                           "acute", "right-angled", "similar", "congruent", "prism", "composite",
                           "regular", "irregular", "symmetry", "axis", "point", "centroid", "circumcenter", "incenter",
                           "orthocenter", "area", "perimeter"]

        for i in mensuration_key:
            if i in l:
                category_list.append("mensuration")
            else:
                pass

        # Statistics and Probability

        stat_prob_key = ['data', 'graph', 'chart', 'mean', 'median', 'mode', 'probability', 'chance', 'likely',
                         'unlikely',
                         "data", "mean", "median", "mode", "range", "frequency", "bar", "chart", "pie", "graph",
                         "probability",
                         "experiment", "outcomes", "sample", "event", "likely", "unlikely", "fair", "biased", "tree",
                         "diagram", "combinations", "permutations", "random", "variable", "independent",
                         "dependent", "expected", "ratio", "odds", "experimental", "theoretical", "trials", "success",
                         "failure", "mutually", "exclusive", "complementary", "union", "intersection",
                         "outcome", "probability", "distribution", "range", "mode", "mean", "median", "variance",
                         "standard",
                         "deviation", "percentile", "correlation", "regression", "sample", "population", "confidence",
                         "interval", "hypothesis", "test"]

        for i in stat_prob_key:
            if i in l:
                category_list.append("statistics and probability")
            else:
                pass

        # Trigonometry
        trigonometry_key = ['trigonometry', "sin", "cos", "tan", "cot", "sec", "cosec", 'angle', 'triangle', 'sine',
                            'cosine', 'tangent',
                            "angle", "degree", "radian", "triangle", "right", "acute", "obtuse", "opposite",
                            "adjacent", "sine", "cosine", "tangent", "cotangent", "secant",
                            "cosecant", "pythagorean", "trigonometric", "identity", "solving", "equations",
                            "trigonometric", "ratios", "trigonometric", "functions", "angle", "measurements",
                            "angle", "sum", "difference", "multiple", "division", "values", "unit", "circle", "solving",
                            "problems"]

        for i in trigonometry_key:
            if i in l:
                category_list.append('trigonometry')
            else:
                pass

        category_list = set(category_list)


        # Quadratic Equation  and Cubic Equation questions from 2 to 20
        if "Quadratic Equation" in category_list or "Cubic Equation" in category_list:
            que_num = random.sample(range(2, 20), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            #output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running

        # trigonometry questions from 44 to 56
        if "trigonometry" in category_list:
            que_num = random.sample(range(44, 56), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            # output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running

        # Algebra questions from 72 to 84
        if "algebra" in category_list:
            que_num = random.sample(range(72, 84), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            # output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running

        # number system questions from 58 to 70
        if "number system" in category_list:
            que_num = random.sample(range(58, 70), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            # output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running

        # mensuration questions from 16 to 27
        if "mensuration" in category_list:
            que_num = random.sample(range(16, 27), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            # output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running

        # probability and statistics from 30 ,42
        if "statistics and probability" in category_list:
            que_num = random.sample(range(30, 42), 1)
            print_use = linecache.getline('./assets/real_life_use.txt', que_num[0])

            # output
            return JsonResponse({"answer": print_use})  # should fetch line from real_life_use.txt file but not running


def level_1_questions(request):

    if request.method == 'POST':

        #input
        user_input = request.POST.get("question", "") # example ( x + 5 = 10) any question
        user_input = str(user_input).lower()

        num_ques = request.POST.get("no_of_ques", "")

        input_list = list(user_input)
        for i in range(num_ques):
            update_list = list()
            for i in input_list:
                if i.isdigit():
                    try:
                        change = random.randint(1, int(i))
                    except:
                        change = random.randint(0, int(i))
                    update_list.append(str(change))
                else:
                    update_list.append(i)

            new = ''.join(update_list)

            # output
            return JsonResponse({"answer": str(new)}) # x + 3 = 7 , should change the digits of the given question, but not running





def level_2_questions(request):

    if request.method == 'POST':

        #input
        user_input = request.POST.get("question", "") # example: (x**2 + 2*x - 15) any question
        user_input = str(user_input).lower()

        import random
        import linecache

        l = user_input.split(" ")
        category_list = []

        # equation type
        alpha_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if 'x**3' in l or 'y**3' in l or 'x^3' in l or 'y^3' in l:
            category_list.append("Cubic Equation")
        elif 'x**2' in l or 'y**2' in l or 'x^2' in l or 'y^2' in l:
            category_list.append("Quadratic Equation")
        else:
            for i in alpha_letters:
                if i in l:
                    category_list.append("Polynomial Equation")

        # Number System
        number_system_key = ['number', 'numeral', '+', '-', '/', '*', 'numeration', 'place_value', 'compare',
                             "Natural_Numbers",
                             "natural", "whole", "integers", "rational", "irrational", "place", "face", "expanded",
                             "roman", "number", "estimation", "fractions", "decimal", "equivalent", "simplification",
                             "addition", 'add', "subtraction", "multiplication", "division", "operations",
                             "terminating",
                             "non-terminating", "remainder", "line", "conversion", "exponents", "power", "square",
                             "cube", "real",
                             "laws", "rationalizing", "euclid's", "hcf", "lcm", 'pow', "euclidean", "fundamental"]

        for i in number_system_key:
            if i in l:
                category_list.append("number system")
            else:
                pass

        # Algebra
        algebra_key = ['algebra', 'expression', 'equation', "=", "algebraic", "expression", "equation", "variable",
                       "constant", "coefficient", "linear", "quadratic", "**", "polynomial", "factor", "identity", 'root',
                       "simultaneous", "inequality", "algebra", "formula", "exponent", 'log', "binomial", "trinomial",
                       "equation", "simplification", "graph", "system"]

        for i in algebra_key:
            if i in l:
                category_list.append("algebra")
            else:
                pass

        # Mensuration
        mensuration_key = ['geometry', 'shape', 'area', 'perimeter', 'volume', "area", "perimeter", "rectangle",
                           "square", "triangle", "hypotenuse", "circle", "parallelogram", "rhombus", "trapezium",
                           "quadrilateral", "polygon",
                           "volume", "cylinder", "cone", "sphere", "cube", "cuboid", "pyramid", "hemisphere", "surface",
                           "base",
                           "height", "radius", "diameter", "perpendicular", "diagonal", "isometric", "net", "height",
                           "lateral", "surface", "right", "angled", "equilateral", "isosceles", "scalene", "obtuse",
                           "acute", "right-angled", "similar", "congruent", "prism", "composite",
                           "regular", "irregular", "symmetry", "axis", "point", "centroid", "circumcenter", "incenter",
                           "orthocenter", "area", "perimeter"]

        for i in mensuration_key:
            if i in l:
                category_list.append("mensuration")
            else:
                pass

        # Statistics and Probability

        stat_prob_key = ['data', 'graph', 'chart', 'mean', 'median', 'mode', 'probability', 'chance', 'likely',
                         'unlikely',
                         "data", "mean", "median", "mode", "range", "frequency", "bar", "chart", "pie", "graph",
                         "probability",
                         "experiment", "outcomes", "sample", "event", "likely", "unlikely", "fair", "biased", "tree",
                         "diagram", "combinations", "permutations", "random", "variable", "independent",
                         "dependent", "expected", "ratio", "odds", "experimental", "theoretical", "trials", "success",
                         "failure", "mutually", "exclusive", "complementary", "union", "intersection",
                         "outcome", "probability", "distribution", "range", "mode", "mean", "median", "variance",
                         "standard",
                         "deviation", "percentile", "correlation", "regression", "sample", "population", "confidence",
                         "interval", "hypothesis", "test"]

        for i in stat_prob_key:
            if i in l:
                category_list.append("statistics and probability")
            else:
                pass

        # Trigonometry
        trigonometry_key = ['trigonometry', "sin", "cos", "tan", "cot", "sec", "cosec", 'angle', 'triangle', 'sine',
                            'cosine', 'tangent',
                            "angle", "degree", "radian", "triangle", "right", "acute", "obtuse", "opposite",
                            "adjacent", "sine", "cosine", "tangent", "cotangent", "secant",
                            "cosecant", "pythagorean", "trigonometric", "identity", "solving", "equations",
                            "trigonometric", "ratios", "trigonometric", "functions", "angle", "measurements",
                            "angle", "sum", "difference", "multiple", "division", "values", "unit", "circle", "solving",
                            "problems"]

        for i in trigonometry_key:
            if i in l:
                category_list.append('trigonometry')
            else:
                pass

        category_list = set(category_list)

        # Quadratic Equation  and Cubic Equation questions from 174 to 200
        if "Quadratic Equation" in category_list or "Cubic Equation" in category_list:
            que_num = random.sample(range(174, 200), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans})     # should fetch lines from questions.txt and answers.txt. but not running


        # trigonometry questions from 1 to 40
        elif "trigonometry" in category_list:
            que_num = random.sample(range(1, 41), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans}) # should fetch lines from questions.txt and answers.txt. but not running


        # Algebra questions from 43 to 80
        elif "algebra" in category_list and "trigonometry" not in category_list:
            que_num = random.sample(range(46, 84), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans}) # should fetch lines from questions.txt and answers.txt. but not running


        # number system questions from 87 to 123
        elif "number system" in category_list and "trigonometry" not in category_list and "algebra" not in category_list and "statistics and probability" not in category_list:
            que_num = random.sample(range(87, 123), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans}) # should fetch lines from questions.txt and answers.txt. but not running


        # mensuration questions from 126 to 170
        elif "mensuration" in category_list and "trigonometry" not in category_list and "algebra" not in category_list and "statistics and probability" not in category_list:
            que_num = random.sample(range(126, 170), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans}) # should fetch lines from questions.txt and answers.txt. but not running



            # statistics and probability questions from 204 to 221
        elif "statistics and probability" in category_list:
            que_num = random.sample(range(204, 221), 3)
            print_L2que = linecache.getline('questions.txt', que_num[0])
            print_L2ans = linecache.getline('answers.txt', que_num[0])

            print_L2que += linecache.getline('questions.txt', que_num[1])
            print_L2ans += linecache.getline('answers.txt', que_num[1])

            print_L2que += linecache.getline('questions.txt', que_num[2])
            print_L2ans += linecache.getline('answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L2que, "answers": print_L2ans}) # should fetch lines from questions.txt and answers.txt. but not running


def level_3_questions(request):
    if request.method == 'POST':

        # input
        user_input = request.POST.get("question", "") #example: (x**2 + 2*x -15) any question
        user_input = str(user_input).lower()

        import random
        import linecache

        l = user_input.split(" ")
        category_list = []

        # equation type
        alpha_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if 'x**3' in l or 'y**3' in l or 'x^3' in l or 'y^3' in l:
            category_list.append("Cubic Equation")
        elif 'x**2' in l or 'y**2' in l or 'x^2' in l or 'y^2' in l:
            category_list.append("Quadratic Equation")
        else:
            for i in alpha_letters:
                if i in l:
                    category_list.append("Polynomial Equation")

        # Number System
        number_system_key = ['number', 'numeral', '+', '-', '/', '*', 'numeration', 'place_value', 'compare',
                             "Natural_Numbers",
                             "natural", "whole", "integers", "rational", "irrational", "place", "face", "expanded",
                             "roman", "number", "estimation", "fractions", "decimal", "equivalent", "simplification",
                             "addition", 'add', "subtraction", "multiplication", "division", "operations",
                             "terminating",
                             "non-terminating", "remainder", "line", "conversion", "exponents", "power", "square",
                             "cube", "real",
                             "laws", "rationalizing", "euclid's", "hcf", "lcm", 'pow', "euclidean", "fundamental"]

        for i in number_system_key:
            if i in l:
                category_list.append("number system")
            else:
                pass

        # Algebra
        algebra_key = ['algebra', 'expression', 'equation', "=", "algebraic", "expression", "equation", "variable",
                       "constant", "coefficient", "linear", "quadratic", "**", "polynomial", "factor", "identity", 'root',
                       "simultaneous", "inequality", "algebra", "formula", "exponent", 'log', "binomial", "trinomial",
                       "equation", "simplification", "graph", "system"]

        for i in algebra_key:
            if i in l:
                category_list.append("algebra")
            else:
                pass

        # Mensuration
        mensuration_key = ['geometry', 'shape', 'area', 'perimeter', 'volume', "area", "perimeter", "rectangle",
                           "square", "triangle", "hypotenuse", "circle", "parallelogram", "rhombus", "trapezium",
                           "quadrilateral", "polygon",
                           "volume", "cylinder", "cone", "sphere", "cube", "cuboid", "pyramid", "hemisphere", "surface",
                           "base",
                           "height", "radius", "diameter", "perpendicular", "diagonal", "isometric", "net", "height",
                           "lateral", "surface", "right", "angled", "equilateral", "isosceles", "scalene", "obtuse",
                           "acute", "right-angled", "similar", "congruent", "prism", "composite",
                           "regular", "irregular", "symmetry", "axis", "point", "centroid", "circumcenter", "incenter",
                           "orthocenter", "area", "perimeter"]

        for i in mensuration_key:
            if i in l:
                category_list.append("mensuration")
            else:
                pass

        # Statistics and Probability

        stat_prob_key = ['data', 'graph', 'chart', 'mean', 'median', 'mode', 'probability', 'chance', 'likely',
                         'unlikely',
                         "data", "mean", "median", "mode", "range", "frequency", "bar", "chart", "pie", "graph",
                         "probability",
                         "experiment", "outcomes", "sample", "event", "likely", "unlikely", "fair", "biased", "tree",
                         "diagram", "combinations", "permutations", "random", "variable", "independent",
                         "dependent", "expected", "ratio", "odds", "experimental", "theoretical", "trials", "success",
                         "failure", "mutually", "exclusive", "complementary", "union", "intersection",
                         "outcome", "probability", "distribution", "range", "mode", "mean", "median", "variance",
                         "standard",
                         "deviation", "percentile", "correlation", "regression", "sample", "population", "confidence",
                         "interval", "hypothesis", "test"]

        for i in stat_prob_key:
            if i in l:
                category_list.append("statistics and probability")
            else:
                pass

        # Trigonometry
        trigonometry_key = ['trigonometry', "sin", "cos", "tan", "cot", "sec", "cosec", 'angle', 'triangle', 'sine',
                            'cosine', 'tangent',
                            "angle", "degree", "radian", "triangle", "right", "acute", "obtuse", "opposite",
                            "adjacent", "sine", "cosine", "tangent", "cotangent", "secant",
                            "cosecant", "pythagorean", "trigonometric", "identity", "solving", "equations",
                            "trigonometric", "ratios", "trigonometric", "functions", "angle", "measurements",
                            "angle", "sum", "difference", "multiple", "division", "values", "unit", "circle", "solving",
                            "problems"]

        for i in trigonometry_key:
            if i in l:
                category_list.append('trigonometry')
            else:
                pass

        category_list = set(category_list)

        # Quadratic Equation  and Cubic Equation questions from 174 to 200
        if "Quadratic Equation" in category_list or "Cubic Equation" in category_list:
            que_num = random.sample(range(174, 200), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running




        # trigonometry questions from 1 to 40
        elif "trigonometry" in category_list:
            que_num = random.sample(range(1, 41), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running

        # Algebra questions from 43 to 80
        elif "algebra" in category_list and "trigonometry" not in category_list:
            que_num = random.sample(range(46, 84), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running

        # number system questions from 87 to 123
        elif "number system" in category_list and "trigonometry" not in category_list and "algebra" not in category_list and "statistics and probability" not in category_list:
            que_num = random.sample(range(87, 123), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running


        # mensuration questions from 126 to 170
        elif "mensuration" in category_list and "trigonometry" not in category_list and "algebra" not in category_list and "statistics and probability" not in category_list:
            que_num = random.sample(range(126, 170), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running

        # statistics and probability questions from 204 to 221
        elif "statistics and probability" in category_list:
            que_num = random.sample(range(204, 221), 3)
            print_L3que = linecache.getline('L3questions.txt', que_num[0])
            print_L3ans = linecache.getline('L3answers.txt', que_num[0])

            print_L3que += linecache.getline('L3questions.txt', que_num[1])
            print_L3ans += linecache.getline('L3answers.txt', que_num[1])

            print_L3que += linecache.getline('L3questions.txt', que_num[2])
            print_L3ans += linecache.getline('L3answers.txt', que_num[2])

            # output
            return JsonResponse({"questions": print_L3que, "answers": print_L3ans}) # should print the fetched lines from L3questions.txt and L3answers.txt. but not running


def specific_category_questions(request):
    if request.method == 'POST':
        #input ; chose category from : Quadratic Equation, trigonometry, statistics and probability, mensuration, number system, algebra
        ask_category = request.POST.get("choose category", "") # category from the above

        if ask_category == 'Quadratic Equation':
            que_num = random.sample(range(174, 201), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(174, 201), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3questions.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running




        elif ask_category == 'statistics and probability':
            que_num = random.sample(range(204, 221), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(204, 221), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3answers.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running



        elif ask_category == 'mensuration':
            que_num = random.sample(range(126, 171), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(126, 171), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3answers.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running



        elif ask_category == 'number system':
            que_num = random.sample(range(87, 123), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(87, 123), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3answers.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running



        elif ask_category == 'algebra':
            que_num = random.sample(range(46, 84), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(46, 84), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3answers.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running



        elif ask_category == 'trigonometry':
            que_num = random.sample(range(1, 41), 3)
            print_Sque = linecache.getline('questions.txt', que_num[0])
            print_Sans = linecache.getline('answers.txt', que_num[0])

            print_Sque += linecache.getline('questions.txt', que_num[1])
            print_Sans += linecache.getline('answers.txt', que_num[1])

            print_Sque += linecache.getline('questions.txt', que_num[2])
            print_Sans += linecache.getline('answers.txt', que_num[2])

            que_num2 = random.sample(range(1, 41), 2)
            print_Sque = linecache.getline('L3questions.txt', que_num2[0])
            print_Sans += linecache.getline('L3answers.txt', que_num2[0])

            print_Sque += linecache.getline('L3questions.txt', que_num2[1])
            print_Sans += linecache.getline('L3answers.txt', que_num2[1])

            # output
            return JsonResponse({"questions": print_Sque, "answers": print_Sans})   # should print the fetched lines from questions.txt, answers.txt and L3questions.txt and L3answers.txt. but not running 

