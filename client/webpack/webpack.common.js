const Path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    app: Path.resolve(__dirname, '../src/index.jsx'),
  },
  output: {
    path: Path.join(__dirname, '../build'),
    filename: 'js/[name].js',
    clean: true,
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [{ from: Path.resolve(__dirname, '../public'), to: './' }],
    }),
  ],
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    alias: {
      '~': Path.resolve(__dirname, '../src'),
    },
  },
  module: {
    rules: [
      {
        test: /\.mjs$/,
        include: /node_modules/,
        type: 'javascript/auto',
      },
      {
        test: /\.html$/i,
        loader: 'html-loader',
      },
      {
        test: /\.s?css$/i,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          'postcss-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.s?css/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],
      },
      {
        test: /\.(ico|jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2)(\?.*)?$/,
        type: 'asset'
      },
    ],
  },
};
