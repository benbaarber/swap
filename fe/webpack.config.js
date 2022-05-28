const path = require("path");
const express = require("express");
const bodyParser = require("body-parser");

module.exports = {
  entry: path.resolve(__dirname, "src", "App.jsx"),
  mode: "development",
  module: {
    rules: [
      {
        test: /\.(js|jsx)/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.(css)/,
        exclude: /node_modules/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|jpe?g|gif|svg|woff2?|ttf)$/i,
        exclude: /node_modules/,
        use: "file-loader",
      },
    ],
  },
  output: {
    publicPath: "/",
    filename: "bundle.js",
    path: path.resolve(__dirname, "build"),
  },
  resolve: {
    extensions: [".css", ".js", ".jsx"],
  },
  // plugins: [new webpack.HotModuleReplacementPlugin()],
  devServer: {
    static: {
      directory: path.join(__dirname, 'build'),
    },
    compress: true,
    port: 9000,
  },
};
