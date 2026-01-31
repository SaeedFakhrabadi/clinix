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
			height: calc(100% - space(32));
			padding-top: space(32);
			max-width: space(650);
			margin: 0 auto;
			@include flexbox(row, center, center);
		}

		&__form {
			width: 30%;
			background-color: var(--primary-700);
			box-shadow: space(0) space(0) space(3) var(--text-900);
			padding: space(14);
			border-radius: space(14);
			@include flexbox(column, center, center, space(10));
			@media (max-width: space(496)) {
				width: 40%;
			}
			@media (max-width: space(384)) {
				width: 50%;
			}
			@media (max-width: space(288)) {
				width: 80%;
			}
		}
	}
</style>
