var path = require('path')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require("extract-text-webpack-plugin")


var extractSass = new ExtractTextPlugin({
    filename: "[name]-[contenthash].css",
});

module.exports = {
  context: __dirname,
  entry: {
    django_material: ['babel-polyfill', './material/static/material/django_material.js'],
  },
  output: {
    path: path.resolve('./material/static/webpack_bundles/'),
    filename: '[name]-[hash].js'
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    extractSass,
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        //exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['babel-preset-env']
          }
        }
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /\.scss$/,
        use: extractSass.extract({
          use: [{
            loader: "css-loader"
          }, {
            loader: "sass-loader",
            options: {
              includePaths: ['./node_modules/']
            }
          }]
        })
      }
    ]
  }
}
