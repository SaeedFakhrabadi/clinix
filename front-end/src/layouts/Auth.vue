<template>
	<div class="auth">
		<TheNavbar />
		<main class="auth__main-content">
			<router-view class="auth__form" />
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.auth {
		height: 100vh;

		&__main-content {
			height: 100%;
			padding-top: space(32);
			box-sizing: border-box;
			max-width: $xl;
			margin: 0 auto;
			@include flexbox(row, center, center);
		}

		&__form {
			width: 30%;
			background-color: var(--primary-800);
			box-shadow: space(0) space(0) space(5) var(--bg-400);
			padding: space(14);
			border-radius: space(14);
			@include flexbox(column, center, center, space(6));

			@media (max-width: $lg) {
				width: 40%;
			}
			@media (max-width: $md) {
				width: 50%;
			}
			@media (max-width: $sm) {
				width: 80%;
			}
		}
	}
</style>
