<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits.js';
</script>

<template>
	<div class="dashboard">
		<NavigationBar />
		<router-view class="dashboard__content" />
		<footer class="dashboard__footer">
			<div class="dashboard__footer-title">
				<h4>ساخته شده با عشق توسط تیم کلینیکس</h4>
			</div>
			<p class="dashboard__footer-copyright">&copy; تمامی حقوق محفوظ است ({{ toPersianDigits(1404) }})</p>
		</footer>
	</div>
</template>

<style lang="scss" scoped>
	.dashboard {
		&__content {
			@include flexbox(Column, center, center, space(0));
		}

		&__footer {
			background-color: var(--primary-800);
			padding: space(10) space(0);
			color: var(--text-600);
			border-top: 1px solid var(--text-100);
			@include flexbox(column, center, center, space(2));
		}

		&__footer-title {
			@include flexbox(row, center, center, space(2));
		}

		&__footer-image {
			width: space(10);
			height: space(10);
		}

		&__footer-copyright {
			opacity: 0.6;
		}
	}
</style>
