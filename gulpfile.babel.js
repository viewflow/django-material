import autoprefixer from 'autoprefixer';
import gulp from 'gulp';
import postcss from 'gulp-postcss';
import sass from 'gulp-sass';

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
        browsers: [
          'Chrome >= 50',
          'Firefox >= 46',
          'Explorer >= 11',
          'Safari >= 9',
          'ChromeAndroid >= 50',
          'FirefoxAndroid >= 46',
        ]
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


gulp.task("default", [
  "materialize.js",
  "materialize.css",
  "roboto.font",
  "material-icons.font",
  "datatables.js",
]);
