# README

> SOUP: Simple, Ordinary, Ugly Pascal compiler

## usage

可以通过如下语句运行 SOUP, 其中

- `input` 参数提供 pascal 文件路径
- `output` 参数（可选）提供三地址码输出路径，默认为 *soup.out*
- `visualize` 参数（可选）提供可视化图片输出路径，将在该路径下输出 Parser 输出的 abstract syntax tree `original_ast.png`，经过 Semantic 缩减后的 abstract syntax tree `final_ast.png`，以及 SymbolTable 的可视化图片 `symb_tab.png`, 在 *visualization* 文件夹下有三种图片示例；

```
python soup.py --input input_file [--output output_file] [--visualize visualize_output_dir]
```

## test

提供 `test_script.py` 进行批量测试，三段码文件将在 `test_dir` 指定的目录下生成：

```
python test_script.py --test_dir test
```

我们报告中涉及的所有测试文件均在 `test` 文件夹下