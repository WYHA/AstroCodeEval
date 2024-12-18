from typing import Optional, Dict
import contextlib
import traceback
# import signal
import io
import re
import sys
import copy
from timeout_decorator import timeout, TimeoutError
import time
import func_timeout
from func_timeout import func_set_timeout
import logging
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
        """ Returns True if the IO object can be read. """
        return False
    
class redirect_stdin(contextlib._RedirectStream):  # type: ignore
    _stream = 'stdin'

@contextlib.contextmanager
def swallow_io():
    stream = WriteOnlyStringIO()
    with contextlib.redirect_stdout(stream):
        with contextlib.redirect_stderr(stream):
            with redirect_stdin(stream):
                yield

@func_set_timeout(60)
def execute_program(check_program,traceback_tag):
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
            result = "failed: {}".format(e)
    return result,exec_globals

def insert_random_seed(code):
    code_temp = copy.deepcopy(code)
    if 'canonical_solution' in code:
        code_temp = copy.deepcopy(code)
        code_temp = 'def canonical_solution():'.join(code_temp.split('def canonical_solution():')[1:])
        code_temp = code_temp.replace('def canonical_solution():\n','').replace('def canonical_solution():','')
        tab_can = re.findall('[\n ]{0,}',code_temp)[0]
        code = code.replace('def canonical_solution():\n','def canonical_solution():\n{}import numpy as np\n{}np.random.seed(10)\n'.format(tab_can,tab_can))
    elif 'generate_function' in code:
        code_temp = copy.deepcopy(code)
        code_temp = 'def generate_function():'.join(code_temp.split('def generate_function():')[1:])
        code_temp = code_temp.replace('def generate_function():\n','').replace('def generate_function():','')
        tab_gen = re.findall('[\n ]{0,}',code_temp)[0]
        code = code.replace('def generate_function():\n','def generate_function():\n{}import numpy as np\n{}np.random.seed(10)\n'.format(tab_gen,tab_gen))
    if 'rng = np.random.default_rng()' in code:
        code = code.replace('np.random.default_rng()','np.random.default_rng(seed=42)')
    else:
        num = re.findall('np.random.default_rng\((\d*)\)',code)
        if num:
            code = code.replace('np.random.default_rng({})'.format(num[0]),'np.random.default_rng(seed=42)')
    return code

def execute_programs(canonical_solution=None,generate_code=None,test_code=None,tuple=False,tuple_index=0,traceback_tag=False):
    if canonical_solution and not generate_code:
        logging.info('执行标准代码')
        check_program = canonical_solution + '\n' + 'answer = canonical_solution()'
    elif generate_code and not canonical_solution:
        logging.info('执行生成代码')
        check_program = generate_code + '\n' + 'answer = generate_function()'
    elif canonical_solution and generate_code and test_code and not tuple:
        canonical_solution = insert_random_seed(canonical_solution)
        generate_code = insert_random_seed(generate_code)
        logging.info('执行非tuple类型测试代码')
        check_program = canonical_solution + '\n' + generate_code + '\n' + test_code + '\n' + 'data1 = canonical_solution()\ndata2 = generate_function()\nassert test_code(data1,data2)==True\nanswer = test_code(data1,data2)'
    elif canonical_solution and generate_code and test_code and tuple:
        canonical_solution = insert_random_seed(canonical_solution)
        generate_code = insert_random_seed(generate_code)
        check_program = canonical_solution + '\n' + generate_code + '\n' + test_code + '\n' + 'data1 = canonical_solution()[{}]\ndata2 = generate_function()[{}]\nassert test_code(data1,data2)==True\nanswer = test_code(data1,data2)'.format(tuple_index,tuple_index)
    else:
        AssertionError('输入存在错误')

    try:
        result,exec_globals = execute_program(check_program,traceback_tag)
    except func_timeout.exceptions.FunctionTimedOut:
        logging.info("执行已超时60秒")
        result = 'timeout'
        exec_globals = {}
    
    if result=='passed':
        answer = exec_globals['answer']
        logging.info(f'代码成功执行')
        return True,result,answer,check_program
    else:   
        answer = ''
        logging.info(f'代码报错，错误代码：{check_program} 原因是: {result}')
        return False,result,answer,check_program

if __name__=='__main__':
    generate_function = "def generate_function():\n  from astropy import units as u\n  from astropy.coordinates import SkyCoord\n  c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, frame='icrs')\n  c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, frame='fk5')\n  return c1.separation(c2)\n"
    canonical_solution = "def canonical_solution():\n  from astropy import units as u\n  from astropy.coordinates import SkyCoord\n  c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, frame='icrs')\n  c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, frame='fk5')\n  return c1.separation(c2)\n"
    text_code = "assert canonical_solution()==generate_function()"
    check_program = generate_function + '\n' + canonical_solution + '\n' + text_code
    traceback_tag = True
    result,exec_globals = execute_program(check_program,traceback_tag)
    print(result)
    