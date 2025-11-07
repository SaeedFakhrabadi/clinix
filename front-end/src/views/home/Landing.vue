<script setup>
	const scrollToContent = () => {
		const content = document.querySelector('.home__content');
		if (content) {
			content.scrollIntoView({ behavior: 'smooth' });
		}
	};
</script>

<template>
	<div class="home">
		<header class="home__header">
			<h1 class="home__slogan">کلینیکس، بزرگترین سامانه آنلاین مدیریت و رزرو نوبت کلینیک های پزشکی</h1>
			<h3 class="home__sub-slogan">برای رزرو نوبت کلیک کنید</h3>
			<TheButton type="big" label="ثبت نوبت" width="100" @click="scrollToContent" />
		</header>
		<div class="home__content"></div>
	</div>
</template>

<style lang="scss" scoped>
	.home {
		&__header {
			background-image: linear-gradient(45deg, var(--secondary-400), var(--primary-600));
			width: 100%;
			height: space(320);
			@include flexbox(column, center, center, space(20));
		}

		&__slogan {
			background-image: linear-gradient(45deg, var(--text-900), var(--text-400));
			background-clip: text;
			-webkit-text-fill-color: transparent;
			animation: subtle-shake 3s infinite alternate ease-in-out;
			@media (max-width: space(600)) {
				display: none;
			}
		}

		@keyframes subtle-shake {
			0% {
				transform: translate(space(0), space(0));
			}
			25% {
				transform: translate(space(1), space(1));
			}
			50% {
				transform: translate(space(1), space(-1));
			}
			75% {
				transform: translate(space(-1), space(1));
			}
			100% {
				transform: translate(space(-1), space(-1));
			}
		}

		&__sub-slogan {
			color: var(--text-700);
		}

		&__content {
			@include flexbox(column, center, right);
		}
	}
</style>
