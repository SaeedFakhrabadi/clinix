<template>
	<div>
		<NavigationBar />
		<div class="container"><router-view class="container__form" /></div>
	</div>
</template>

<style lang="scss" scoped>
	.container {
		height: 91vh;
		transition: none;
		@include flexbox();

		&__form {
			width: 20%;
			background-color: var(--primary-200);
			box-shadow: space(0) space(0) space(5) var(--text-900);
			padding: space(14);
			border-radius: space(14);
			@media (max-width: space(600)) {
				width: 30%;
			}
			@media (max-width: space(450)) {
				width: 40%;
			}
			@media (max-width: space(300)) {
				width: 80%;
			}
		}
	}
</style>
