import multiprocessing
from multiprocessing import Pool
from app.compile import compile_code


# 시간 제한이 있는 컴파일 함수
def compile_with_timeout(code):
    with Pool(processes=1) as pool:
        result = pool.apply_async(compile_code, (code,))
        try:
            # 5초 내에 결과를 얻습니다.
            return result.get(timeout=5)
        except multiprocessing.TimeoutError:
            pool.terminate()
            return "Execution timed out"
