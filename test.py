


from abc import ABC
from dataclasses import asdict, dataclass
from functools import wraps
from json import dumps, loads



@dataclass
class Base:
    event_store: list

@dataclass
class Test(ABC):
    id: str
    text: str

    def test(func):
        print(func, 'this')
        @wraps(func)
        def wrappered(self, *args, **kwargs):
            print(self, *args, **kwargs)
            return func(self, *args, **kwargs)
        return wrappered



@dataclass
class Test2(Base):
    cache: str
    testov: Test
    
    @Test.test
    def handele(self, string: str):
        print("await function")

tes = Test('141', '123')
t = Test2([1, 2], 'saf', tes)
data = asdict(t)
data = [data]
stroka = (dumps(data))
new_data = loads(stroka)[0]
print(asdict)