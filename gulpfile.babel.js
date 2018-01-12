import addsrc from 'gulp-add-src';
import autoprefixer from 'autoprefixer';
import babel from 'gulp-babel';
import cleanCSS from 'gulp-clean-css';
import concat from 'gulp-concat';
import gulp from 'gulp';
import postcss from 'gulp-postcss';
import rename from 'gulp-rename';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';
import uglify from 'gulp-uglify';

let supportedBrowsers = ['last 2 versions'];

let babelOpts = {
  'presets': [
    ['env', {
      'targets': {
        'browsers': supportedBrowsers,
      }},
    ],
  ],
  'plugins': [
    ['transform-class-properties', {
      'spec': true,
    }],
  ],
};


gulp.task('turbolinks', () => {
  return gulp.src('node_modules/turbolinks/dist/turbolinks.js')
    .pipe(rename('turbolinks.min.js'))
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('material-components-web', () => {
  let js = gulp.src('node_modules/material-components-web/dist/material-components-web.min.js')
    .pipe(gulp.dest('./material/static/material/js/'));

  let css = gulp.src('node_modules/material-components-web/dist/material-components-web.min.css')
    .pipe(gulp.dest('./material/static/material/css/'));

  let icons = gulp.src('./node_modules/material-design-icons/iconfont/*')
    .pipe(gulp.dest('./material/static/material/fonts/material-design-icons/'));

  let roboto = gulp.src('./node_modules/roboto-npm-webfont/full/**/*')
    .pipe(gulp.dest('./material/static/material/fonts/roboto/'));

  return [js, css, icons, roboto];
});


gulp.task('django-material-css', () => {
  return gulp.src('./material/static/material/sass/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass({includePaths: './node_modules/'})
    .on('error', sass.logError))
    .pipe(postcss([
      autoprefixer({
        browsers: supportedBrowsers,
      }),
    ]))
    .pipe(cleanCSS())
    .pipe(rename(function(path) {
      path.extname = '.min.css';
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/css/'));
});


gulp.task('django-material-forms', () => {
  gulp.src('./material/static/material/components/forms/*.js')
    .pipe(sourcemaps.init())
    .pipe(
      addsrc.prepend('./material/static/material/components/registry.js'))
    .pipe(babel(babelOpts))
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(concat('django-material-forms.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('django-material-frontend', () => {
  gulp.src('./material/static/material/components/frontend/*.js')
    .pipe(sourcemaps.init())
    .pipe(babel(babelOpts))
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(concat('django-material-frontend.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('django-material-frontend-profile', () => {
  gulp.src('./material/static/material/components/pages/profile.js')
    .pipe(sourcemaps.init())
    .pipe(babel(babelOpts))
    .pipe(
      addsrc.prepend([
        './material/static/material/components/umd_local.js',
        'node_modules/smartcrop/smartcrop.js',
        ]))
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(concat('django-material-frontend-profile.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('default', [
  'turbolinks',
  'material-components-web',
  'django-material-css',
  'django-material-forms',
  'django-material-frontend',
  'django-material-frontend-profile',
]);
