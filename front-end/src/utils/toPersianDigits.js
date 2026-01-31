export function toPersianDigits(input) {
	if (typeof input !== 'string')
		return input.toString().replace(/\d/g, (d) => '۰۱۲۳۴۵۶۷۸۹'[d]);
	return input.replace(/\d/g, (d) => '۰۱۲۳۴۵۶۷۸۹'[d]);
}
