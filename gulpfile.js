const postcss = require("gulp-postcss");
const gulpSass = require("gulp-sass")
const dartSass = require("sass")
const sass = gulpSass(dartSass)
const { src, dest, parallel, watch } = require("gulp");

const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");

function defaultTask() {
  return src("assets/**/*.scss")
    .pipe(sass())
    .pipe(postcss([autoprefixer(), cssnano()]))
    .pipe(dest("kyrios/static/css"));
}

exports.default = parallel(defaultTask);
exports.watch = () => {
  watch(["assets/**/*.scss"], defaultTask);
};
