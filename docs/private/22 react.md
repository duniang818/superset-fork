```
# Npmnpm install -g react-devtools
```

接下来从终端打开开发者工具：

```
react-devtools
```

然后通过将以下 `<script>` 标签添加到你网站的 `<head>` 开头来连接你的网站：

```
<html>  <head>    <script src="http://localhost:8097"></script>
```

## 查看node 依赖包安装路径：

npm root -g
如果不对，则可以修改：
npm config set prefix "D:\Program Files\nodejs\node_modules"
npm config set cache "D:\Program Files\nodejs\node_cache"

随着项目的发展，你会发现很多布局可以通过复用已经完成的组件来实现，从而加快开发进程。上文中提到的目录可以通过 `<TableOfContents />` 组件添加到任意的画面中！你也可以使用 React 开源社区分享的大量组件（例如 [Chakra UI](https://chakra-ui.com/) 和 [Material UI](https://material-ui.com/)）来项目。

## Facebook发明了[react](https://react.docschina.org/learn/rendering-lists)，jsx

react是用jsx编写的，支持js， HTML，css的组件

微软发明了 typescript， 文件后缀名为：tsc

那么jsx与tsc有什么关系？

### JS 和 JSX、TS 和 TSX 的区别

在编程世界中，文件后缀扮演着重要的角色，它们告诉我们文件的类型和应该如何处理这些文件。对于JavaScript和与其相关的技术，我们有两种常见的后缀：.js和.jsx，以及.ts和.tsx。

.js，作为JavaScript文件的标志，表明该文件包含的是纯JavaScript代码，这是一种广泛使用的直译式脚本语言，被大多数浏览器直接支持。

而.jsx，则代表该文件不仅包含JavaScript代码，还融入了类似XML的语法，这主要是React框架用来构建组件内部标签的一种方式。这种格式的文件需要通过编译器（如webpack）转换成纯JavaScript代码后，才能被浏览器执行。

值得注意的是，尽管.js和.jsx在语法上有所区别，但在实际使用中，它们的互换性很高，.jsx文件完全可以采用.js的语法编写，而且Facebook的React团队也建议统一使用.js后缀，无需特意区分。

再来看.ts和.tsx，它们与TypeScript紧密相关。.ts文件是纯粹的TypeScript代码，而.tsx文件则是TypeScript与JSX的结合。这意味着.tsx文件在遵循TypeScript语法的同时，还支持React的JSX语法。

从使用的角度来说，如果你的文件中需要包含HTML标签（如

），那么你应该使用.tsx后缀，因为.ts文件不支持这种语法。反之，如果你的文件只是纯粹的辅助函数或类型定义，那么使用.ts后缀就足够了。

总的来说，选择正确的文件后缀对于确保代码的正确性和提高开发效率都是非常重要的。

## **React 组件是一段可以 使用标签进行扩展 的 JavaScript 函数**。

- 使用标签，标签是函数体，是功能
- 最终呈现是js函数，只是首字母大写的js函数
- 组合起来就是用HTML标签来组装完成函数体功能的且函数名大写的js函数，被称为react组件。

## npx create-react-app basic-react

```
创建第一个应用；npx create-react-app basic-react
启动：
cd basic-react
npm start
```

```js
export default function Profile() {
  return (
    <img
      src="https://i.imgur.com/MK3eW3Am.jpg"
      alt="Katherine Johnson"
    />
  )
}
```

## 定义组件三部曲

### 第一步：导出组件

export default， 默认导出，是JavaScript的语法

### 第二步：定义函数

使用 `function Profile() { }` 定义名为 `Profile` 的 JavaScript 函数。

陷阱：

React 组件是常规的 JavaScript 函数，但 **组件的名称必须以大写字母开头**，否则它们将无法运行！

### 第三步：添加标签

添加类似HTML的标签，在js函数中添加标签，这种语法叫 jsx.

返回return语句可以在一行上，如果不在一行上，需要用 `()`一对括号括起来，否则 return 下一行的代码都将被忽略！

## CodeSandbox 与 Next.js

CodeSandbox: 基于React的在线代码沙盒平台

Next.js：The React 框架

你的 React 应用程序从“根”组件开始。通常，它会在启动新项目时自动创建。例如，如果你使用 [CodeSandbox](https://codesandbox.io/)，根组件定义在 `src/App.js` 中。如果使用 [Next.js](https://nextjs.org/) 框架，根组件定义在 `pages/index.js` 中。在这些示例中，一直有导出根组件。

## 导出导入

该示例中需要注意的是，如何将组件拆分成两个文件：

1. `Gallery.js`:

   * 定义了 `Profile` 组件，该组件仅在该文件内使用，没有被导出。
   * 使用 **默认导出** 的方式，将 `Gallery` 组件导出
2. `App.js`:

   * 使用 **默认导入** 的方式，从 `Gallery.js` 中导入 `Gallery` 组件。
   * 使用 **默认导出** 的方式，将根组件 `App` 导出。
   * 引入过程中，有些文件没有 .js 后缀，也是可以正常使用的。带上后缀更符合 [原生ES模块](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Modules)。

   ```js
   import Gallery from './Gallery.js';export default function App() {
   return (
   gallery
   );
   }
   ```

   这是 JavaScript 里两个主要用来导出值的方式：默认导出和具名导出。到目前为止，我们的示例中只用到了默认导出。但你可以在一个文件中，选择使用其中一种，或者两种都使用。**一个文件里有且仅有一个 *默认* 导出，但是可以有任意多个 *具名* 导出。**

   ![Default and named exports](https://react.docschina.org/images/docs/illustrations/i_import-export.svg)

   组件的导出方式决定了其导入方式。当你用默认导入的方式，导入具名导出的组件时，就会报错。如下表格可以帮你更好地理解它们：


   | 语法 | 导出语句                              | 导入语句                                |
   | ---- | ------------------------------------- | --------------------------------------- |
   | 默认 | `export default function Button() {}` | `import Button from './Button.js';`     |
   | 具名 | `export function Button() {}`         | `import { Button } from './Button.js';` |

   当使用默认导入时，你可以在 `import` 语句后面进行任意命名。比如 `import Banana from './Button.js'`，如此你能获得与默认导出一致的内容。相反，对于具名导入，导入和导出的名字必须一致。这也是为什么称其为 **具名** 导入的原因！

   **通常，文件中仅包含一个组件时，人们会选择默认导出，而当文件中包含多个组件或某个值需要导出时，则会选择具名导出。** 无论选择哪种方式，请记得给你的组件和相应的文件命名一个有意义的名字。我们不建议创建未命名的组件，比如 `export default () => {}`，因为这样会使得调试变得异常困难。

## props

事实上，props **正是** 组件的唯一参数！ React 组件函数接受一个参数，一个 `props` 对象：

```
function Avatar(props) {
  let person = props.person;
  let size = props.size;
  // ...
}
```

通常你不需要整个 `props` 对象，所以可以将它解构为单独的 props， 解构的时候需要用一对{}将函数的参数括起来，因为这里是实参引用的是对象。**不要忘记 `(` 和 `)` 之间的一对花括号 `{` 和 `}`**  。

```js
function Avatar({person, size}) {
let person = person;
let size = size;
// ...
}
```

这种语法被称为 [“解构”](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#Unpacking_fields_from_objects_passed_as_a_function_parameter)，等价于于从函数参数中读取属性：

```
function Avatar(props) {
  let person = props.person;
  let size = props.size;
  // ...
}
```

简洁的“展开”语法是有意义的：

```
function Profile(props) {
  return (
    <div className="card">
      <Avatar {...props} />
    </div>
  );
}
```

这会将 `Profile` 的所有 props 转发到 `Avatar`，而不列出每个名字。

**请克制地使用展开语法。** 如果你在所有其他组件中都使用它，那就有问题了。 通常，它表示你应该拆分组件，并将子组件作为 JSX 传递。 接下来会详细介绍！

## SyntaxError: Cannot use import statement outside a module

修改的app.js 与index.js有错误

## 状态：Hook， useState函数

你可以用 [`useState`](https://react.docschina.org/reference/react/useState) Hook 为组件添加状态。*Hook* 是能让你的组件使用 React 功能的特殊函数（状态是这些功能之一）。`useState` Hook 让你声明一个状态变量。它接收初始状态并返回一对值：当前状态，以及一个让你更新状态的设置函数。

以“`use`”开头的函数都被称为 **Hook**

State 变量仅用于在组件重渲染时保存信息。在单个事件处理函数中，普通变量就足够了。当普通变量运行良好时，不要引入 state 变量。

## 更新函数 n => n + 1， 必须是纯函数？只返回结果？

## react的驼峰命名？

React 使用的 JSX 语法是基于 JavaScript 的，而 JavaScript 中的变量名通常采用驼峰命名法（camelCase）。这是因为 JSX 本质上是 JavaScript 的语法糖，而且 React 组件的 props 和 state 也遵循 JavaScript 的命名习惯。

驼峰命名法是一种编码约定，它将词分开，并且每个单词的首字母大写，例如 `camelCase` 或 `CamelCase`。这与小驼峰命名法（lowerCamelCase）形成对比，在小驼峰命名法中，变量的第一个单词的首字母是小写的。

例如，在 JSX 中使用 React 组件时，你可能会这样写：

## const 与 let 的区别

## JavaScript中，"transform"和"translate"

在JavaScript中，"transform"和"translate"是用于处理HTML元素的样式属性，它们有以下区别：transform属性：transform属性是一个通用的属性，用于应用一系列的变换效果，包括平移、旋转、缩放、倾斜等。transform属性的值是一个变换函数列表，可以同时应用多个变换效果。变换函数可以使用关键字（如"translate"、“rotate”、“scale"等）或矩阵函数（如"matrix”、"matrix3d"等）来表示具体的变换操作。通过transform属性，可以在不改变文档流的情况下，改变元素的位置、形状和方向。translate属性：translate属性是transform属性的一部分，用于指定元素的平移变换效果。translate属性只能单独应用于元素的平移，而不能实现其他类型的变换效果。translate属性的值是一个表示平移距离的函数，可以指定在X轴和Y轴方向上的平移量。语法：translate(<x>, <y>)，其中<x>表示在X轴上的平移距离，<y>表示在Y轴上的平移距离。

mutation：可变的

immutation：不可变的

## js中的箭头函数


// 传统函数表达式
const add = function(a, b) {
return a + b;
}

// 箭头函数
const add = (a, b) => a + b;
// 箭头函数有一个参数的时候可以省略小括号
const add = a => { return a + b};
// 箭头函数返回值只有一条语句时可以省略return和{}
const add = a => a + b;
// 温馨提示：const声明的变量是不能重复的，由于本人比较***，宁愿打字提醒也不愿意更改。

总结
箭头函数的特点
1、箭头函数有一个参数的时候可以省略小括号
2、箭头函数返回值只有一条语句时可以省略return和{}
3、箭头函数没有内置对象arguments
*4、箭头函数不是构造函数，不能构造实例化对象
5、箭头函数的this不能发生改变，call和apply能调用箭头函数
*6、箭头函数没有原型对象
7、箭头函数的this指向父作用域（定义他的地方）
————————————————

                        版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
原文链接：https://blog.csdn.net/weixin_62160709/article/details/136563611

## JavaScript中的反引号（键盘波浪号下面的符合）

```js
1、反引号`用法
(1)反引号可以换行const str = `this  is a \`string`
console.log(str)
(2)反引号里面可以格式化字符串→ ${}const name = "tom"
const str = `hey, ${name}, ${1 + 1}, ${Math.random()}`
console.log(str)
2、反引号与函数关系
(1)反引号还可以调用函数const name = 'zs';
const gender = true;
function myTagFunc(strings){
console.log(strings)
}
const str = myTagFunc`你好!${name}是一个${gender}`
[ ‘你好!’, ‘是一个’, ‘’ ]观察发现规律：反引号调用函数会自动将字符串分割为列表，并且是以${}为分隔符。如果最后以${}结尾，会多出一个’'，如果最后不是以${}结尾，则是这样的：(2)${}可以给函数传递参数const name = 'zs';
const gender = true;
function myTagFunc(strings,name,gender){
console.log(strings,name,gender)
}
const str = myTagFunc`你好!${name}是一个${gender}呀`
[ ‘你好!’, ‘是一个’, ‘呀’ ] zs true(3)拼接参数const name = '张三';
const gender = true;
function myTagFunc(strings,name,gender){
const sex = gender ? '男' : '女'; // 根据true或false判断gender方法，常用必记
return strings[0]+name+strings[1]+sex+strings[2]
}
const str = myTagFunc`你好!${name}是一个${gender}呀`
console.log(str);
你好!张三是一个男呀。
```
