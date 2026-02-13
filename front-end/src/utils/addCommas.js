export function addCommas(input) {
	const number = Number(input);

	const withCommas = number
		.toString()
		.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

	return `${withCommas}\u00A0تومان`;
}
