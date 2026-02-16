<script setup>
	import { useRouter } from 'vue-router';

	const router = useRouter();
</script>

<template>
	<div class="landing">
		<header class="landing__header header">
			<h1 class="header__slogan">
				کلینیکس، بزرگترین کلینیک آنلاین مدیریت و رزرو نوبت های پزشکی
			</h1>
			<h3 class="header__sub-slogan">
				همین الآن برای مشاهده لیست پزشکان و رزرو نوبت کلیک کنید
			</h3>
			<TheButton
				class="header__button"
				type="submit"
				label="مشاهده لیست پزشکان"
				@click="() => router.push({ name: 'DoctorsList' })"
			/>
		</header>
		<main class="home__content content">
			<h2 class="content__title">درباره ما</h2>
			<p class="content__about-us">
				کلینیکس جایی است که سلامت، تخصص و آرامش در کنار هم معنا پیدا می‌کنند. ما
				در کلینیکس با بهره‌گیری از تیمی مجرب از پزشکان و کادر درمانی حرفه‌ای،
				تلاش می‌کنیم تجربه‌ای متفاوت و مطمئن از خدمات درمانی را برای مراجعان
				فراهم کنیم. در کلینیکس، تمرکز ما بر ارائه خدمات دقیق، به روز و مبتنی بر
				استاندارد های علمی است. از مشاوره‌های تخصصی گرفته تا خدمات تشخیصی و
				درمانی، همه چیز با هدف ارتقای کیفیت زندگی شما طراحی شده است. فضای مدرن و
				آرام کلینیک نیز به گونه‌ای آماده شده تا مراجعان در محیطی امن و صمیمی
				خدمات مورد نیاز خود را دریافت کنند.
			</p>
			<p class="content__about-us">
				ما باور داریم که هر مراجعه‌کننده نیازها و شرایط منحصربه‌فردی دارد. به
				همین دلیل، در کلینیکس رویکرد ما شخصی‌سازی خدمات درمانی و همراهی کامل در
				مسیر بهبود است. پاسخگویی دقیق، نوبت‌دهی منظم و احترام به زمان بیماران از
				اصول اصلی کار ماست. کلینیکس فقط یک مرکز درمانی نیست؛ بلکه همراهی قابل
				اعتماد برای حفظ و ارتقای سلامت شماست.
			</p>
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.landing {
		@include flexbox(column, center, center, space(10));

		.header {
			width: 100%;
			background-color: var(--bg-600);
			padding-block: space(10);
			text-align: center;
			@include flexbox(column, center, center, space(20));

			&__slogan {
				color: var(--title-500);
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
				color: var(--title-100);
			}

			&__button {
				width: space(80);
				height: space(30);
			}
		}

		.content {
			width: 100%;
			@include flexbox(column, center, right);

			&__title {
				color: var(--text-900);
				padding-right: space(4);
				border-right: space(4) solid var(--title-100);
			}

			&__about-us {
				color: var(--text-800);
			}
		}
	}
</style>
