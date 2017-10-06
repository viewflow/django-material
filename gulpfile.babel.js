import gulp from 'gulp'
import sass from 'gulp-sass'

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
  

gulp.task('default', [
    'mdc.js',
    'mdc.css',
    'mdc.font',
    'dmc.scss',
])
