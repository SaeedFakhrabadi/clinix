export function toEnglishDigits(input) {
	if (typeof input !== 'string')
		return input.toString().replace(/\d/g, (d) => '0123456789'[d]);
	return input.replace(/\d/g, (d) => '0123456789'[d]);
}
