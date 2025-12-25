from fuzzingbook.ConcolicFuzzer import ConcolicTracer, SimpleConcolicFuzzer, ExpectError
from src.evaluator import setup_runtime

with ConcolicTracer() as tracer:
    tracer[setup_runtime]("thing")
scf = SimpleConcolicFuzzer()
scf.add_trace(tracer, "thing")
for i in range(20):
    v = scf.fuzz()
    if v is None:
        break
    print(repr(v))
    with ExpectError(print_traceback=False):
        with ConcolicTracer() as tracer:
            tracer[setup_runtime](v)
    scf.add_trace(tracer, v)