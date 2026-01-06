<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits.js';
</script>

<template>
	<div class="dashboard">
		<TheNavbar />
		<router-view class="dashboard__content" />
		<footer class="dashboard__footer footer">
			<div class="footer__title">
				<h4>ساخته شده با عشق توسط تیم کلینیکس</h4>
			</div>
			<p class="footer__copyright">
				&copy; تمامی حقوق محفوظ است ({{ toPersianDigits(1404) }})
			</p>
		</footer>
	</div>
</template>

<style lang="scss" scoped>
	.dashboard {
		&__content {
			padding-top: space(50);
			margin: 0 auto;
			max-width: space(650);
			@include flexbox(row, start, start, space(0));
		}

		.footer {
			background-color: var(--primary-800);
			padding: space(10) space(0);
			color: var(--text-600);
			border-top: 1px solid var(--text-100);
			@include flexbox(column, center, center, space(2));

			&__title {
				@include flexbox(row, center, center, space(2));
			}

			&__copyright {
				opacity: 0.6;
			}
		}
	}
</style>
