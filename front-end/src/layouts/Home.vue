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
			height: 100vh;
			padding-top: space(32);
			box-sizing: border-box;
			@include flexbox(row, start, start, space(0));
		}

		&__content {
			width: $xl;
			min-height: calc(100vh - space(80));
			box-sizing: border-box;
			margin-inline: auto;
			padding: space(8) space(6);
			background-color: var(--bg-700);
			@include flexbox(column, start, start, space(10), nowrap);
		}
	}
</style>
