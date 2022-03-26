```python
class Person:
    def __init__(self, age = 20, gender = "female"):
        self.gender = gender
        self.age = age
```

```python
from dataclasses import dataclass
@dataclass
class DataclassPerson:
    gender: str = "female"
    name: int = 20
```

## DataClass の利点

- 可読性が高まる。
- 型アノテーションができる。
- 

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="PIL IOError: image file truncated with big images" src="https://hatenablog-parts.com/embed?url=https://stackoverflow.com/questions/12984426/pil-ioerror-image-file-truncated-with-big-images" frameborder="0" scrolling="no"></iframe>
