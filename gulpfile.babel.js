import autoprefixer from 'autoprefixer'
import gulp from 'gulp'
import postcss from 'gulp-postcss'
import sass from 'gulp-sass'
import merge from 'merge-stream'

var supportedBrowsers = [
  'Chrome >= 50',
  'Firefox >= 46',
  'Explorer >= 11',
  'Safari >= 9',
  'ChromeAndroid >= 50',
  'FirefoxAndroid >= 46'
]

gulp.task('3rdparty.fonts', () => {
  return merge(
    gulp.src('./node_modules/material-design-icons/iconfont/*')
      .pipe(gulp.dest('./material/static/material/fonts/material-design-icons/')),
    gulp.src('./node_modules/materialize-css/fonts/roboto/*')
      .pipe(gulp.dest('./material/static/material/fonts/roboto/'))
  )
})

gulp.task('3rdparty.js', () => {
  var deps = [
    'node_modules/datatables.net-fixedheader/js/dataTables.fixedHeader.js',
    'node_modules/datatables.net-responsive/js/dataTables.responsive.js',
    'node_modules/datatables/media/js/jquery.dataTables.js',
    'node_modules/jquery-datetimepicker/build/jquery.datetimepicker.full.js',
    'node_modules/materialize-css/dist/js/materialize.js',
    'node_modules/perfect-scrollbar/dist/js/perfect-scrollbar.jquery.js',
    'node_modules/turbolinks/dist/turbolinks.js'
  ]

  return gulp.src(deps)
    .pipe(gulp.dest('./material/static/material/js/'))
})

gulp.task('3rdparty.css', () => {
  var deps = [
    './node_modules/datatables.net-fixedheader-dt/css/fixedHeader.dataTables.css',
    './node_modules/datatables.net-responsive-dt/css/responsive.dataTables.css',
    './node_modules/jquery-datetimepicker/jquery.datetimepicker.css',
    './node_modules/perfect-scrollbar/dist/css/perfect-scrollbar.css'
  ]
  return gulp.src(deps)
    .pipe(gulp.dest('./material/static/material/css/'))
})

gulp.task('materialize.scss', () => {
  return gulp.src('./material/static/material/sass/*.scss')
    .pipe(sass({
      includePaths: './node_modules/'
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: supportedBrowsers
      })
    ]))
    .pipe(gulp.dest(
      './material/static/material/css/'
    ))
})

gulp.task('materialize.django.scss', () => {
  return gulp.src('./material/static/material/sass/*.scss')
    .pipe(sass({
      includePaths: ['./node_modules/', './material/static/']
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: supportedBrowsers
      })
    ]))
    .pipe(gulp.dest(
      './material/static/material/css/'
    ))
})

gulp.task('default', [
  '3rdparty.fonts',
  '3rdparty.js',
  '3rdparty.css',
  'materialize.scss',
  'materialize.django.scss'
])
