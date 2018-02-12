const path = require('path');
const copyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const ExtraneousFileCleanupPlugin = require('webpack-extraneous-file-cleanup-plugin');


const BABEL_LOADER_CONFIG = {
  test: /\.js$/,
  exclude: [
    /node_modules/,
  ],
  use: [
    {loader: 'babel-loader'},
  ],
};

const extractSass = new ExtractTextPlugin({
  filename: 'css/[name].min.css',
  allChunks: true,
});

const SASS_LOADER_CONFIG = {
  test: /\.scss$/,
  use: extractSass.extract({
    use: [{
      loader: 'css-loader',
      options: {
        minimize: true,
        sourceMap: true,
      },
    }, {
      loader: 'sass-loader',
      options: {
        sourceMap: true,
        includePaths: [path.resolve(__dirname, 'node_modules')],
      },
    }],
  }),
};

const THEMES_CONFIG = {
  entry: {
    'django-material-theme-amber': './material/components/themes/theme-amber.scss',
    'django-material-theme-bluegrey': './material/components/themes/theme-bluegrey.scss',
    'django-material-theme-blue': './material/components/themes/theme-blue.scss',
    'django-material-theme-brown': './material/components/themes/theme-brown.scss',
    'django-material-theme-cyan': './material/components/themes/theme-cyan.scss',
    'django-material-theme-deeporange': './material/components/themes/theme-deeporange.scss',
    'django-material-theme-deeppurple': './material/components/themes/theme-deeppurple.scss',
    'django-material-theme-green': './material/components/themes/theme-green.scss',
    'django-material-theme-indigo': './material/components/themes/theme-indigo.scss',
    'django-material-theme-lightblue': './material/components/themes/theme-lightblue.scss',
    'django-material-theme-lightgreen': './material/components/themes/theme-lightgreen.scss',
    'django-material-theme-lime': './material/components/themes/theme-lime.scss',
    'django-material-theme-orange': './material/components/themes/theme-orange.scss',
    'django-material-theme-pink': './material/components/themes/theme-pink.scss',
    'django-material-theme-purple': './material/components/themes/theme-purple.scss',
    'django-material-theme-red': './material/components/themes/theme-red.scss',
    'django-material-theme-teal': './material/components/themes/theme-teal.scss',
    'django-material-theme-yellow': './material/components/themes/theme-yellow.scss',
  },

  output: {
    filename: 'obsolete-[name].js',
    path: path.resolve(__dirname, 'material/static/material'),
  },

  module: {
    rules: [SASS_LOADER_CONFIG],
  },

  plugins: [
    extractSass,
    new ExtraneousFileCleanupPlugin({
      extensions: ['.js'],
      minBytes: 4096,
    }),
  ],
};

const COMPONENTS_CONFIG = {
  entry: {
    'django-material-components': './material/components/index.js',
  },

  output: {
    filename: 'js/[name].min.js',
    path: path.resolve(__dirname, 'material/static/material'),
    library: 'frontend',
    libraryTarget: 'umd',
  },

  devtool: 'source-map',

  module: {
    rules: [BABEL_LOADER_CONFIG, SASS_LOADER_CONFIG],
  },

  externals: {
    '@material': 'mdc',
    'stimulus': 'Stimulus',
    'turbolinks': 'Turbolinks',
  },

  plugins: [
    extractSass,
    copyWebpackPlugin([
      {
        from: 'node_modules/turbolinks/dist/turbolinks.js',
        to: 'js/turbolinks.min.js',
      },
      {
        from: 'node_modules/material-components-web/dist/material-components-web.min.js',
        to: 'js/',
      },
      {
        from: 'node_modules/material-components-web/dist/material-components-web.min.css',
        to: 'css/',
      },
      {
        from: 'node_modules/stimulus/dist/stimulus.umd.js',
        to: 'js/stimulus.min.js',
      },
      {
        from: './node_modules/material-design-icons/iconfont/',
        to: 'fonts/material-design-icons/',
      },
      {
        from: './node_modules/roboto-npm-webfont/full/',
        to: 'fonts/roboto/',
      },
    ]),
  ],
};

module.exports = [
  COMPONENTS_CONFIG,
  THEMES_CONFIG,
];
