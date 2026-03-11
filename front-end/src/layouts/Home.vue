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
			overflow: auto;
			@include flexbox(row, start, start, space(0));

			@media (min-width: $xl) {
				padding-right: space(6);
			}
		}

		&__content {
			width: 100%;
			margin-inline: auto;
			max-width: $xl;
			padding-block: space(8);

			@media (max-width: $xl) {
				padding-inline: space(6);
			}
		}
	}
</style>
