# フロントビルド手順 

## 開発用ビルド 
1. distの中身にまず再配布不可ファイルを含めたZipの中身をおいておく 
2. distの中身を消さずに `webpack --mode development` 
3. バグでindex.htmlにscriptタグが余計に生成されるので消す 