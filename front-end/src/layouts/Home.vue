<script setup></script>

<template>
	<div class="home">
		<TheNavbar />
		<main class="home__main-content">
			<router-view class="home__content" />
			<TheFooter />
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.home {
		&__main-content {
			height: calc(100vh - space(32));
			padding-top: space(32);
			@include flexbox(row, start, start, space(0));
		}

		&__content {
			width: calc($xl - space(12));
			min-height: calc(100% - space(80));
			max-width: $xl;
			margin-inline: auto;
			padding: space(8) space(6);
			background-color: var(--primary-700);
			@include flexbox(column, start, start, space(10), nowrap);
		}
	}
</style>
