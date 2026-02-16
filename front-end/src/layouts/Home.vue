<script setup></script>

<template>
	<div class="home">
		<TheNavbar />
		<main class="home__main-content">
			<router-view class="home__content" />
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
			max-width: $xl;
			@include flexbox(row, start, start, space(0));
		}

		&__content {
			width: 100%;
			padding-block: space(8);

			@media (max-width: $xl) {
				padding-inline: space(6);
			}
		}
	}
</style>
