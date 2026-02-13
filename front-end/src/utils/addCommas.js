import { toPersianDigits } from '@/utils/toPersianDigits';

export function addCommas(input) {
	const number = Number(input);
	const withCommas = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	return toPersianDigits(`${withCommas}\u00A0تومان`);
}
