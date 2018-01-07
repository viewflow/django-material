import babel from 'gulp-babel';
import concat from 'gulp-concat';
import gulp from 'gulp';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';

function compileJs(gulpSrc, dst) {
  return gulpSrc
    .pipe(sourcemaps.init())
    .pipe(
      babel({
        'presets': [
          ['env', {
            'targets': {
              'browsers': ['last 2 versions'],
            }},
          ],
        ],
        'plugins': [
          ['transform-class-properties', {
            'spec': true,
          }],
        ],
    }))
    .pipe(concat(dst))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./material/static/material/js/'));
}

gulp.task('3d-party.js', () => {
  const deps = [
    'node_modules/turbolinks/dist/turbolinks.js',
  ];
  return gulp.src(deps).pipe(gulp.dest('./material/static/material/js/'));
});


gulp.task('mdc.js', () => {
    return gulp.src([
        'node_modules/material-components-web/dist/material-components-web.js',
    ]).pipe(gulp.dest('./material/static/material/js/'));
});

gulp.task('mdc.css', () => {
  return gulp.src([
    'node_modules/material-components-web/dist/material-components-web.css',
  ]).pipe(gulp.dest('./material/static/material/css/'));
});

gulp.task('mdc.font', () => {
    return gulp.src([
        './node_modules/material-design-icons/iconfont/*',
    ]).pipe(
        gulp.dest('./material/static/material/fonts/material-design-icons/')
    );
});

gulp.task('roboto.font', () => {
  return gulp.src([
      './node_modules/roboto-npm-webfont/full/**/*',
  ]).pipe(
      gulp.dest('./material/static/material/fonts/roboto/')
  );
});

gulp.task('dmc.scss', () => {
    return gulp.src([
        './material/static/material/sass/*.scss',
    ]).pipe(sass({
        includePaths: './node_modules/',
    }).on(
      'error', sass.logError
    )).pipe(gulp.dest(
      './material/static/material/css/'
    ));
});

gulp.task('dmc.js', () => {
  return compileJs(
    gulp.src('./material/static/material/components/*.js'),
    'django-material-components.js'
  );
});

gulp.task('django-material-registry.js', () => {
  return compileJs(
    gulp.src('./material/static/material/scripts/django-material-registry.js'),
    'django-material-registry.js'
  );
});
gulp.task('profile.js', () => {
  return compileJs(
    gulp.src([
      'node_modules/smartcrop/smartcrop.js',
      './material/static/material/scripts/profile.js',
    ]),
    'django-material-frontend-profile.js'
  );
});


gulp.task('default', [
    '3d-party.js',
    'mdc.js',
    'mdc.css',
    'mdc.font',
    'roboto.font',
    'dmc.scss',
    'django-material-registry.js',
    'dmc.js',
    'profile.js',
]);
