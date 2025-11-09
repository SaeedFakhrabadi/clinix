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
			<h1 class="home__slogan">کلینیکس، بزرگترین کلینیک آنلاین برای مدیریت و رزرو نوبت پزشکی</h1>
			<h3 class="home__sub-slogan">همین الآن برای رزرو نوبت کلیک کنید</h3>
			<TheButton type="big" label="رزرو نوبت" width="100px" @click="scrollToContent" />
		</header>
		<div class="home__content"></div>
	</div>
</template>

<style lang="scss" scoped>
	.home {
		&__header {
			background-image: linear-gradient(0deg, var(--primary-600), var(--bg-900));
			width: 100%;
			height: space(300);
			@include flexbox(column, center, center, space(20));
		}

		&__slogan {
			color: var(--text-900);
			animation: subtle-shake 3s infinite alternate ease;
			@include flexbox(row, center, center, space(0), wrap);
		}

		@keyframes subtle-shake {
			0% {
				transform: translate(space(0), space(0));
			}
			25% {
				transform: translate(space(0), space(2));
			}
			50% {
				transform: translate(space(0), space(0));
			}
			75% {
				transform: translate(space(0), space(2));
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
