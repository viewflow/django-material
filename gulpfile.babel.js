import autoprefixer from 'autoprefixer';
import gulp from 'gulp';
import postcss from 'gulp-postcss';
import sass from 'gulp-sass';


var supported_browsers = [
  'Chrome >= 50',
  'Firefox >= 46',
  'Explorer >= 11',
  'Safari >= 9',
  'ChromeAndroid >= 50',
  'FirefoxAndroid >= 46',
];


gulp.task('material-icons.font', () => {
  return gulp.src('./node_modules/material-design-icons/iconfont/*')
    .pipe(gulp.dest('./material/static/material/fonts/material-design-icons/'));
});


gulp.task('roboto.font', () => {
  return gulp.src('./node_modules/materialize-css/fonts/roboto/*')
    .pipe(gulp.dest('./material/static/material/fonts/roboto/'));
});



gulp.task('materialize.js', () => {
  return gulp.src('./node_modules/materialize-css/dist/js/materialize.js')
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('materialize.css', () => {
  return gulp.src('./material/static/material/sass/*.scss')
    .pipe(sass({
      includePaths: './node_modules/'
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: supported_browsers
      })
    ]))
    .pipe(gulp.dest(
      './material/static/material/css/'
    ));
});


gulp.task('datatables.js', () => {
  return gulp.src('./node_modules/datatables/media/js/jquery.dataTables.js')
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('datatables.fixedHeader.js', () => {
  return gulp.src('./node_modules/datatables.net-fixedheader/js/dataTables.fixedHeader.js')
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('datatables.responsive.js', () => {
  return gulp.src('./node_modules/datatables.net-responsive/js/dataTables.responsive.js')
    .pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('frontend.css', () => {
  return gulp.src('./material/frontend/static/material/frontend/sass/*.scss')
    .pipe(sass({
      includePaths: ['./node_modules/', './material/static/']
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: supported_browsers
      })
    ]))
    .pipe(gulp.dest(
      './material/frontend/static/material/frontend/css/'
    ));
});


gulp.task('admin.css', () => {
  return gulp.src('./material/admin/static/material/admin/sass/*.scss')
    .pipe(sass({
      includePaths: ['./node_modules/', './material/static/']
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: supported_browsers
      })
    ]))
    .pipe(gulp.dest(
      './material/admin/static/material/admin/css/'
    ));
});


gulp.task("default", [
  "materialize.js",
  "materialize.css",
  "roboto.font",
  "material-icons.font",
  "datatables.js",
  "datatables.fixedHeader.js",
  "datatables.responsive.js",
  "frontend.css",
  "admin.css",
]);
