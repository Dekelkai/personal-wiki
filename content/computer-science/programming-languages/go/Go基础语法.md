---
title: Go基础语法
type: guide
domain: computer-science
status: draft
publish: true
created: 2026-07-17
updated: 2026-07-17
topics: [go, programming-languages]
---

# 🐹 Go 基础语法

Go 程序由包、声明和函数组成。语法的核心特点是静态类型、显式错误值、简洁的控制流，以及由方法集隐式满足的接口。

## 最小程序

```go
package main

import "fmt"

func main() {
	fmt.Println("hello, wiki")
}
```

- 每个 `.go` 文件属于一个包；
- 可执行程序使用 `package main`；
- 入口函数是无参数、无返回值的 `main`。

## 变量与常量

```go
var count int          // 零值为 0
var name = "Quartz"   // 根据初始值推断类型
ready := true          // 短变量声明，只能在函数内使用

const maxRetries = 3
```

Go 变量在未显式初始化时获得该类型的零值。`:=` 至少需要引入一个新变量，不能在包级使用。

## 基本类型与转换

- 布尔：`bool`；
- 字符串：`string`，内容是只读字节序列；
- 整数：`int`、`int8`、`int16`、`int32`、`int64` 及对应无符号类型；
- 浮点：`float32`、`float64`；
- `byte` 是 `uint8` 的别名，`rune` 是 `int32` 的别名，常用于表达 Unicode 码点。

Go 不默认执行数值类型之间的隐式转换：

```go
var total int = 42
ratio := float64(total) / 100.0
```

## 控制流

Go 只有 `for` 循环，同时支持传统三段式、仅条件和无限循环。

```go
sum := 0
for i := 0; i < 5; i++ {
	sum += i
}

if sum >= 10 {
	fmt.Println("large")
} else {
	fmt.Println("small")
}

switch sum {
case 10:
	fmt.Println("exact")
default:
	fmt.Println("other")
}
```

`defer` 把函数调用延迟到外层函数返回前执行，多个延迟调用按后进先出顺序运行。

## 函数与多返回值

```go
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}
	return a / b, nil
}
```

多返回值常用于同时返回结果和 `error`。调用方应显式检查错误：

```go
result, err := divide(10, 2)
if err != nil {
	fmt.Println("error:", err)
	return
}
fmt.Println(result)
```

## 复合类型

| 类型 | 特点 | 典型用途 |
| --- | --- | --- |
| 数组 `[N]T` | 长度是类型的一部分，赋值时复制元素 | 固定规模数据 |
| 切片 `[]T` | 描述底层数组的一段，具有长度与容量 | 动态序列 |
| 映射 `map[K]V` | 键到值的关联结构 | 查表、计数、索引 |
| 结构体 `struct` | 将多个字段组成一个值 | 领域对象与配置 |
| 指针 `*T` | 引用可寻址的值，不支持指针算术 | 共享修改与避免大值复制 |

数组和切片的存储关系见[[数组与切片]]。

## 方法与接口

方法是带接收者的函数。接口由方法签名组成，类型无需显式声明即可满足接口。

```go
type Stringer interface {
	String() string
}

type User struct {
	Name string
}

func (u User) String() string {
	return u.Name
}
```

## 常见易错点

- 对未初始化的 `nil` 映射赋值会触发 panic；
- `append` 可能返回指向新底层数组的切片，必须接收返回值；
- 对切片进行子切片操作通常会共享底层数组；
- `range` 产生索引和元素值，元素值是当次迭代的值副本；
- 标识符首字母大写表示可从其他包访问。

## 官方资料

- [Go 语言规范](https://go.dev/ref/spec)
- [A Tour of Go](https://go.dev/tour/)

## 相关页面

- [[Go语言]]
- [[数组与切片]]
- [[二分查找]]
- [[软件工程]]
