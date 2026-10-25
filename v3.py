# -*- coding: gbk -*-
import threading, time
from od_platform.inference import CancelToken, InferHooks
t = CancelToken()
assert not t.is_cancelled()
t.cancel()
assert t.is_cancelled()
print("? CancelToken ���� + �ݵ�")
h = InferHooks()
def bad(*a, **kw): raise RuntimeError("user bug")
h3 = InferHooks(on_frame=bad)
h3.fire_frame(None)
print("? InferHooks �쳣����")
