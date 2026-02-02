# 创意编程模式

## 生成艺术

### 分形

```python
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(h, w, max_iter):
    y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
    c = x + y*1j
    z = c
    div_time = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (div_time == max_iter)
        div_time[div_now] = i
        z[diverge] = 2

    return div_time

plt.imshow(mandelbrot(800, 1200, 100), cmap='hot')
plt.show()
```

### 粒子系统

```python
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.life = 100

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1

    def is_alive(self):
        return self.life > 0
```

### L-System

```python
def l_system(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_str = ""
        for char in current:
            next_str += rules.get(char, char)
        current = next_str
    return current

# 树的 L-system
rules = {
    'F': 'FF+[+F-F-F]-[-F+F+F]'
}
tree = l_system('F', rules, 3)
```

## 数据可视化

### 交互式图表

```javascript
// D3.js 示例
const svg = d3.select("svg");
const data = [10, 20, 30, 40, 50];

svg.selectAll("rect")
   .data(data)
   .enter()
   .append("rect")
   .attr("x", (d, i) => i * 50)
   .attr("y", d => 100 - d)
   .attr("width", 40)
   .attr("height", d => d)
   .on("mouseover", function() {
       d3.select(this).style("fill", "orange");
   });
```

## 算法音乐

### 简单合成器

```python
import numpy as np

def generate_sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * freq * t)

def generate_chord(frequencies, duration):
    waves = [generate_sine_wave(f, duration) for f in frequencies]
    return sum(waves) / len(waves)

# C 大三和弦
c_major = generate_chord([261.63, 329.63, 392.00], 1.0)
```

## 元编程

### 代码生成器

```python
def create_class(name, attributes):
    attrs = "\n    ".join(
        f"self.{attr} = {attr}" for attr in attributes
    )
    params = ", ".join(attributes)

    code = f'''
class {name}:
    def __init__(self, {params}):
        {attrs}

    def __repr__(self):
        return f"{name}({", ".join(f"{a}={{self.{a}}}" for a in {attributes!r})})"
'''
    return code

# 动态创建类
exec(create_class("Person", ["name", "age"]))
```

## 随机性与种子

```python
import random

def reproducible_art(seed):
    random.seed(seed)
    # 基于种子的确定性随机
    colors = [random.choice(['red', 'blue', 'green']) for _ in range(10)]
    positions = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    return colors, positions

# 相同种子总是产生相同结果
art1 = reproducible_art(42)
art2 = reproducible_art(42)
assert art1 == art2
```

## 创意原则

1. **拥抱意外**: 错误可能是新发现
2. **迭代探索**: 小步快速实验
3. **组合创新**: 混合不同技术
4. **约束激发**: 限制催生创意
5. **记录过程**: 保存中间版本
