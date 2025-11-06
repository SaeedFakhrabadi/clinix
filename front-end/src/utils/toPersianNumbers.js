export function toPersianNumbers(input) {
  return input.toString().replace(/\d/g, (d) => '۰۱۲۳۴۵۶۷۸۹'[d]);
}
