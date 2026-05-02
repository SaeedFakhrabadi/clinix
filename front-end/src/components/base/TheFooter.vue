<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits';
</script>

<template>
	<footer class="the-footer">
		<h4 class="the-footer__copyright">
			© تمامی حقوق محفوظ است ({{ toPersianDigits('1404') }})
		</h4>
	</footer>
</template>

<style lang="scss" scoped>
	.the-footer {
		width: 100vw;
		height: space(48);
		padding-block: space(8);
		box-sizing: border-box;
		background-color: var(--text-200);
		@include flexbox(column, center, center);

		&__copyright {
			color: var(--bg-900);
		}
	}
</style>
