import autoprefixer from 'autoprefixer'
import concat from 'gulp-concat'
import cssnano from 'cssnano';
import gulp from 'gulp'
import merge from 'merge-stream'
import postcss from 'gulp-postcss'
import pump from 'pump'
import sass from 'gulp-sass'
import uglify from 'gulp-uglify'
import babel from 'gulp-babel'

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
    'node_modules/jquery/dist/jquery.js',
    'node_modules/datatables.net-fixedheader/js/dataTables.fixedHeader.js',
    'node_modules/datatables.net-responsive/js/dataTables.responsive.js',
    'node_modules/datatables/media/js/jquery.dataTables.js',
    'node_modules/jquery-datetimepicker/build/jquery.datetimepicker.full.js',
    // 'node_modules/materialize-css/dist/js/materialize.js',
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


gulp.task('materialize.js', () => {
  return gulp.src('node_modules/materialize-css/js/**/*.js')
    .pipe(babel({presets: ['es2015']}))
    .pipe(concat('materialize.js'))
    .pipe(gulp.dest('./material/static/material/js/'));
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

gulp.task('frontend.min.js', ['materialize.js', '3rdparty.js'], (cb) => {
  var deps = [
    'material/static/material/js/turbolinks.js',
    'material/static/material/js/jquery.js',
    'material/static/material/js/jquery.dataTables.js',
    'material/static/material/js/jquery.activeNavigation.js',
    'material/static/material/js/jquery.datetimepicker.js',
    'material/static/material/js/jquery.formset.js',
    'material/static/material/js/perfect-scrollbar.jquery.js',
    'material/static/material/js/dataTables.fixedHeader.js',
    'material/static/material/js/dataTables.responsive.js',
    'material/static/material/js/materialize.js',
    'material/static/material/js/materialize.forms.js',
    'material/static/material/js/materialize.frontend.js',
  ]
  pump([
    gulp.src(deps),
    concat('materialize.frontend.min.js'),
    uglify(),
    gulp.dest('material/static/material/js/')], cb)
})

gulp.task('frontend.min.css', ['3rdparty.css', 'materialize.scss', 'materialize.django.scss'], () => {
  var deps = [
    'material/static/material/css/materialize.css',
    'material/static/material/css/materialize.forms.css',
    'material/static/material/css/materialize.frontend.css',
    'material/static/material/css/jquery.datetimepicker.css',
    'material/static/material/css/responsive.dataTables.css',
    'material/static/material/css/fixedHeader.dataTables.css',
    'material/static/material/css/perfect-scrollbar.css'
  ]

  return gulp.src(deps)
    .pipe(concat('materialize.frontend.min.css'))
    .pipe(postcss([
      cssnano()
    ]))
    .pipe(gulp.dest('material/static/material/css/'))
})

gulp.task('admin.min.js', ['materialize.js', '3rdparty.js'], (cb) => {
  var deps = [
    'material/static/material/js/jquery.datetimepicker.js',
    'material/static/material/js/jquery.formset.js',
    'material/static/material/js/jquery.dataTables.js',
    'material/static/material/js/dataTables.responsive.js',
    'material/static/material/js/dataTables.fixedHeader.js',
    'material/static/material/js/perfect-scrollbar.jquery.js',
    'material/static/material/js/materialize.js',
    'material/static/material/js/materialize.forms.js',
    'material/static/material/js/materialize.admin.js',
  ]
  pump([
    gulp.src(deps),
    concat('materialize.admin.min.js'),
    uglify(),
    gulp.dest('material/static/material/js/')], cb)
})

gulp.task('admin.min.css', ['3rdparty.css', 'materialize.scss', 'materialize.django.scss'], () => {
  var deps = [
    'material/static/material/css/materialize.css',
    'material/static/material/css/materialize.forms.css',
    'material/static/material/css/materialize.admin.css',
    'material/static/material/css/jquery.datetimepicker.css',
    'material/static/material/css/responsive.dataTables.css',
    'material/static/material/css/fixedHeader.dataTables.css',
    'material/static/material/css/perfect-scrollbar.css'
  ]

  return gulp.src(deps)
    .pipe(concat('materialize.admin.min.css'))
    .pipe(postcss([
      cssnano()
    ]))
    .pipe(gulp.dest('material/static/material/css/'))
})

gulp.task('default', [
  '3rdparty.fonts',
  '3rdparty.js',
  '3rdparty.css',
  'materialize.scss',
  'materialize.django.scss',
  'materialize.js',
  'frontend.min.js',
  'frontend.min.css',
  'admin.min.js',
  'admin.min.css',
])
