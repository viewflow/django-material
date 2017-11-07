import babel from 'gulp-babel'
import concat from 'gulp-concat'
import gulp from 'gulp'
import sass from 'gulp-sass'
import sourcemaps from 'gulp-sourcemaps'

gulp.task('mdc.js', () => {
    return gulp.src([
        'node_modules/material-components-web/dist/material-components-web.js'
    ]).pipe(gulp.dest('./material/static/material/js/'))
})

gulp.task('mdc.css', () => {
  return gulp.src([
    'node_modules/material-components-web/dist/material-components-web.css'
  ]).pipe(gulp.dest('./material/static/material/css/'))
})

gulp.task('mdc.font', () => {
    return gulp.src([
        './node_modules/material-design-icons/iconfont/*'
    ]).pipe(
        gulp.dest('./material/static/material/fonts/material-design-icons/')
    )
})

gulp.task('roboto.font', () => {
  return gulp.src([
      './node_modules/roboto-npm-webfont/full/**/*'
  ]).pipe(
      gulp.dest('./material/static/material/fonts/roboto/')
  )
})

gulp.task('dmc.scss', () => {
    return gulp.src([
        './material/static/material/sass/*.scss'
    ]).pipe(sass({
        includePaths: './node_modules/'
    }).on(
      'error', sass.logError
    )).pipe(gulp.dest(
      './material/static/material/css/'
    ))
})

gulp.task('dmc.js', () => {
  return gulp.src('./material/static/material/components/*.js')
    .pipe(sourcemaps.init())
    .pipe(
      babel({
        presets: [
          ['env', {
            "targets": {
              "browsers": ["last 2 versions"]
            }}
          ]
        ],
        "plugins": [
          ["transform-es2015-modules-umd", {
            "globals": {
              "material-components-web": "mdc"
            }
          }]
        ]
    }))
    .pipe(concat('django-material-components.js'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/js/'))
})


gulp.task('default', [
    'mdc.js',
    'mdc.css',
    'mdc.font',
    'roboto.font',
    'dmc.scss',
    'dmc.js',
])
