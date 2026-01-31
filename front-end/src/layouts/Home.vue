<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits.js';
</script>

<template>
	<div class="home">
		<TheNavbar />
		<main class="home__main-content">
			<router-view class="home__content" />
			<footer class="home__footer footer">
				<div class="footer__title">
					<h4>ساخته شده با عشق توسط تیم کلینیکس</h4>
				</div>
				<p class="footer__copyright">
					&copy; تمامی حقوق محفوظ است ({{ toPersianDigits(1404) }})
				</p>
			</footer>
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.home {
		&__main-content {
			height: calc(100vh - space(32));
			padding-top: space(32);
			margin: 0 auto;
			overflow: auto;
			max-width: space(650);
			@include flexbox(row, start, start, space(0));
		}

		&__content {
			padding-top: space(20);
			@include flexbox(row, start, start, space(0));
		}

		.footer {
			background-color: var(--primary-800);
			padding: space(10) space(0);
			color: var(--text-600);
			width: 100%;
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
