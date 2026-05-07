<template>
	<div class="about-us">
		<TheTitle label="درباره ما" has-divider />
		<div class="about-us__content">
			<p class="about-us__text">
				کلینیکس جایی است که سلامت، تخصص و آرامش در کنار هم معنا پیدا می‌کنند. ما
				در کلینیکس با بهره‌گیری از تیمی مجرب از پزشکان و کادر درمانی حرفه‌ای،
				تلاش می‌کنیم تجربه‌ای متفاوت و مطمئن از خدمات درمانی را برای مراجعان
				فراهم کنیم. در کلینیکس، تمرکز ما بر ارائه خدمات دقیق، به روز و مبتنی بر
				استاندارد های علمی است. از مشاوره‌های تخصصی گرفته تا خدمات تشخیصی و
				درمانی، همه چیز با هدف ارتقای کیفیت زندگی شما طراحی شده است. فضای مدرن و
				آرام کلینیک نیز به گونه‌ای آماده شده تا مراجعان در محیطی امن و صمیمی
				خدمات مورد نیاز خود را دریافت کنند.
			</p>
			<img class="about-us__image" src="/about-us.png" />
		</div>
		<p class="about-us__text">
			ما باور داریم که هر مراجعه‌کننده نیازها و شرایط منحصربه‌فردی دارد. به همین
			دلیل، در کلینیکس رویکرد ما شخصی‌سازی خدمات درمانی و همراهی کامل در مسیر
			بهبود است. پاسخگویی دقیق، نوبت‌دهی منظم و احترام به زمان بیماران از اصول
			اصلی کار ماست. کلینیکس فقط یک مرکز درمانی نیست؛ بلکه همراهی قابل اعتماد
			برای حفظ و ارتقای سلامت شماست.
		</p>
	</div>
</template>

<style lang="scss" scoped>
	.about-us {
		width: 100%;
		@include flexbox(column, center, center, space(6));

		&__content {
			@include flexbox(row, center, start, space(6), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(6));
			}
		}

		&__text {
			color: var(--text-800);
		}

		&__image {
			position: relative;
			width: space(200);
      object-fit: cover;
			border-radius: space(6);
			height: space(100);

			@media (max-width: $md) {
				width: 100%;
			}
		}
	}
</style>
