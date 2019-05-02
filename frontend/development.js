import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';

const src = path.resolve(__dirname, 'src');
const dist = path.resolve(__dirname, 'dist');

export default {
  mode: 'development',
  entry: src + '/js/index.js',

  output: {
    path: dist,
    filename: 'bundle.js'
  },

  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: ['/node_modules/', '/Dockerfile$/'],
        loader: 'babel-loader'
      },
      {
        test: /\.js$/,
        exclude: ['/node_modules/', '/Dockerfile$/'],
        loader: 'babel-loader'
      }
    ]
  },

  resolve: {
    extensions: ['.js', '.jsx']
  },

  devServer: {
    inline: true,
    contentBase: dist,
    watchContentBase: true,
    hot: true,
    open: true,
    port: 8888
  },

  plugins: [
  ]
};
