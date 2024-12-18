from typing import Optional, Dict
import contextlib
import traceback
import io
import re
import sys
import copy
import logging
from func_timeout import func_set_timeout

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class WriteOnlyStringIO(io.StringIO):
    """ StringIO that throws an exception when it's read from """
    def read(self, *args, **kwargs):
        raise IOError

    def readline(self, *args, **kwargs):
        raise IOError

    def readlines(self, *args, **kwargs):
        raise IOError

    def readable(self, *args, **kwargs):
        """ Returns False as the IO object cannot be read. """
        return False


class redirect_stdin(contextlib._RedirectStream):  # type: ignore
    _stream = 'stdin'


@contextlib.contextmanager
def swallow_io():
    """ Context manager that redirects stdout, stderr, and stdin to a WriteOnlyStringIO. """
    stream = WriteOnlyStringIO()
    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream), redirect_stdin(stream):
        yield


@func_set_timeout(60)
def execute_program(check_program: str, traceback_tag: bool):
    """ Executes a given Python program and captures output or exceptions.

    Args:
        check_program (str): The code to be executed.
        traceback_tag (bool): If True, include traceback in the output on failure.

    Returns:
        tuple: Result of execution and globals defined by the executed code.
    """
    try:
        exec_globals = {}
        with swallow_io():
            exec(check_program, exec_globals)
        result = "passed"
    except Exception as e:
        if traceback_tag:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            result = traceback_lines
        else:
            result = f"failed: {e}"
    return result, exec_globals


def insert_random_seed(code: str) -> str:
    """ Inserts a random seed into the provided code for reproducibility.

    Args:
        code (str): The original code to be modified.

    Returns:
        str: The modified code with random seed inserted.
    """
    code_temp = copy.deepcopy(code)

    # Insert seed for canonical_solution function
    if 'canonical_solution' in code:
        code_temp = 'def canonical_solution():'.join(code_temp.split('def canonical_solution():')[1:])
        code_temp = code_temp.replace('def canonical_solution():\n', '').replace('def canonical_solution():', '')
        tab_can = re.findall('[\n ]{0,}', code_temp)[0]
        code = code.replace('def canonical_solution():\n', f'def canonical_solution():\n{tab_can}import numpy as np\n{tab_can}np.random.seed(10)\n')

    # Insert seed for generate_function function
    elif 'generate_function' in code:
        code_temp = 'def generate_function():'.join(code_temp.split('def generate_function():')[1:])
        code_temp = code_temp.replace('def generate_function():\n', '').replace('def generate_function():', '')
        tab_gen = re.findall('[\n ]{0,}', code_temp)[0]
        code = code.replace('def generate_function():\n', f'def generate_function():\n{tab_gen}import numpy as np\n{tab_gen}np.random.seed(10)\n')

    # Modify default_rng if present
    if 'rng = np.random.default_rng()' in code:
        code = code.replace('np.random.default_rng()', 'np.random.default_rng(seed=42)')
    else:
        num = re.findall('np.random.default_rng\((\d*)\)', code)
        if num:
            code = code.replace(f'np.random.default_rng({num[0]})', 'np.random.default_rng(seed=42)')
    
    return code


def execute_programs(canonical_solution: Optional[str] = None, generate_code: Optional[str] = None,
                     test_code: Optional[str] = None, is_tuple: bool = False,
                     tuple_index: int = 0, traceback_tag: bool = False):
    """
    Execute a series of programs based on provided solutions and testing code.

    Args:
        canonical_solution (str): The canonical solution code to execute.
        generate_code (str): The generated code to test.
        test_code (str): The test code to validate the results.
        is_tuple (bool): If True, treats outputs as tuples.
        tuple_index (int): The index to access in tuple outputs.
        traceback_tag (bool): If True, includes traceback in execution.

    Returns:
        tuple: A tuple containing success status, result message, answer, and executed code.
    """
    if canonical_solution and not generate_code:
        logging.info('Executing canonical solution code')
        check_program = canonical_solution + '\n' + 'answer = canonical_solution()'
    elif generate_code and not canonical_solution:
        logging.info('Executing generated code')
        check_program = generate_code + '\n' + 'answer = generate_function()'
    elif canonical_solution and generate_code and test_code:
        # Insert random seed for both solutions
        canonical_solution = insert_random_seed(canonical_solution)
        generate_code = insert_random_seed(generate_code)

        if not is_tuple:
            logging.info('Executing non-tuple type test code')
            check_program = (
                f"{canonical_solution}\n{generate_code}\n{test_code}\n"
                "data1 = canonical_solution()\ndata2 = generate_function()\n"
                "assert test_code(data1, data2) == True\n"
                "answer = test_code(data1, data2)"
            )
        else:
            logging.info('Executing tuple type test code')
            check_program = (
                f"{canonical_solution}\n{generate_code}\n{test_code}\n"
                f"data1 = canonical_solution()[{tuple_index}]\n"
                f"data2 = generate_function()[{tuple_index}]\n"
                "assert test_code(data1, data2) == True\n"
                "answer = test_code(data1, data2)"
            )
    else:
        raise AssertionError('Input parameters are incorrect')

    try:
        result, exec_globals = execute_program(check_program, traceback_tag)
    except func_timeout.exceptions.FunctionTimedOut:
        logging.info("Execution timed out after 60 seconds")
        result = 'timeout'
        exec_globals = {}

    if result == 'passed':
        answer = exec_globals.get('answer', '')
        logging.info('Code execution successful')
        return True, result, answer, check_program
    else:
        answer = ''
        logging.info(f'Code execution failed. Check code: {check_program} Reason: {result}')
        return False, result, answer, check_program