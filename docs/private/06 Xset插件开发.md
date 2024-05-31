# 1 参考资料
https://www.npmjs.com/package/@stanislav.domb/several-dimension-multi-line-chart
# 2 several-dimension-multi-line-chart

This is the "Several Dimension Multi Line Chart" Superset Chart Plugin.

### 2.1.1 [](https://www.npmjs.com/package/@stanislav.domb/several-dimension-multi-line-chart#usage)Usage

To install Superset you can use this resurses:

```
https://preset.io/blog/building-custom-viz-plugins-in-superset-v2/
https://github.com/nielsen-oss/superset-viz-plugins/blob/master/plugins/plugin-chart-status/src/plugin/controlPanel.ts
https://www.youtube.com/watch?v=sS-P2OI0fgk

```

After creating the new plugin (folders and files), inside root directory:

```
npm i

```

To run the plugin in development mode (=rebuilding whenever changes are made), App starts on localhost port: [http://localhost:9000/](http://localhost:9000/) Start the dev server with the following command:

```
npm start

```

To add the package to Superset, go to the `superset-frontend` subdirectory in your Superset source folder (assuming both the `superset-plugin-several-dimension` plugin and `superset` repos are in the same root directory) and run

```
npm i -S ../../several-dimension-multi-line-chart
```

After this edit the `superset-frontend/src/visualizations/presets/MainPreset.js` and make the following changes:

```js
import { SeveralDimensionMultiLineChartPlugin } from 'several-dimension-multi-line-chart';
```

to import the plugin and later add the following to the array that's passed to the `plugins` property:

```js
new SeveralDimensionMultiLineChartPlugin().configure({
    key: 'several-dimension-multi-line-chart',
    }),
```

After that the plugin should show up when you run Superset, e.g. the development server:

```
npm run dev-server
```

It's possible, to use your new plugin as additional package. And you can publish the plugin to the npm repo and for installing you should have it in package.json:

```
"@stanislav.domb/several-dimension-multi-line-chart": "^0.1.1",
```

### 2.1.2 [](https://www.npmjs.com/package/@stanislav.domb/several-dimension-multi-line-chart#hint-for-plugin-usage)Hint for plugin usage

- If you need an additional line on the chart add data to "METRICS"
- If you need an additional chart add data to "COLUMNS" (filtering works only by one column)
- Filter by date works as usual
# 3 hello world 2
![[Pasted image 20240524145613.png]]
## 3.1 第一步：
```bash
npm i -g yo
cd superset-frontend/packages/generator-superset
npm i
npm link
```
## 3.2 第二步：安装yo
npm install -g yo
安装yo后无法使用：
需要配置环境变量，node的bin目录到path中。因为node 18版本已经没有bin目录，目的就是找到运行的二进制文件，因此只要添加此路径到path中就ok了。
![[Pasted image 20240524152645.png]]
![[Pasted image 20240524152702.png]]
![[Pasted image 20240524152716.png]]
## 3.3 第三步
```bash
mkdir /tmp/superset-plugin-chart-hello-world
cd /tmp/superset-plugin-chart-hello-world
yo @superset-ui/superset
```

# 4 ? npm link, yo @superset-ui/superset

![[Pasted image 20240524163705.png]]